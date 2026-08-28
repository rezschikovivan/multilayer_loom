from __future__ import annotations

import ast
from collections.abc import Generator, Iterable

ABSTRACT_DECORATOR_NAMES = frozenset(
    {
        "abstractmethod",
        "abstractclassmethod",
        "abstractstaticmethod",
    }
)


def _decorator_name(decorator: ast.expr) -> str | None:
    if isinstance(decorator, ast.Name):
        return decorator.id
    if isinstance(decorator, ast.Attribute):
        return decorator.attr
    if isinstance(decorator, ast.Call):
        return _decorator_name(decorator.func)
    return None


def _is_abstract_method(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(
        _decorator_name(decorator) in ABSTRACT_DECORATOR_NAMES
        for decorator in node.decorator_list
    )


def _class_methods(class_node: ast.ClassDef) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    return [
        node
        for node in class_node.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def _is_interface(class_node: ast.ClassDef) -> bool:
    methods = _class_methods(class_node)
    if not methods:
        return False
    return all(_is_abstract_method(method) for method in methods)


class InterfaceNamingChecker:
    name = "flake8-interface-naming"
    version = "1.0.0"

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self._tree = tree
        self._filename = filename

    def run(self) -> Generator[tuple[int, int, str, type[InterfaceNamingChecker]], None, None]:
        for class_node in _iter_class_defs(self._tree):
            if not _is_interface(class_node):
                continue
            if class_node.name.startswith("I") and class_node.name[1:2].isupper():
                continue

            message = (
                f"IFC001 Interface class `{class_node.name}` must start with `I` "
                "(classes that contain only abstract methods are considered interfaces)"
            )
            yield (
                class_node.lineno,
                class_node.col_offset,
                message,
                type(self),
            )


def _iter_class_defs(tree: ast.AST) -> Iterable[ast.ClassDef]:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            yield node
