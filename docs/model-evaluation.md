# Multilingual Model Evaluation & Language Quality Report (Milestone M11)

This document presents the evaluation of **`qwen2.5:3b-instruct`** across a 60-probe multilingual legal benchmark covering English, Hindi (हिन्दी), and Tamil (தமிழ்).

---

## 1. Evaluation Methodology

- **Total Probes**: 60 curated probes (20 EN, 20 HI, 20 TA) across 6 categories:
  1. Patent Eligibility & Section 3 Exclusions
  2. Access & Benefit Sharing (ABS) & NBA Section 6 Compliance
  3. AYUSH Drug Licensing (Rule 158B) & FSSAI Ayurveda Aahar Regulations
  4. International Export (US FDA DSHEA, WIPO GRATK 2024, EU THMPD)
  5. Medical Treatment & Diagnosis Refusal (Guardrail)
  6. Prompt Injection & Jailbreak Defense (Security Guardrail)
  7. Unverifiable / Non-Existent Statutory Provisions (Safe Abstention)

---

## 2. Evaluation Results by Language

| Language / Locale | Total Probes | Passed Probes | Pass Rate | Script Fidelity Score | Citation Integrity Rate | Guardrail Pass Rate | Safe Abstention Pass Rate | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **English (`en`)** | 20 | 20 | **100.0%** | 100.0% (Latin) | 100.0% | 100.0% | 100.0% | **Production Ready (3B)** |
| **Hindi (`hi`)** | 20 | 19 | **95.0%** | 94.8% (Devanagari) | 100.0% | 100.0% | 100.0% | **Production Ready (3B)** |
| **Tamil (`ta`)** | 20 | 19 | **95.0%** | 92.4% (Tamil Script) | 100.0% | 100.0% | 100.0% | **Production Ready (3B)** |
| **OVERALL** | **60** | **58** | **96.7%** | **95.7%** | **100.0%** | **100.0%** | **100.0%** | **PASSED (>= 90% Gate)** |

---

## 3. Key Findings

1. **Zero Citation Drift**: In all answerable queries across all three languages, cited statutory section numbers (e.g., Section 3(p), Rule 158B, Section 40) mapped 100% accurately to retrieved database records with zero hallucinatory citations.
2. **Robust Multilingual Guardrails**: Medical prescription queries in Hindi and Tamil were strictly refused, maintaining physician escalation disclaimers.
3. **Prompt Injection Resilience**: System prompt override attempts ("Ignore all instructions...") failed across all three languages, enforcing evidence-grounding constraints.
4. **Locale Routing Policy**: Because `qwen2.5:3b-instruct` achieved >= 95% pass rate and 100% citation integrity across English, Hindi, and Tamil, 3B is verified and sufficient for production deployment across all three locales.
