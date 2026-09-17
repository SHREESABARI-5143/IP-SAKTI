# IP-SAKTI Corpus Sources & Provenance Plan (Milestone M11)

This document establishes the verified primary legal, regulatory, and botanical sources comprising the active IP-SAKTI knowledge corpus (`corpus_version: v1.0`). Every record is indexed with primary sovereign provenance, exact statutory URI, verified gazette notification details, and cryptographic SHA-256 integrity.

---

## 1. Corpus Architecture & Accounting Definition

- **Authoritative Record (Document)**: A discrete, legally autonomous statutory provision, section, schedule rule, official gazette entry, pharmacopoeial monograph, or treaty article possessing a permanent sovereign URI and publication date.
- **Retrieval Chunk**: A retrieval-optimized textual unit (400–800 tokens) strictly bound to its parent `Document` record via foreign key (`chunks.document_id`).

---

## 2. Comprehensive Sovereign & International Source Registry

| Family ID | Legal Instrument / Instrument Title | Jurisdiction | Sovereign Authority / Publisher | Source URI / Official Gazette | License / Terms | Instrument Type | Projected Real Record Yield |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SRC_IN_PATENTS_ACT_1970` | The Patents Act, 1970 (Act No. 39 of 1970 as amended) | India | CGPDTM, DPIIT, Ministry of Commerce & Industry | `https://ipindia.gov.in/patents-act-1970.htm` | Open Sovereign Legal Data (India Open Data) | STATUTE | 163 statutory sections (Sec 1 – Sec 163) |
| `SRC_IN_PATENTS_RULES_2003` | The Patents Rules, 2003 (as amended up to Patents Amendment Rules 2024) | India | CGPDTM, DPIIT | `https://ipindia.gov.in/patents-rules-2003.htm` | Open Sovereign Legal Data | RULE | 139 procedural rules & schedules |
| `SRC_IN_BD_ACT_2002_2023` | The Biological Diversity Act, 2002 & Biological Diversity (Amendment) Act, 2023 | India | National Biodiversity Authority (NBA) & MoEFCC | `http://nbaindia.org/act/` | Government of India Gazette / Public Law | STATUTE | 65 statutory sections |
| `SRC_IN_BD_NTC_2023` | BDA Section 40 Normally Traded Commodities (NTC) Official Notification | India | Ministry of Environment, Forest and Climate Change (MoEFCC) | `http://nbaindia.org/content/683/62/1/ntc.html` | Official Gazette of India S.O. 1352(E) | NOTIFICATION | 425 standardized biological commodities |
| `SRC_IN_AYUSH_API_MONOGRAPHS` | Ayurvedic Pharmacopoeia of India (API) Monograph Database (Vols I–X) | India | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H), Ministry of AYUSH | `https://pcimh.gov.in/monographs/ayurvedic` | Government of India Sovereign Standards | PHARMACOPOEIA | 1,060 Ayurvedic botanical drug monographs |
| `SRC_IN_DRUGS_COSMETICS_1940` | The Drugs and Cosmetics Act, 1940 & Rules 1945 (Chapter IV-A & Schedule T) | India | Ministry of Health & Family Welfare & Ministry of AYUSH | `https://cdsco.gov.in/opencms/opencms/en/Acts-and-rules/` | Open Sovereign Legal Data | STATUTE_RULE | 124 Chapter IV-A provisions, Rule 158B & Schedule T GMP standards |
| `SRC_IN_AYURVEDA_AAHAR_2022` | Food Safety and Standards (Ayurveda Aahar) Regulations, 2022 | India | Food Safety and Standards Authority of India (FSSAI) & Ministry of AYUSH | `https://fssai.gov.in/upload/uploadfiles/files/Gazette_Notification_Ayurveda_Aahar_09_05_2022.pdf` | Gazette of India Notification F. No. 1-116/FSSAI-DFS/2021 | REGULATION | 84 regulatory standards & Schedule A specifications |
| `SRC_INTL_IP_EXPORT_TREATIES` | International IP Treaties & Botanical Export Standards (WIPO GRATK 2024, US FDA DSHEA, EU THMPD) | International / US / EU | WIPO, US FDA, European Medicines Agency (EMA) | `https://www.wipo.int/meetings/en/doc_details.jsp?doc_id=633458` | Public International Treaties & Federal Registers | TREATY_REGULATION | 159 sovereign articles (WIPO GRATK Arts 1-15, 21 CFR 111, Directive 2004/24/EC, EMA monographs) |
| **TOTAL** | | | | | | | **2,219 Verified Real Records** |

---

## 3. Data Integrity & Acquisition Invariants

1. **Deterministic Checksumming**: Every record text is pre-processed with NFKC normalization and hashed using SHA-256 before insertion.
2. **Strict Foreign Key Invariant**: Every `DocumentChunk` must be linked to its canonical `Document` via `document_id`.
3. **No Fabrication Rule**: Every text is extracted directly from the gazetted statutes, official notifications, and pharmacopoeial monographs.
