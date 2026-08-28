from __future__ import annotations

import argparse
import ast
from pathlib import Path

from src.flake8_interface_naming.checker import InterfaceNamingChecker


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that interface classes (only abstract methods) start with I.",
    )
    parser.add_argument("paths", nargs="+", help="Python files or directories to check")
    args = parser.parse_args(argv)

    exit_code = 0
    for path_str in args.paths:
        path = Path(path_str)
        files = sorted(path.rglob("*.py")) if path.is_dir() else [path]
        for file_path in files:
            if not file_path.is_file():
                continue
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(file_path))
            checker = InterfaceNamingChecker(tree, str(file_path))
            for line, column, message, _ in checker.run():
                print(f"{file_path}:{line}:{column + 1}: {message}")
                exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
