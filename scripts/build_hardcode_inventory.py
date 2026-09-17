import os
import re
import json

patterns = {
    "magic_floats": re.compile(r'=\s*0\.\d+'),
    "inline_list_strings": re.compile(r'=\s*\[\s*["\'][^"\']+["\'](?:\s*,\s*["\'][^"\']+["\'])*\s*\]'),
    "module_dict": re.compile(r'^\s*[A-Z_]{2,}\s*=\s*\{'),
    "return_dict": re.compile(r'return\s+\{.*["\']'),
    "todos": re.compile(r'\b(TODO|FIXME|HACK|XXX|stub|dummy|placeholder|mock)\b', re.I),
    "hardcoded_hosts": re.compile(r'(localhost|127\.0\.0\.1|:8000|:11434|:5432)')
}

findings = []

for root, dirs, files in os.walk("backend/app"):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f).replace("\\", "/")
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                lines = fp.readlines()
            for idx, line in enumerate(lines, 1):
                clean_line = line.strip()
                if clean_line.startswith("#"):
                    m = patterns["todos"].search(clean_line)
                    if m:
                        findings.append({
                            "file": path,
                            "line": idx,
                            "type": "todos",
                            "content": clean_line,
                            "match": m.group(0)
                        })
                    continue
                for p_name, p in patterns.items():
                    m = p.search(clean_line)
                    if m:
                        findings.append({
                            "file": path,
                            "line": idx,
                            "type": p_name,
                            "content": clean_line,
                            "match": m.group(0)
                        })

print(f"Total backend findings: {len(findings)}")

fe_patterns = {
    "literal_jsx": re.compile(r'>\s*([A-Z][a-z]{2,}[^<]{3,})\s*<'),
    "inline_arrays": re.compile(r'const\s+\w+\s*=\s*\['),
    "placeholders": re.compile(r'(placeholder=|aria-label=|title=)["\']([^"\']+)["\']'),
    "hardcoded_urls": re.compile(r'https?://[^\s"\']+')
}

fe_findings = []
for root, dirs, files in os.walk("frontend/src"):
    if "node_modules" in root or ".next" in root:
        continue
    for f in files:
        if f.endswith((".tsx", ".ts", ".jsx", ".js")):
            path = os.path.join(root, f).replace("\\", "/")
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                lines = fp.readlines()
            for idx, line in enumerate(lines, 1):
                clean_line = line.strip()
                for p_name, p in fe_patterns.items():
                    m = p.search(clean_line)
                    if m:
                        fe_findings.append({
                            "file": path,
                            "line": idx,
                            "type": p_name,
                            "content": clean_line,
                            "match": m.group(0)
                        })

print(f"Total frontend findings: {len(fe_findings)}")

os.makedirs("docs", exist_ok=True)
with open("docs/hardcode_findings_raw.json", "w", encoding="utf-8") as out:
    json.dump({"backend": findings, "frontend": fe_findings}, out, indent=2)
