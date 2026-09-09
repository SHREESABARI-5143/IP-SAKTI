from typing import List, Dict, Any
from backend.app.schemas.ip_strategy import IPStrategyInput, IPStrategyResult, IPRoutesMatrix

class IPStrategyAgent:
    """
    Evaluates multi-dimensional IP protection routes for Ayurvedic products across:
    - Patents (Distinguishing Eligibility, Section 3(p) TK exclusions, Section 3(d), FTO)
    - Trademarks (Nice Classes 5, 30, 32; descriptive name disclaimers)
    - Geographical Indications (GI tag provenance)
    - Trade Secrets (Extraction ratios, manufacturing processes)
    - Industrial Designs (Novel bottles, applicator packaging)
    - Copyright (Proprietary educational brochures, software diagnostic tools)
    - Plant Variety Protection (PPV&FRA 2001 for novel cultivated herb varieties)
    """

    @staticmethod
    def evaluate(data: IPStrategyInput) -> IPStrategyResult:
        product_name = data.product_name
        is_classical = data.is_classical_formulation
        has_novelty = data.novel_extraction_or_synergy
        has_process = data.is_proprietary_process
        has_plant = data.uses_indigenous_crop_variety
        brand = data.brand_name or product_name

        routes: List[IPRoutesMatrix] = []

        # 1. Patent Analysis
        if is_classical and not has_novelty:
            patent_rel = "Generally Not Applicable"
            patent_details = "Formulation is based on classical Ayurvedic text recipes. Section 3(p) of the Patents Act, 1970 strictly bars patents on traditional knowledge and aggregations of known properties. The Patent Office and TKDL will issue statutory objections."
            patent_actions = [
                "Do NOT file a composition patent on the classical recipe; it will be rejected under Section 3(p).",
                "Focus IP investment on Trademark, Trade Dress, and Proprietary Branding."
            ]
        elif has_novelty or has_process:
            patent_rel = "Potentially Relevant (Requires Non-Obvious Synergy Proof)"
            patent_details = "Eligible for Patent consideration if you can prove unexpected synergistic therapeutic efficacy (overcoming Section 3(d)) or a novel technical extraction process. A mere admixture is barred under Section 3(e) and 3(p)."
            patent_actions = [
                "Conduct exhaustive Prior Art & TKDL search to confirm novelty beyond classical texts.",
                "Generate comparative in-vitro / clinical data proving synergy exceeding individual ingredients.",
                "Disclose biological origin and obtain NBA Form III approval under Section 6 of Biological Diversity Act."
            ]
        else:
            patent_rel = "Requires Professional Assessment"
            patent_details = "Need to establish whether modified ratio creates a non-obvious synergistic technical effect."
            patent_actions = [
                "Consult an IP facilitator to perform Freedom-to-Operate (FTO) and patentability search."
            ]

        routes.append(
            IPRoutesMatrix(
                route_name="Patent Protection",
                relevance_level=patent_rel,
                analysis_details=patent_details,
                statutory_basis="Indian Patents Act 1970 [Sections 3(p), 3(d), 3(e), 10(4)(d)(ii)]",
                action_items=patent_actions
            )
        )

        # 2. Trademark Strategy
        tm_rel = "Highly Relevant (Immediate Priority)"
        tm_details = f"Protecting the brand name '{brand}' under Nice Classification Class 5 (Medicines/Herbal) or Class 30 (Foods). Generic names like 'Triphala' or 'Churna' cannot be monopolized, but coined names and distinct logos are strongly protectable."
        routes.append(
            IPRoutesMatrix(
                route_name="Trademark & Brand Identity",
                relevance_level=tm_rel,
                analysis_details=tm_details,
                statutory_basis="Trade Marks Act, 1999 (Sections 9, 11 & Class 5/30/32)",
                action_items=[
                    f"Perform phonetic and similarity search on IP India Trade Marks Registry for '{brand}'.",
                    "File Form TM-A with distinct logo mark and word mark in Class 5 (and Class 30 if Ayurveda Aahar).",
                    "Avoid purely descriptive Sanskrit health terms in the mark to prevent Section 9 absolute grounds objections."
                ]
            )
        )

        # 3. Trade Secret
        ts_rel = "Highly Relevant (Zero Public Disclosure)"
        ts_details = "Proprietary manufacturing parameters, specific temperature curves, solvent ratios, and supplier supply chain details can be protected indefinitely as Trade Secrets without expiration or public disclosure."
        routes.append(
            IPRoutesMatrix(
                route_name="Trade Secrets & Confidential Know-How",
                relevance_level=ts_rel,
                analysis_details=ts_details,
                statutory_basis="Indian Contract Act, 1872 & Common Law Breach of Confidence",
                action_items=[
                    "Implement strict Non-Disclosure Agreements (NDAs) with manufacturing staff, contract labs, and CMOs.",
                    "Segment formulation process sheets so no single employee has end-to-end recipe visibility."
                ]
            )
        )

        # 4. Geographical Indication (GI)
        gi_rel = "Possibly Relevant (Territorial / Regional)" if any(h in "".join(data.ingredients).lower() for h in ["kerala", "kashmir", "assam", "malabar", "coorg"]) else "Generally Not Applicable"
        routes.append(
            IPRoutesMatrix(
                route_name="Geographical Indication (GI)",
                relevance_level=gi_rel,
                analysis_details="If using botanicals from certified GI regions (e.g. Navara Rice, Malabar Cardamom, Kangra Tea), producers can register as Authorised Users to command export premiums.",
                statutory_basis="Geographical Indications of Goods Act, 1999",
                action_items=[
                    "Check GI Registry for certified state heritage botanical list.",
                    "Apply as an Authorised User on Form GI-3 to use official GI logo on packaging."
                ]
            )
        )

        # 5. Plant Variety Protection
        pv_rel = "Highly Relevant" if has_plant else "Generally Not Applicable"
        routes.append(
            IPRoutesMatrix(
                route_name="Plant Variety Protection (PPV&FRA)",
                relevance_level=pv_rel,
                analysis_details="If your organization bred or developed an extant or novel medicinal plant variety with distinct, uniform, and stable (DUS) traits.",
                statutory_basis="Protection of Plant Varieties and Farmers' Rights Act, 2001",
                action_items=[
                    "Conduct DUS field testing across multiple agro-climatic zones.",
                    "File application with PPV&FR Authority in New Delhi."
                ]
            )
        )

        # Timelines & Costs
        timelines = [
            {"milestone": "Trademark Search & Filing (TM-A)", "timeline": "1-3 days", "estimated_official_fee": "Rs. 4,500 (Startup/MSME) / Rs. 9,000 (Others)"},
            {"milestone": "SBB Prior Intimation (ABS)", "timeline": "1-2 months", "estimated_official_fee": "Nominal application fee + 0.1-0.5% ex-factory ABS"},
            {"milestone": "Provisional Patent Application (if novel)", "timeline": "2-4 weeks", "estimated_official_fee": "Rs. 1,600 (Startup/Individual) / Rs. 8,000 (Others)"},
            {"milestone": "NBA Form III Approval (IPR clearance)", "timeline": "6-12 months", "estimated_official_fee": "Rs. 500 processing fee"}
        ]

        warnings = [
            "Never publicly publish research papers, youtube videos, or marketing pamphlets describing novel extraction methods prior to filing a patent application.",
            "Always maintain signed traceable provenance certificates for all botanical raw materials to prevent biodiversity penalties."
        ]

        return IPStrategyResult(
            product_name=product_name,
            overall_executive_summary=f"Comprehensive IP strategy for '{product_name}'. Primary focus is strong Trademark and Trade Dress protection, coupled with ABS compliance. Patent protection is viable only upon proving non-obvious synergistic efficacy beyond classical traditional knowledge.",
            routes=routes,
            patent_analysis={
                "eligibility": "Excluded under 3(p) unless synergistic technical leap is established.",
                "patentability_hurdle": "Overcoming Section 3(d) enhancement of efficacy requirement.",
                "fto_status": "Free to practice classical recipes; must avoid infringing active extraction patent claims.",
                "nba_mandate": "Section 6 approval required before patent grant."
            },
            trademark_strategy={
                "recommended_classes": ["Class 5 (Pharmaceutical/Herbal formulations)", "Class 30 (Health food/Dietary)", "Class 35 (Retail/E-commerce distribution)"],
                "coined_brand_advice": "Combine distinctive prefixes with non-descriptive suffixes."
            },
            gi_opportunities={
                "tag_opportunity": "Explore state-specific medicinal plant GI registers."
            },
            trade_secret_recommendations=[
                "Bind all AYUSH formulation consultants under 5-year post-termination restrictive covenants.",
                "Maintain encrypted cloud repositories for proprietary compounding batch records."
            ],
            timeline_and_cost_guidelines=timelines,
            risk_warnings=warnings
        )

ip_strategy_agent = IPStrategyAgent()
