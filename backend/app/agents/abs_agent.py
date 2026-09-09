from typing import List
from backend.app.schemas.abs import ABSAssessmentInput, ABSAssessmentResult

class ABSComplianceAgent:
    """
    Evaluates Access and Benefit Sharing (ABS) legal obligations under:
    - Biological Diversity Act, 2002 & Biological Diversity (Amendment) Act, 2023
    - ABS Guidelines (2014) & National Biodiversity Authority (NBA) regulations
    - Nagoya Protocol on ABS
    """

    @staticmethod
    def assess(data: ABSAssessmentInput) -> ABSAssessmentResult:
        is_foreign = "foreign" in data.user_entity_type.lower() or "nri" in data.user_entity_type.lower()
        is_seeking_ipr = data.is_seeking_ipr
        is_ntc = data.is_normally_traded_commodity
        is_vaid = data.is_local_vaid_or_hakim
        is_export = data.is_export_involved
        bio_resources = data.biological_resources or ["Indian Botanical Resource"]

        nba_required = False
        sbb_required = False
        risk_level = "Low"
        forms: List[str] = []
        sections: List[str] = []
        exemptions: List[str] = []

        if is_vaid:
            exemptions.append("Section 7 Exemption: Registered AYUSH vaids, hakims, and local traditional practitioners are exempt from prior intimation under 2023 Amendment.")
            risk_level = "Low"
            benefit_sharing = "0% (Statutory Exemption for Traditional Practitioners)"
            authority = "State Biodiversity Board (SBB) - Exempted Status"
            roadmap = [
                "Maintain local clinical practice records and practitioner registration.",
                "Ensure biological resources are sourced for direct local patient care, not large-scale industrial commercialization."
            ]
        elif is_foreign:
            nba_required = True
            risk_level = "Critical"
            forms.append("Form I (Application for access to biological resources by foreign entities under Section 3/19)")
            sections.extend(["Section 3", "Section 19", "Section 21", "Section 55"])
            authority = "National Biodiversity Authority (NBA, Chennai)"
            benefit_sharing = "0.1% to 0.5% of ex-factory sale price or upfront fee as negotiated with NBA under Mutually Agreed Terms (MAT)."
            roadmap = [
                "Submit NBA Form I prior to procuring, transporting, or conducting research on Indian biological resources.",
                "Execute Mutually Agreed Terms (MAT) with the National Biodiversity Authority.",
                "Consult local Biodiversity Management Committees (BMCs) via NBA for Prior Informed Consent (PIC).",
                "Ensure benefit-sharing remittance prior to commercial distribution."
            ]
        elif is_seeking_ipr:
            nba_required = True
            sbb_required = True
            risk_level = "High"
            forms.append("Form III (Application for seeking prior approval of NBA for applying for IPR under Section 6)")
            forms.append("SBB Form A (State Biodiversity Board Intimation)")
            sections.extend(["Section 6(1)", "Section 10(4)(d)(ii) of Patents Act", "Section 20"])
            authority = "National Biodiversity Authority (NBA) & Patent Office (CGPDTM)"
            benefit_sharing = "0.2% to 0.8% on commercialization or 2% to 5% on royalty/licensing fee."
            roadmap = [
                "Disclose full source and geographical origin of biological resources in Patent Specification as mandated by Section 10(4)(d)(ii).",
                "Submit NBA Form III to obtain statutory clearance before the grant of the patent.",
                "Intimate the concerned State Biodiversity Board (SBB) where the resources are cultivated/collected.",
                "Provide NBA approval certificate to the Patent Examiner during first examination response (FER)."
            ]
        elif is_ntc:
            exemptions.append("Section 40 NTC Exemption: Biological resources listed on the Central Government Normally Traded Commodities notification are exempt when traded strictly as agricultural commodities.")
            risk_level = "Low"
            benefit_sharing = "Exempt under Section 40 (only if raw commodity is traded without patented or proprietary bio-utilization)."
            authority = "National Biodiversity Authority / SBB"
            roadmap = [
                "Verify that all raw ingredients exist verbatim on the notified Section 40 NTC list.",
                "Ensure no novel biotechnology, gene editing, or patent claims are asserted over the raw resource."
            ]
        else:
            sbb_required = True
            risk_level = "Moderate"
            forms.append("SBB Form A / Form 1 (Prior Intimation to State Biodiversity Board for Commercial Utilization under Section 7)")
            sections.extend(["Section 7", "Section 23", "Section 24"])
            authority = "State Biodiversity Board (SBB) of the respective sourcing state"
            benefit_sharing = "0.1% to 0.5% of annual gross ex-factory sales of the manufactured Ayurvedic product."
            roadmap = [
                "File prior intimation with the State Biodiversity Board in the state where the manufacturing plant or herb collection takes place.",
                "Execute benefit-sharing agreement with SBB as per ABS Guidelines 2014 / 2024 Rules.",
                "Maintain traceable purchase vouchers showing sustainable sourcing from registered local cultivators or forest cooperatives."
            ]

        if is_export:
            forms.append("Export Inspection Agency Clearance & NBA Form B (if biological material is exported out of India for research)")
            roadmap.append("Comply with International Nagoya Protocol standards and verify target country ABS checkpoint declarations.")

        docs_to_verify = [
            "Raw material purchase invoices and vendor origin certificates",
            "Traceability log indicating state, district, and Gram Panchayat of biological harvest",
            "Herb authentication certificate / Pharmacopoeial monograph test report",
            "AYUSH manufacturing license (Form 25-D / FSSAI License)"
        ]

        return ABSAssessmentResult(
            biological_resource_status=f"Identified {len(bio_resources)} biological resource(s): {', '.join(bio_resources)}",
            jurisdiction_authority=authority,
            risk_level=risk_level,
            nba_approval_required=nba_required,
            sbb_intimation_required=sbb_required,
            benefit_sharing_obligation=benefit_sharing,
            applicable_forms=forms,
            applicable_statutory_sections=sections,
            exemptions_identified=exemptions if exemptions else ["No standard exemption identified; full statutory compliance required."],
            documents_to_verify=docs_to_verify,
            step_by_step_compliance_roadmap=roadmap
        )

abs_agent = ABSComplianceAgent()
