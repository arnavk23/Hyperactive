#!/usr/bin/env python3
"""Scan src/hyperactive for public classes missing docstrings."""
import ast
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.abspath(os.path.join(ROOT, "src/hyperactive"))

missing = []

for dirpath, dirnames, filenames in os.walk(SRC):
    # skip tests and migrations
    if "tests" in dirpath.split(os.sep):
        continue
    for fn in filenames:
        if not fn.endswith(".py"):
            continue
        path = os.path.join(dirpath, fn)
        # skip __init__ files
        try:
            with open(path, "r", encoding="utf-8") as f:
                src = f.read()
        except Exception:
            continue
        try:
            tree = ast.parse(src, filename=path)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                name = node.name
                # consider public classes only
                if name.startswith("_"):
                    continue
                # check if class docstring exists
                doc = ast.get_docstring(node)
                if doc is None:
                    # record location
                    missing.append((path, node.lineno, name))

if not missing:
    print("No missing public class docstrings found.")
else:
    print("Public classes missing docstrings:\n")
    for path, lineno, name in missing:
        rel = os.path.relpath(path, os.path.abspath(os.path.join(ROOT, "..")))
        print(f"{path}:{lineno} -> class {name}")

if __name__ == '__main__':
    pass
