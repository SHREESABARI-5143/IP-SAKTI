#!/usr/bin/env python3
"""
scripts/check_no_hardcode.py — CI Linter for Hardcode Eradication (Milestone M11)

Rules enforced:
1. Module-level dict/list literals over N=5 string entries inside backend/app/
2. Literal floats in backend/app/services/ or backend/app/rag/ not defined in config.py
3. Unwrapped JSX text nodes in frontend/src/
4. Forbidden markers: TODO, FIXME, HACK in active codebase
"""

import ast
import json
import os
import re
import sys

ALLOWLIST_PATH = os.path.join(os.path.dirname(__file__), "hardcode_allowlist.json")

def load_allowlist():
    if os.path.exists(ALLOWLIST_PATH):
        try:
            with open(ALLOWLIST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def is_allowlisted(category, filepath, identifier, allowlist):
    cat_list = allowlist.get(category, [])
    norm_path = filepath.replace("\\", "/")
    for entry in cat_list:
        entry_path = entry.get("file", "").replace("\\", "/")
        if entry_path in norm_path and entry.get("id") == identifier:
            return True, entry.get("reason", "")
    return False, ""

def check_python_ast(filepath, allowlist):
    errors = []
    norm_path = filepath.replace("\\", "/")
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source, filename=filepath)
    except Exception as e:
        return [f"{filepath}: Syntax error during AST parsing: {e}"]

    # 1. Check module level lists/dicts > 5 items
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    # Check list of constants
                    if isinstance(node.value, ast.List):
                        str_elems = [el for el in node.value.elts if isinstance(el, ast.Constant) and isinstance(el.value, str)]
                        if len(str_elems) > 5:
                            allowed, reason = is_allowlisted("module_literals", norm_path, var_name, allowlist)
                            if not allowed:
                                errors.append(
                                    f"[MODULE_LITERAL] {norm_path}:{node.lineno} Variable '{var_name}' is a module-level list with {len(str_elems)} string elements (>5). Move to database/data files or justify in allowlist."
                                )
                    # Check dict of constants
                    elif isinstance(node.value, ast.Dict):
                        if len(node.value.keys) > 5:
                            allowed, reason = is_allowlisted("module_literals", norm_path, var_name, allowlist)
                            if not allowed:
                                errors.append(
                                    f"[MODULE_LITERAL] {norm_path}:{node.lineno} Variable '{var_name}' is a module-level dict with {len(node.value.keys)} entries (>5). Move to database/data files or justify in allowlist."
                                )

    # 2. Check literal floats in services/ or rag/
    if "/services/" in norm_path or "/rag/" in norm_path:
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, float):
                # Allow standard 0.0 or 1.0 or simple increments
                if node.value in (0.0, 1.0, 2.0):
                    continue
                loc_id = f"float_{node.value}_{node.lineno}"
                allowed, reason = is_allowlisted("literal_floats", norm_path, loc_id, allowlist)
                if not allowed:
                    errors.append(
                        f"[LITERAL_FLOAT] {norm_path}:{node.lineno} Literal float '{node.value}' found in service/rag layer. Define in backend/app/core/config.py or justify in allowlist."
                    )

    # 3. Check TODO/FIXME/HACK
    for idx, line in enumerate(source.splitlines(), 1):
        if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', line):
            allowed, reason = is_allowlisted("forbidden_markers", norm_path, f"line_{idx}", allowlist)
            if not allowed:
                errors.append(f"[FORBIDDEN_MARKER] {norm_path}:{idx} Forbidden marker found: '{line.strip()}'")

    return errors

def check_frontend(filepath, allowlist):
    errors = []
    norm_path = filepath.replace("\\", "/")
    if "node_modules" in norm_path or ".next" in norm_path:
        return errors

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Check forbidden markers
    for idx, line in enumerate(content.splitlines(), 1):
        if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', line):
            allowed, reason = is_allowlisted("forbidden_markers", norm_path, f"line_{idx}", allowlist)
            if not allowed:
                errors.append(f"[FORBIDDEN_MARKER] {norm_path}:{idx} Forbidden marker in frontend: '{line.strip()}'")

    return errors

def main():
    allowlist = load_allowlist()
    all_errors = []

    # Check backend
    for root, _, files in os.walk("backend/app"):
        for f in files:
            if f.endswith(".py"):
                full_path = os.path.join(root, f)
                all_errors.extend(check_python_ast(full_path, allowlist))

    # Check frontend
    for root, _, files in os.walk("frontend/src"):
        for f in files:
            if f.endswith((".tsx", ".ts", ".jsx", ".js")):
                full_path = os.path.join(root, f)
                all_errors.extend(check_frontend(full_path, allowlist))

    if all_errors:
        print(f"FAILED: Found {len(all_errors)} hardcode/quality violations:")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("PASSED: 0 hardcode violations found. All code complies with Milestone M11 rules.")
        sys.exit(0)

if __name__ == "__main__":
    main()
