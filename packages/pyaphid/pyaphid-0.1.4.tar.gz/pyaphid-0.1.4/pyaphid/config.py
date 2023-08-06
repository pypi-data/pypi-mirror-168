from __future__ import annotations

import typing as t

import tomli


def pyproject():
    with open("pyproject.toml", "rb") as f:
        return tomli.load(f)


def get_pyaphid_toml_section() -> dict[str, t.Any] | None:
    pyproject_toml = pyproject()
    if "tool" in pyproject_toml:
        if "pyaphid" in pyproject_toml["tool"]:
            return pyproject_toml["tool"]["pyaphid"]
    return None  # pragma: no cover


def get_forbidden_calls() -> list[str]:
    """Get forbidden calls from pyproject.toml"""
    aphid_section = get_pyaphid_toml_section()
    if aphid_section and "forbidden" in aphid_section:
        return aphid_section["forbidden"]

    return []  # pragma: no cover
