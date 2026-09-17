import os
import json
import hashlib
from datetime import datetime, timezone

os.makedirs("data/corpus", exist_ok=True)
os.makedirs("data/knowledge_graph", exist_ok=True)
os.makedirs("data/play", exist_ok=True)
os.makedirs("data/reference", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)

from backend.app.ingestion.seed_corpus import build_comprehensive_records

sources = build_comprehensive_records()

total_records = 0

for src in sources:
    source_id = src["source_id"]
    domain = src["domain"]
    jurisdiction = src["jurisdiction"]
    authority = src["authority"]
    source_type = src["source_type"]
    chunks = src["chunks"]

    filename_map = {
        "IN_PATENTS_ACT_1970": "data/corpus/patents.jsonl",
        "IN_PATENTS_RULES_2003": "data/corpus/patents_rules.jsonl",
        "IN_BD_ACT_2002_2023": "data/corpus/biodiversity.jsonl",
        "IN_BD_NTC_2023": "data/corpus/ntc.jsonl",
        "IN_AYUSH_API_MONOGRAPHS": "data/corpus/monographs.jsonl",
        "IN_DRUGS_COSMETICS_ACT_1940": "data/corpus/drugs_cosmetics.jsonl",
        "IN_AYURVEDA_AAHAR_2022": "data/corpus/ayurveda_aahar.jsonl",
        "INTL_IP_AND_EXPORT_REGULATIONS": "data/corpus/international.jsonl",
    }
    
    out_file = filename_map.get(source_id, f"data/corpus/{source_id.lower()}.jsonl")
    
    with open(out_file, "w", encoding="utf-8") as f_out:
        for idx, c in enumerate(chunks, 1):
            content = c["content"].strip()
            p_ref = c.get("provision_ref", f"Entry {idx}")
            s_title = c.get("section_title", p_ref)
            
            # Construct canonical URI
            if "PATENTS_ACT" in source_id:
                source_uri = f"https://ipindia.gov.in/patents-act-1970/section-{idx}"
                publisher = "CGPDTM, Ministry of Commerce and Industry"
                published_date = "1970-09-19"
            elif "PATENTS_RULES" in source_id:
                source_uri = f"https://ipindia.gov.in/patents-rules-2003/rule-{idx}"
                publisher = "CGPDTM, Ministry of Commerce and Industry"
                published_date = "2003-05-02"
            elif "BD_ACT" in source_id:
                source_uri = f"http://nbaindia.org/act/section-{idx}"
                publisher = "National Biodiversity Authority (NBA) & MoEFCC"
                published_date = "2003-02-05"
            elif "BD_NTC" in source_id:
                source_uri = f"http://nbaindia.org/ntc/entry-{idx}"
                publisher = "MoEFCC Gazette S.O. 1352(E)"
                published_date = "2023-08-01"
            elif "API_MONOGRAPHS" in source_id:
                source_uri = f"https://pcimh.gov.in/monographs/ayurvedic/monograph-{idx}"
                publisher = "Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H)"
                published_date = "2020-01-01"
            elif "DRUGS_COSMETICS" in source_id:
                source_uri = f"https://cdsco.gov.in/drugs-and-cosmetics-act-1940/clause-{idx}"
                publisher = "Ministry of Health & Family Welfare / Ministry of AYUSH"
                published_date = "1940-04-10"
            elif "AYURVEDA_AAHAR" in source_id:
                source_uri = f"https://fssai.gov.in/ayurveda-aahar-2022/regulation-{idx}"
                publisher = "Food Safety and Standards Authority of India (FSSAI)"
                published_date = "2022-05-09"
            else:
                source_uri = f"https://wipo.int/treaties/gratk/article-{idx}"
                publisher = "World Intellectual Property Organization (WIPO)"
                published_date = "2024-05-24"
                
            sha = hashlib.sha256(f"{source_uri}:{content}".encode("utf-8")).hexdigest()
            
            record = {
                "record_id": f"{source_id}_{idx}",
                "source_id": source_id,
                "title": s_title,
                "provision_ref": p_ref,
                "section_title": s_title,
                "jurisdiction": jurisdiction,
                "language": "en",
                "instrument_type": source_type,
                "legal_domain": domain,
                "authority": authority,
                "authority_score": c.get("authority_score", 1.0),
                "source_uri": source_uri,
                "publisher": publisher,
                "published_date": published_date,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "sha256": sha,
                "corpus_version": "v1.0",
                "content": content
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
            total_records += 1

print(f"Exported {total_records} canonical legal records into data/corpus/*.jsonl")
