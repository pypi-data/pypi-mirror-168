from __future__ import annotations

import ast
import os
import typing as t

import typer

from pyaphid import config
from pyaphid.analyzer import ExpandedCallCollector, Transformer, Visitor
from pyaphid.helpers import echo_with_line_ref


def collect_python_files(files_and_dirs: list[str]):
    files: list[str] = []
    for file_or_dir in files_and_dirs:
        path = os.path.abspath(file_or_dir)
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(file_or_dir)
        elif os.path.isdir(path):
            for dirpath, _, filenames in os.walk(file_or_dir, followlinks=False):
                for filename in filenames:
                    if filename.endswith(".py"):
                        files.append(f"{dirpath}/{filename}")

    return files


app = typer.Typer(name="pyaphid")


@app.command()
def main(
    files_and_dirs: t.List[str] = typer.Argument(
        None, show_default=False, help="Multiple files and/or directories to work with"
    ),
    # omit: bool = typer.Option(
    #    False,
    #   "--omit",
    #   "-o",
    #  rich_help_panel="Pyaphid options",
    # show_default=False,
    # help="Remove calls from falls (might destroy formatting)",
    # ),
    print_names_only: bool = typer.Option(
        False,
        "--names",
        "-n",
        rich_help_panel="Pyaphid options",
        show_default=False,
        help="Print only the expandend names of calls in files",
    ),
):
    if not files_and_dirs:
        typer.echo("Please provide files and/or directories to check")
        raise typer.Exit(1)
    files = collect_python_files(files_and_dirs)
    forbidden = config.get_forbidden_calls()
    omit = False
    exit_code = 0
    cls: type[Transformer] | type[Visitor] | type[ExpandedCallCollector]
    if print_names_only:
        cls = ExpandedCallCollector
    elif omit:  # pragma: no cover
        cls = Transformer
    else:
        cls = Visitor

    for filepath in files:
        with open(filepath, "rb") as f:
            tree = ast.parse(f.read())
        visitor = cls(filepath=filepath, forbidden=forbidden)
        visitor.visit(tree)
        if isinstance(visitor, ExpandedCallCollector):
            names = visitor.calls
        else:
            names = visitor.matches
        exit_code += len(names)
        for match, expanded_call_name in names:
            echo_with_line_ref(filepath, match, expanded_call_name)

        # if omit and names:
        #    with open(filepath, "w") as f:
        #        f.write(ast.unparse(tree))

    if not exit_code:
        typer.echo("Nothing found")

    raise typer.Exit(exit_code if not print_names_only else 0)


def run():  # pragma: no cover

    app()
