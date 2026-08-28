from __future__ import annotations

from src.flake8_interface_naming.checker import InterfaceNamingChecker

__all__ = ["InterfaceNamingChecker"]


class Plugin:
    name = InterfaceNamingChecker.name
    version = InterfaceNamingChecker.version

    def __init__(self, tree, filename: str) -> None:
        self._checker = InterfaceNamingChecker(tree, filename)

    def run(self):
        yield from self._checker.run()
