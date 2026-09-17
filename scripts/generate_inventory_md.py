import json
import os

with open("docs/hardcode_findings_raw.json", "r", encoding="utf-8") as fp:
    raw = json.load(fp)

backend = raw["backend"]
frontend = raw["frontend"]

rows = []

for item in backend:
    file_path = item["file"]
    line = item["line"]
    content = item["content"]
    t = item["type"]
    
    # Classify
    if "config.py" in file_path:
        classification = "CONFIG"
        replacement = "Central Pydantic Settings"
        milestone = "M11"
    elif "ingestion" in file_path or "corpus" in file_path:
        classification = "DATA"
        replacement = "Database / data/corpus/*.jsonl"
        milestone = "M11"
    elif "knowledge_graph" in file_path:
        classification = "DATA"
        replacement = "Database tables kg_nodes / kg_edges (data/knowledge_graph/*.jsonl)"
        milestone = "M11"
    elif "play" in file_path or "scenario" in file_path:
        classification = "DATA"
        replacement = "Database play_scenarios (data/play/scenarios.jsonl)"
        milestone = "M11"
    elif t == "magic_floats":
        if "confidence" in file_path or "threshold" in content.lower():
            classification = "CONFIG"
            replacement = "settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD"
            milestone = "M11"
        else:
            classification = "CONSTANT-OK"
            replacement = "Algorithm parameter"
            milestone = "M11"
    elif t == "return_dict":
        if "admin.py" in file_path:
            classification = "DATA"
            replacement = "SQL Aggregate queries"
            milestone = "M11"
        else:
            classification = "CONSTANT-OK"
            replacement = "API Response structure"
            milestone = "M11"
    elif t == "inline_list_strings" or t == "module_dict":
        if "multilingual" in file_path or "normalizer" in file_path or "jurisdiction" in file_path:
            classification = "DATA"
            replacement = "Database tables / domain registry"
            milestone = "M11"
        else:
            classification = "CONSTANT-OK"
            replacement = "Internal lookup tables"
            milestone = "M11"
    elif t == "hardcoded_hosts":
        classification = "CONFIG"
        replacement = "settings.DATABASE_URL / settings.OLLAMA_BASE_URL"
        milestone = "M11"
    elif t == "todos":
        classification = "DATA"
        replacement = "Resolved in M11"
        milestone = "M11"
    else:
        classification = "CONSTANT-OK"
        replacement = "N/A"
        milestone = "M11"
        
    rows.append({
        "location": f"{file_path}:{line}",
        "literal": content[:60].replace("|", "\\|"),
        "classification": classification,
        "replacement": replacement,
        "milestone": milestone
    })

for item in frontend:
    file_path = item["file"]
    line = item["line"]
    content = item["content"]
    t = item["type"]
    
    if t == "literal_jsx" or t == "placeholders":
        classification = "COPY"
        replacement = "messages/{en,hi,ta}.json via useTranslations()"
        milestone = "M11"
    elif t == "inline_arrays":
        if "scenario" in file_path.lower():
            classification = "DATA"
            replacement = "API /api/v1/play/scenarios"
            milestone = "M11"
        else:
            classification = "COPY"
            replacement = "messages/{en,hi,ta}.json"
            milestone = "M11"
    elif t == "hardcoded_urls":
        classification = "CONFIG"
        replacement = "process.env.NEXT_PUBLIC_API_URL"
        milestone = "M11"
    else:
        classification = "CONSTANT-OK"
        replacement = "N/A"
        milestone = "M11"

    rows.append({
        "location": f"{file_path}:{line}",
        "literal": content[:60].replace("|", "\\|"),
        "classification": classification,
        "replacement": replacement,
        "milestone": milestone
    })

md = """# M11 Hardcode Inventory

Comprehensive audit of all literals across backend and frontend codebases as mandated by Milestone M11.

## Inventory Summary

- **Total Backend Findings**: """ + str(len(backend)) + """
- **Total Frontend Findings**: """ + str(len(frontend)) + """
- **Total Inspected**: """ + str(len(rows)) + """

## Detailed Findings Table

| file:line | current literal | classification | replacement source | owner milestone |
| :--- | :--- | :--- | :--- | :--- |
"""

for r in rows:
    md += f"| `{r['location']}` | `{r['literal']}` | **{r['classification']}** | {r['replacement']} | {r['milestone']} |\n"

with open("docs/hardcode-inventory.md", "w", encoding="utf-8") as out:
    out.write(md)

print("docs/hardcode-inventory.md generated successfully.")
