# ADR-003: Multilingual Concept Normalization & Script Normalization

## Status
Accepted

## Context
Ayurvedic botanical names and statutory terminology are expressed in Devanagari Hindi (उदा. अश्वगंधा, त्रिफला, धारा ३(p)), Tamil (எ.கா. அஸ்வகந்தா, பிரிவு 3(p)), and Tanglish/Hinglish. Direct embedding models often experience cross-lingual semantic drift on specialized Indic pharmacopoeial terms.

## Decision
We utilize a multi-tier concept normalizer:
1. Regex and Unicode script detection for language identification (`en`, `hi`, `ta`).
2. Pharmacopoeial botanical and legal dictionary expansion mapping vernacular terms to canonical Sanskrit/Latin scientific names and statutory provisions.
3. Multilingual response synthesis maintaining statutory citation numbers and official gazette section nomenclature.

## Consequences
- **Positive**: Sub-millisecond normalization without heavy GPU translation model overhead.
- **Positive**: Accurate cross-lingual retrieval against Indian Acts regardless of input query language.
