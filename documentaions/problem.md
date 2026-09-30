# IP-SAKTI Sahayak — Problem Definition

> **Document ID:** IPSAKTI-PRB-001  
> **Version:** 1.0  
> **Status:** Ideation / Pre-Build  
> **Owner:** Product & Strategy  
> **Last Updated:** 2026-09-27  
> **Prerequisite:** Read [context.md](file:///E:/Projects/Active/IP-SAKTI-1/documents/context.md) first.

---

## 1. Problem Statement (One-Liner)

**Ayurvedic innovators, manufacturers, and practitioners have no single, authoritative, multilingual system that maps their product to the correct IP protection pathway *and* regulatory classification — simultaneously — while keeping Indian and international legal layers distinct, source-cited, and current.**

---

## 2. The Five Core Pain Points

### Pain Point 1 — Regime Fragmentation

An Ayurvedic product's IP and regulatory compliance sits across **7+ distinct legal regimes** (patents, GI, trademarks, copyright, designs, plant-variety rights, trade secrets) plus drug-regulatory and biodiversity-access requirements. No tool, portal, or advisor unifies these into a single guided workflow.

**Impact:**
- MSME founders spend 3-6 months and ₹3-8 lakh just to *understand* which IP instruments apply, before even filing.
- 60%+ of AYUSH patent applications face TKDL prior-art objections because applicants didn't know about existing formulations.
- Startups frequently file the *wrong* type of protection (e.g., trademark when they needed a GI, or patent when the formulation is already in AFI).

### Pain Point 2 — Jurisdictional Conflation

Indian IP law and international treaties have **different rules for identical concepts**. Example:

| Question | Indian Answer | International Answer |
|---|---|---|
| "Can I patent a classical Ayurvedic formulation?" | **No** — Section 3(p) of Patents Act bars patents on TK *per se* | **Depends** — Novelty/non-obviousness assessed against TKDL prior art; a novel modification *may* be patentable under PCT/national phases |
| "What ABS obligations apply?" | Biological Diversity Act 2002 + NBA/SBB approval | Nagoya Protocol + CBD Article 15; national law of the source country governs |
| "How do I protect my brand name?" | Trade Marks Act 1999 + AYUSH licensing name approval | Madrid Protocol for international TM registration |

Existing AI assistants (ChatGPT, Gemini, Copilot) routinely **blend these layers** in a single answer, giving the user incorrect or misleading guidance. There is no "jurisdiction switch" in any existing tool.

### Pain Point 3 — Product Classification Complexity

Before any IP advice is meaningful, the product must be correctly classified. The AYUSH regulatory framework recognises **six distinct product categories**, each with radically different IP and licensing implications:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AYUSH PRODUCT CLASSIFICATION                     │
├─────────────────┬───────────────────────────────────────────────────┤
│ Category        │ Key Characteristic                               │
├─────────────────┼───────────────────────────────────────────────────┤
│ 1. Classical /  │ Formulation + method from First-Schedule         │
│    Generic      │ authoritative text (Charaka, Sushruta, etc.)     │
├─────────────────┼───────────────────────────────────────────────────┤
│ 2. Patent &     │ Manufacturer's proprietary composition; not in   │
│    Proprietary  │ authoritative texts; own brand name              │
├─────────────────┼───────────────────────────────────────────────────┤
│ 3. New / Non-   │ Novel drug requiring proof of safety &           │
│    Classical    │ effectiveness; clinical trials needed             │
├─────────────────┼───────────────────────────────────────────────────┤
│ 4. Phytopharma- │ Purified plant-fraction standardised drug;       │
│    ceutical     │ regulated under allopathic-like pathway           │
├─────────────────┼───────────────────────────────────────────────────┤
│ 5. AYUSH Aahar  │ Nutraceutical / health supplement; FSSAI-        │
│    / Nutra      │ regulated, not D&C Act                           │
├─────────────────┼───────────────────────────────────────────────────┤
│ 6. Cosmetic     │ Ayurvedic cosmetic product; Cosmetics Rules      │
│                 │ 2020 pathway                                     │
└─────────────────┴───────────────────────────────────────────────────┘
```

**The classification determines everything downstream** — which IP instruments are available, which licences are needed, which clinical evidence is required, and which regulatory body has jurisdiction. Getting it wrong wastes months and money.

Currently, this classification requires a **human expert** (regulatory affairs consultant + IP attorney). There is no assisted, questionnaire-driven tool for it.

### Pain Point 4 — Source Trust Deficit

Legal and regulatory guidance demands **source citations**. Users need to know:
- Which exact section of which Act or Rule says X
- Which pharmacopoeial monograph defines the standard for ingredient Y
- Which court/tribunal order established precedent Z

Current AI assistants either:
- **Hallucinate** citations (fabricated section numbers, non-existent cases)
- Provide **no citations** at all
- Provide citations that are **outdated** (pre-amendment text)

For a government-endorsed tool serving the Ministry of Ayush, hallucinated legal advice is **unacceptable** and potentially actionable.

### Pain Point 5 — Language Barrier

- **65%+** of AYUSH MSMEs operate in Hindi or regional-language environments.
- Legal texts exist primarily in English; some in Hindi.
- Ayurvedic terminology is in **Sanskrit** (with regional transliterations).
- No existing IP tool provides Ayurveda-specific guidance in Hindi, Tamil, Telugu, Kannada, Marathi, or Bengali.
- Users in Tier-2/3 cities — the bulk of AYUSH manufacturing — are functionally excluded from English-only IP guidance tools.

---

## 3. User Personas

### Persona 1: Rajesh Sharma — AYUSH MSME Manufacturer

| Attribute | Detail |
|---|---|
| **Age / Location** | 42, Haridwar, Uttarakhand |
| **Language** | Hindi (primary), English (basic reading) |
| **Business** | 15-employee Ayurvedic medicine unit; ₹2 crore annual revenue |
| **Products** | 12 classical formulations + 3 proprietary products |
| **IP Status** | Trademark registered for brand; no patents; no GI; no ABS compliance check |
| **Goal** | Protect his 3 proprietary formulations + explore GI for a Haridwar-specific preparation |
| **Frustration** | "I went to a patent attorney in Delhi — ₹5 lakh just for consultation + filing. He told me one of my products can't be patented because it's already in Sharngadhara Samhita. I wish I'd known that before spending ₹50,000 on the trip." |
| **Desired Outcome** | Self-service tool that tells him *before* he hires a lawyer: what can be patented, what's already in TKDL/AFI, and what licences he needs |

### Persona 2: Dr. Meera Nair — AYUSH Startup Founder

| Attribute | Detail |
|---|---|
| **Age / Location** | 34, Bengaluru, Karnataka |
| **Language** | English (primary), Kannada, Hindi |
| **Business** | AYUSH nutraceutical startup; ₹80 lakh seed funding |
| **Products** | Novel turmeric-based bioavailability-enhanced supplement |
| **IP Status** | Provisional patent filed (India); exploring PCT |
| **Goal** | Understand if her product is a "drug" or "nutraceutical" under FSSAI/AYUSH rules; file international patent; ensure ABS compliance for turmeric sourcing |
| **Frustration** | "My lawyer says it's a drug, my regulatory consultant says it's AYUSH Aahar, and my investor wants clarity before Series A. Three experts, three answers." |
| **Desired Outcome** | Definitive, cited classification of her product + IP roadmap for India and international markets |

### Persona 3: Ankit Verma — Ministry of Ayush Policy Officer

| Attribute | Detail |
|---|---|
| **Age / Location** | 29, New Delhi |
| **Language** | Hindi (primary), English (fluent) |
| **Role** | Deputy Director, IP Cell, Ministry of Ayush |
| **Task** | Respond to RTI queries, prepare policy briefs, advise state AYUSH directorates |
| **Goal** | Quick, cited answers to complex IP + regulatory questions from diverse stakeholders |
| **Frustration** | "I handle 50+ queries a month. Each one requires cross-referencing 3-4 Acts, rules, and sometimes international treaties. There's no internal tool — I do it manually with PDF searches." |
| **Desired Outcome** | Internal assistant that gives cited answers he can copy-paste into official responses |

### Persona 4: Prof. Sunita Devi — AYUSH Researcher

| Attribute | Detail |
|---|---|
| **Age / Location** | 55, BHU Varanasi |
| **Language** | Hindi (primary), Sanskrit (reading), English |
| **Role** | Professor of Dravyaguna (Ayurvedic Pharmacology) |
| **Task** | Publish research on novel formulations; help students understand IP for their innovations |
| **Goal** | Prior-art search against TKDL + AFI; understand patentability of modifications to classical formulations |
| **Frustration** | "TKDL is for patent examiners, not for researchers like me. I can't directly search it to check if my formulation modification is novel." |
| **Desired Outcome** | Search tool that tells her whether a formulation (or close variant) exists in the codified corpus, with source text citation |

---

## 4. Jobs-to-Be-Done (JTBD)

| # | Job Statement | Current Solution | Satisfaction |
|---|---|---|---|
| J1 | "Help me classify my Ayurvedic product so I know which regulatory pathway and IP instruments apply" | Hire a regulatory consultant (₹50K-2L) | Low — expensive, slow, often conflicting opinions |
| J2 | "Tell me which IP protection options are available for my specific formulation, citing the relevant law" | Hire an IP attorney (₹1-5L) | Low — Ayurveda-specific expertise is rare |
| J3 | "Check whether my formulation already exists in TKDL, AFI, or API before I invest in IP filing" | No self-service option; TKDL access restricted to patent offices | Very Low — inaccessible |
| J4 | "Give me a clear answer that distinguishes Indian law from international obligations" | Manual research across multiple portals | Very Low — error-prone, time-consuming |
| J5 | "Answer my IP question in Hindi so I can understand it without translation" | No existing tool does this for AYUSH IP | Zero — unserved |
| J6 | "Show me the exact source (Act, section, rule, monograph) for every claim you make" | Manual verification of any AI-generated answer | Very Low — high effort to verify |
| J7 | "Guide me step-by-step through the filing process for the IP instrument I need" | Scattered information across CGPDTM, AYUSH, NBA portals | Low — fragmented, incomplete |

---

## 5. Quantified Impact

### 5.1 Direct Impact

| Metric | Current State | Target State (12 months post-launch) |
|---|---|---|
| Time to understand IP options for a new product | 3-6 months | < 1 hour (self-service) |
| Cost of initial IP consultation | ₹50,000 - 5,00,000 | ₹0 (free public tool) |
| Erroneous patent applications (TKDL objection rate) | ~60% | < 25% (pre-filing check) |
| IP awareness among AYUSH MSMEs | < 5% have formal IP | Target 20% adoption in pilot states |
| Ministry query resolution time | 3-5 working days | < 5 minutes (with human review) |

### 5.2 Strategic Impact

- **Bio-piracy prevention:** Proactive prior-art visibility reduces erroneous foreign patents on Indian TK.
- **MSME empowerment:** Democratises access to IP guidance previously reserved for well-funded companies.
- **Policy consistency:** Standardised, cited answers reduce inter-officer interpretation variance within the Ministry.
- **India's negotiating position at WIPO IGC:** A working, deployed TK-protection tool strengthens India's leadership on TK/GR/TCE negotiations.

---

## 6. Constraints

### 6.1 Hard Constraints

| # | Constraint | Reason |
|---|---|---|
| C1 | Must cite sources for every substantive claim | Legal/regulatory guidance without citation is dangerous and unacceptable for a government tool |
| C2 | Must maintain strict jurisdiction separation (India vs. International) | Conflated answers give legally wrong guidance |
| C3 | Must support at least Hindi + English at MVP | 65%+ target users are Hindi-primary |
| C4 | Must not hallucinate legal provisions | Zero tolerance — one wrong section number destroys trust |
| C5 | Must handle product classification before IP advice | IP advice without classification is meaningless |
| C6 | Must be accessible on mobile browsers | MSME users primarily on smartphones |
| C7 | Deadline: 20 September 2026 (SIH) | Hackathon timeline constrains MVP scope |

### 6.2 Soft Constraints (Desirable)

| # | Constraint | Priority |
|---|---|---|
| S1 | Support 5+ scheduled languages beyond Hindi | Phase 2 |
| S2 | Offline capability for low-connectivity areas | Phase 3 |
| S3 | Integration with IPO e-filing portal | Phase 3 |
| S4 | Voice input/output for accessibility | Phase 2 |
| S5 | Knowledge graph for multi-hop reasoning | Phase 2 |

---

## 7. Scope Boundaries

### 7.1 In Scope (MVP)

- [x] Multilingual Q&A (Hindi + English) with source citations
- [x] Jurisdiction switch (India / International)
- [x] Product classification assistant (6 categories)
- [x] RAG over curated corpus (statutes, rules, pharmacopoeia, treaties)
- [x] Prior-art check against AFI/API formulation database
- [x] Step-by-step IP filing guidance
- [x] Web-based responsive UI
- [x] Confidence scoring and "I don't know" escalation

### 7.2 Out of Scope (MVP)

- [ ] Direct e-filing integration with IPO/CGPDTM portals
- [ ] Full TKDL database integration (requires CSIR MoU — deferred)
- [ ] Automated legal document drafting (patent specifications, TM applications)
- [ ] Real-time gazette monitoring for amendments
- [ ] Voice interface
- [ ] Case-law predictive analytics
- [ ] Offline mode

---

## 8. Problem Validation Checklist

| # | Validation Question | Status | Evidence |
|---|---|---|---|
| 1 | Is this a real problem or a constructed one? | ✅ Real | Ministry of Ayush has published this as an official SIH 2026 PS; TKDL bio-piracy cases are documented |
| 2 | Do users currently pay to solve this? | ✅ Yes | ₹50K-5L for IP consultations; regulatory compliance costs |
| 3 | Is the existing solution "good enough"? | ❌ No | No unified tool exists; manual multi-portal research is the current state |
| 4 | Is the user base large enough? | ✅ Yes | 9,000+ registered AYUSH manufacturers + practitioners + researchers + startups |
| 5 | Can this be solved with technology? | ✅ Yes | RAG + knowledge graphs + NLP are mature enough for domain-specific Q&A with citations |
| 6 | Is the timing right? | ✅ Yes | India Digital India push + AYUSH export growth + WIPO TK negotiations = policy tailwind |
| 7 | Is there a champion/sponsor? | ✅ Yes | Ministry of Ayush is the problem-statement owner |

---

*This document defines what we are solving and for whom. For how we solve it, see [solution.md](file:///E:/Projects/Active/IP-SAKTI-1/documents/solution.md).*
