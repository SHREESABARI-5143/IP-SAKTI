# KNOWLEDGE INGESTION & STATUTORY CORPUS — IP-SAKTI SAHAYAK

The platform ingests primary, verified government statutes, official rules, guidelines, and international treaties.

---

## 1. Verified Statutory Corpus

| Source ID | Statutory Name | Authority | Domain | Version |
|---|---|---|---|---|
| `IN_PATENTS_ACT_1970` | The Patents Act, 1970 (as amended) | CGPDTM / DPIIT | Patent / TK | 2005 Amendment |
| `IN_BD_ACT_2002_2023` | Biological Diversity Act, 2002 & 2023 | National Biodiversity Authority (NBA) | ABS / Biodiversity | 2023 Amendment |
| `IN_DRUGS_COSMETICS_ACT_1940` | Drugs and Cosmetics Act & Rules (Ch. IV-A) | Ministry of AYUSH / CDSCO | Regulatory (ASU) | Rule 158B Consolidated |
| `IN_FSSAI_AYURVEDA_AAHAR_2022` | Food Safety and Standards (Ayurveda Aahar) | FSSAI & Ministry of AYUSH | Regulatory (Food) | 2022 Gazette |
| `IN_TRADEMARKS_GI_ACTS` | Trade Marks Act 1999 & GI Act 1999 | CGPDTM & GI Registry | Trademark / GI | 1999 Consolidated |
| `INTL_WIPO_GRATK_2024` | WIPO Treaty on IP, GR and Associated TK | WIPO | International / TK | May 2024 Treaty |
| `INTL_NAGOYA_PROTOCOL_CBD` | Nagoya Protocol on Access & Benefit Sharing | CBD Secretariat | ABS / International | 2014 Entry into Force |
| `US_FDA_DSHEA_EXPORT` | US FDA DSHEA 1994 & 21 CFR 111 cGMP | US FDA & California OEHHA | Export (USA) | 21 CFR 111 / Prop 65 |
| `EU_THMPD_2004` | EU Traditional Herbal Directive (2004/24/EC) | European Medicines Agency (EMA) | Export (EU) | Directive 2004/24/EC |

---

## 2. Ingestion Pipeline & Checksums

1. **Parser**: Ingests statutory gazette PDF/DOCX/TXT texts.
2. **Cleaner**: Removes boilerplate gazette pagination and normalizes legal section headers.
3. **Metadata Extractor**: Tags provision references (`Section 3(p)`, `Rule 158B`), authority ranks, jurisdiction, and effective dates.
4. **Chunker**: Splits by statutory section and paragraph boundaries.
5. **Integrity Checksum**: Computes SHA-256 hash stored in `source_versions` to detect text modifications or updates.
6. **Indexer**: Populates `source_registry` and `document_chunks`.
