"""
Authoritative Seed Corpus for IP-SAKTI Sahayak
Contains verified statutory provisions, official rules, guidelines, and international treaties.
Every entry contains authoritative citations, source URLs, effective dates, and authority rankings.
"""

AUTHORITATIVE_SOURCES = [
    {
        "source_id": "IN_PATENTS_ACT_1970",
        "name": "The Patents Act, 1970 (as amended)",
        "authority": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM), DPIIT",
        "authority_rank": 1,
        "jurisdiction": "India",
        "domain": "Patent",
        "source_type": "Act",
        "source_url": "https://ipindia.gov.in/patents.htm",
        "version_tag": "2005_amendment",
        "effective_from": "1972-04-20",
        "chunks": [
            {
                "section_title": "Section 3(p) - Inventions not patentable (Traditional Knowledge)",
                "provision_ref": "Section 3(p)",
                "authority": "CGPDTM, Ministry of Commerce and Industry",
                "authority_score": 1.0,
                "content": "Under Section 3(p) of the Patents Act, 1970: An invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not an invention within the meaning of this Act and cannot be patented in India. Merely combining known Ayurvedic herbs (such as Ashwagandha and Turmeric) without demonstrating an unexpected synergistic technical effect beyond the sum of their individual known properties will result in statutory refusal under Section 3(p)."
            },
            {
                "section_title": "Section 3(d) - Incremental Innovations and Derivatives",
                "provision_ref": "Section 3(d)",
                "authority": "CGPDTM, Ministry of Commerce and Industry",
                "authority_score": 1.0,
                "content": "Section 3(d) of the Patents Act, 1970 provides that the mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance, or the mere discovery of any new property or new use for a known substance, or of the mere use of a known process, machine or apparatus unless such known process results in a new product or employs at least one new reactant, is not patentable. In herbal formulations, extraction methods or new dosage delivery forms must establish significantly enhanced therapeutic efficacy over the known herbal raw substance."
            },
            {
                "section_title": "Section 3(j) - Plants, Animals and Biological Processes",
                "provision_ref": "Section 3(j)",
                "authority": "CGPDTM, Ministry of Commerce and Industry",
                "authority_score": 1.0,
                "content": "Section 3(j) of the Patents Act, 1970 excludes plants and animals in whole or any part thereof other than micro-organisms, but including seeds, varieties and species and essentially biological processes for production or propagation of plants and animals from patentability. Naturally occurring Ayurvedic medicinal plants or unisolated parts cannot be patented as products."
            },
            {
                "section_title": "Section 10(4)(d)(ii) - Mandatory Disclosure of Biological Resource Origin",
                "provision_ref": "Section 10(4)(d)(ii)",
                "authority": "CGPDTM, Ministry of Commerce and Industry",
                "authority_score": 1.0,
                "content": "Under Section 10(4)(d)(ii) of the Patents Act, 1970, every complete specification must disclose the source and geographical origin of the biological material specified in the specification when used in an invention. If the biological resource is obtained from India, prior approval of the National Biodiversity Authority (NBA) under Section 6 of the Biological Diversity Act, 2002 must be obtained before the grant of the patent."
            },
            {
                "section_title": "Section 25(1)(k) - Grounds for Opposition based on Anticipation by Traditional Knowledge",
                "provision_ref": "Section 25(1)(k)",
                "authority": "CGPDTM, Ministry of Commerce and Industry",
                "authority_score": 1.0,
                "content": "Section 25(1)(k) allows any person to oppose a patent application on the ground that the complete specification does not disclose or wrongly mentions the source or geographical origin of biological material used for the invention, or that the invention was anticipated having regard to knowledge, oral or otherwise, available within any local or indigenous community in India or elsewhere."
            }
        ]
    },
    {
        "source_id": "IN_BD_ACT_2002_2023",
        "name": "The Biological Diversity Act, 2002 & Amendment Act, 2023",
        "authority": "National Biodiversity Authority (NBA) & Ministry of Environment, Forest and Climate Change (MoEFCC)",
        "authority_rank": 1,
        "jurisdiction": "India",
        "domain": "ABS",
        "source_type": "Act",
        "source_url": "http://nbaindia.org/",
        "version_tag": "2023_amendment",
        "effective_from": "2003-02-05",
        "chunks": [
            {
                "section_title": "Section 3 - Certain Persons not to undertake Biodiversity-related activities without NBA approval",
                "provision_ref": "Section 3",
                "authority": "National Biodiversity Authority (NBA)",
                "authority_score": 1.0,
                "content": "Section 3 of the Biological Diversity Act stipulates that non-Indian citizens, non-residents, foreign entities, or Indian entities having foreign shareholding or management participation (as amended in 2023) must obtain prior approval of the National Biodiversity Authority before obtaining any biological resource occurring in India or knowledge associated thereto for research or commercial utilization or bio-survey and bio-utilization."
            },
            {
                "section_title": "Section 6 - Application for Intellectual Property Rights & NBA Approval",
                "provision_ref": "Section 6",
                "authority": "National Biodiversity Authority (NBA)",
                "authority_score": 1.0,
                "content": "Under Section 6(1) of the Biological Diversity Act, no person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the prior approval of the National Biodiversity Authority before the grant of such IPR (or at the time of patent application for foreign applicants). For Indian applicants, under the 2023 Amendment, intimation/approval processes with NBA/SBB must be completed before patent grant."
            },
            {
                "section_title": "Section 7 - Prior Intimation to State Biodiversity Board (SBB) for Indian Entities",
                "provision_ref": "Section 7",
                "authority": "State Biodiversity Boards (SBB)",
                "authority_score": 1.0,
                "content": "Section 7 requires Indian citizens and Indian body corporates to give prior intimation to the concerned State Biodiversity Board (SBB) before obtaining any biological resource for commercial utilization. However, under the 2023 Amendment, registered AYUSH practitioners (vaids, hakims) and local communities cultivating or collecting biological resources are specifically exempted from prior intimation and benefit sharing obligations."
            },
            {
                "section_title": "Section 40 - Exemption for Normally Traded Commodities (NTC)",
                "provision_ref": "Section 40",
                "authority": "MoEFCC & NBA",
                "authority_score": 1.0,
                "content": "Section 40 empowers the Central Government to exempt certain biological resources normally traded as commodities (NTC list) from the provisions of the Biological Diversity Act. However, this exemption applies strictly when the item is traded as an agricultural commodity in raw form, and does NOT exempt an entity from obtaining approval if the resource is used as raw material for patented inventions or biotechnology research."
            },
            {
                "section_title": "ABS Guidelines - Benefit Sharing Formula & Percentages",
                "provision_ref": "ABS Guidelines 2014 & Rules 2024",
                "authority": "National Biodiversity Authority (NBA)",
                "authority_score": 2,
                "content": "Under the Access and Benefit Sharing (ABS) Guidelines, commercial manufacturers of Ayurvedic products utilizing biological resources sourced from India are required to share monetary benefits, typically ranging from 0.1% to 0.5% of the ex-factory sale price (or graded percentages based on turnover), payable to the National Biodiversity Authority or concerned State Biodiversity Board for community development and conservation."
            }
        ]
    },
    {
        "source_id": "IN_DRUGS_COSMETICS_ACT_1940",
        "name": "Drugs and Cosmetics Act, 1940 & Rules, 1945 (Chapter IV-A: ASU Drugs)",
        "authority": "Ministry of AYUSH & Central Drugs Standard Control Organisation (CDSCO)",
        "authority_rank": 1,
        "jurisdiction": "India",
        "domain": "Regulatory",
        "source_type": "Act and Rules",
        "source_url": "https://ayush.gov.in/",
        "version_tag": "2023_consolidated",
        "effective_from": "1940-04-10",
        "chunks": [
            {
                "section_title": "Section 3(a) - Definition of Ayurvedic, Siddha or Unani (ASU) Drug",
                "provision_ref": "Section 3(a)",
                "authority": "Ministry of AYUSH",
                "authority_score": 1.0,
                "content": "Section 3(a) defines an 'Ayurvedic, Siddha or Unani drug' as including all medicines intended for internal or external use for or in the diagnosis, treatment, mitigation or prevention of disease or disorder in human beings or animals, and manufactured exclusively in accordance with the formulae described in the authoritative books of Ayurvedic, Siddha and Unani systems specified in the First Schedule (e.g. Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Sharangadhara Samhita, Ayurvedic Formulary of India)."
            },
            {
                "section_title": "Rule 158B - Licensing Requirements for Classical vs Patent or Proprietary ASU Medicines",
                "provision_ref": "Rule 158B",
                "authority": "Ministry of AYUSH & State Licensing Authorities",
                "authority_score": 2,
                "content": "Rule 158B of the Drugs and Cosmetics Rules, 1945 sets out proof of effectiveness and licensing requirements: (1) Classical Ayurvedic Medicines: Formulations strictly adhering to First Schedule authoritative texts require no clinical trial data; submission of classical textual citations and safety compliance is sufficient. (2) Patent or Proprietary Ayurvedic Medicines: Formulations containing ingredients mentioned in authoritative books but in novel ratios, novel dosage forms, or modified combinations require safety studies and published literature proof or pilot clinical trials to obtain a manufacturing license from the State Licensing Authority."
            },
            {
                "section_title": "Schedule T - Good Manufacturing Practices (GMP) for ASU Drugs",
                "provision_ref": "Schedule T",
                "authority": "Ministry of AYUSH",
                "authority_score": 2,
                "content": "Schedule T mandates Good Manufacturing Practices (GMP) for all licensed Ayurvedic, Siddha, and Unani manufacturing facilities in India. It prescribes minimum space, hygienic conditions, standard operating procedures, quality control laboratories, batch testing for heavy metals (Lead, Cadmium, Mercury, Arsenic), pesticide residues, microbial contamination, and authentic raw herb batch records."
            },
            {
                "section_title": "Rule 170 - Prohibition of Misleading Advertisements for ASU Drugs",
                "provision_ref": "Rule 170",
                "authority": "Ministry of AYUSH",
                "authority_score": 2,
                "content": "Rule 170 of the Drugs and Cosmetics Rules prohibits direct-to-consumer advertising of Ayurvedic, Siddha, and Unani drugs without prior unique identification number/approval from the State Licensing Authority. Furthermore, the Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954 strictly prohibits claims to cure specified disorders including cancer, diabetes, hypertension, and sexual performance."
            }
        ]
    },
    {
        "source_id": "IN_FSSAI_AYURVEDA_AAHAR_2022",
        "name": "Food Safety and Standards (Ayurveda Aahar) Regulations, 2022",
        "authority": "Food Safety and Standards Authority of India (FSSAI) & Ministry of AYUSH",
        "authority_rank": 3,
        "jurisdiction": "India",
        "domain": "Regulatory",
        "source_type": "Regulation",
        "source_url": "https://fssai.gov.in/",
        "version_tag": "2022_gazette",
        "effective_from": "2022-05-05",
        "chunks": [
            {
                "section_title": "Ayurveda Aahar Scope and Definition",
                "provision_ref": "Regulation 2 & 3",
                "authority": "FSSAI & Ministry of AYUSH",
                "authority_score": 0.95,
                "content": "Food Safety and Standards (Ayurveda Aahar) Regulations, 2022 govern food prepared in accordance with recipes or processes and principles described in authoritative Ayurvedic books listed in Schedule A. Ayurveda Aahar covers food for physiological wellness, dietary health, and Rasayana support. It strictly EXCLUDES products intended to treat or cure acute medical diseases or synthetic vitamins/minerals."
            },
            {
                "section_title": "Ayurveda Aahar Labeling, Logo and Health Claims",
                "provision_ref": "Regulation 5 & 6",
                "authority": "FSSAI",
                "authority_score": 0.95,
                "content": "Every package of Ayurveda Aahar must prominently display the official 'Ayurveda Aahar' logo alongside the FSSAI license number. Labels must specify: 'ONLY FOR DIETARY PURPOSES AND NOT FOR MEDICINAL USE', recommended duration of usage, target physiological dosha balance, and warning against exceeding daily recommended allowance. Disease treatment or curative therapeutic claims are strictly prohibited under Ayurveda Aahar regulations."
            }
        ]
    },
    {
        "source_id": "IN_TRADEMARKS_GI_ACTS",
        "name": "Trade Marks Act, 1999 & Geographical Indications of Goods Act, 1999",
        "authority": "CGPDTM & Geographical Indications Registry, Chennai",
        "authority_rank": 1,
        "jurisdiction": "India",
        "domain": "Trademark / GI",
        "source_type": "Act",
        "source_url": "https://ipindia.gov.in/",
        "version_tag": "1999_consolidated",
        "effective_from": "2003-09-15",
        "chunks": [
            {
                "section_title": "Trademark Protection for Ayurvedic Brands (Class 5 vs Class 30/32)",
                "provision_ref": "Nice Classification Class 5, 30, 32",
                "authority": "Trade Marks Registry, CGPDTM",
                "authority_score": 1.0,
                "content": "Ayurvedic products are classified under Nice Classification: Class 5 covers medicinal Ayurvedic formulations, pharmaceutical preparations, and herbal medicaments. Class 30 covers herbal infusions, dietary spices, and food items. Class 32 covers non-alcoholic herbal health beverages. Generic Ayurvedic or Sanskrit names (e.g., 'Triphala', 'Ashwagandharishta', 'Chyawanprash') cannot be registered as trademarks individually because they are descriptive public domain terms; distinct brand prefixes, coined names, and composite logos can be trademarked."
            },
            {
                "section_title": "Geographical Indications for Region-Specific Ayurvedic Heritage",
                "provision_ref": "GI Act 1999 Section 8 & 11",
                "authority": "GI Registry, Chennai",
                "authority_score": 1.0,
                "content": "Under the Geographical Indications of Goods (Registration and Protection) Act, 1999, registered GI tags protect region-specific Ayurvedic products and medicinal plants (e.g. Navara Rice, Malabar Pepper, Alleppey Green Cardamom, Kangra Tea). Individual manufacturers cannot monopolize a GI tag as a private patent or trademark, but authorized producers within the geographical territory can apply as registered users for certified provenance."
            }
        ]
    },
    {
        "source_id": "INTL_WIPO_GRATK_2024",
        "name": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024)",
        "authority": "World Intellectual Property Organization (WIPO)",
        "authority_rank": 5,
        "jurisdiction": "International",
        "domain": "International",
        "source_type": "Treaty",
        "source_url": "https://www.wipo.int/treaties/en/ip/gratk/",
        "version_tag": "2024_diplomatic_conference",
        "effective_from": "2024-05-24",
        "chunks": [
            {
                "section_title": "Mandatory Patent Disclosure Requirement for Genetic Resources & Traditional Knowledge",
                "provision_ref": "Article 3 (WIPO GRATK Treaty)",
                "authority": "WIPO",
                "authority_score": 0.95,
                "content": "Adopted by WIPO Member States in Geneva in May 2024, the Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge establishes a historic global requirement: where a claimed invention in a patent application is based on genetic resources or traditional knowledge associated with genetic resources, patent applicants across contracting countries MUST disclose the country of origin or indigenous/local community source in their international and national patent applications."
            },
            {
                "section_title": "Information Systems and TK Databases for Prior Art Searches",
                "provision_ref": "Article 6 & 7 (WIPO GRATK Treaty)",
                "authority": "WIPO",
                "authority_score": 0.95,
                "content": "The WIPO GRATK Treaty encourages contracting parties to establish traditional knowledge databases and information systems (analogous to India's TKDL - Traditional Knowledge Digital Library) accessible to patent examiners globally to prevent wrongful patent grants on existing public domain traditional knowledge."
            }
        ]
    },
    {
        "source_id": "INTL_NAGOYA_PROTOCOL_CBD",
        "name": "Nagoya Protocol on Access to Genetic Resources and the Fair and Equitable Sharing of Benefits",
        "authority": "Convention on Biological Diversity (CBD) Secretariat",
        "authority_rank": 5,
        "jurisdiction": "International",
        "domain": "ABS / International",
        "source_type": "Treaty",
        "source_url": "https://www.cbd.int/abs/",
        "version_tag": "2010_nagoya",
        "effective_from": "2014-10-12",
        "chunks": [
            {
                "section_title": "Prior Informed Consent (PIC) and Mutually Agreed Terms (MAT)",
                "provision_ref": "Article 5 & 6 (Nagoya Protocol)",
                "authority": "CBD Secretariat",
                "authority_score": 0.95,
                "content": "The Nagoya Protocol establishes international legal obligations for the fair and equitable sharing of benefits arising from the utilization of genetic resources. Any enterprise or research institution seeking access to biological resources or traditional knowledge in a provider country must obtain Prior Informed Consent (PIC) from national authorities and establish Mutually Agreed Terms (MAT) governing commercial benefit sharing."
            }
        ]
    },
    {
        "source_id": "US_FDA_DSHEA_EXPORT",
        "name": "US FDA Dietary Supplement Health and Education Act (DSHEA 1994) & 21 CFR 111",
        "authority": "United States Food and Drug Administration (US FDA)",
        "authority_rank": 6,
        "jurisdiction": "USA",
        "domain": "Export",
        "source_type": "Regulation",
        "source_url": "https://www.fda.gov/food/dietary-supplements",
        "version_tag": "21_CFR_Part_111",
        "effective_from": "1994-10-25",
        "chunks": [
            {
                "section_title": "US Market Entry for Ayurvedic Botanicals: Dietary Supplements vs Drugs",
                "provision_ref": "21 U.S.C. 321(ff) & 21 CFR Part 111",
                "authority": "US FDA",
                "authority_score": 0.90,
                "content": "In the United States, Ayurvedic formulations are generally regulated as 'Dietary Supplements' under DSHEA (1994), not as prescription/OTC drugs. (1) Therapeutic disease claims (e.g. 'cures arthritis', 'treats diabetes') are strictly unlawful without FDA drug approval (NDA/IND) and will trigger FDA Warning Letters and import detentions. (2) Structure/Function claims (e.g., 'supports joint mobility', 'promotes vitality') are permissible with mandatory FDA disclaimer: 'These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.' (3) Mandatory compliance with 21 CFR 111 cGMP (current Good Manufacturing Practices) for dietary supplements, including heavy metal testing, identity testing for raw botanicals, and facility registration under FSMA."
            },
            {
                "section_title": "California Proposition 65 Heavy Metal Thresholds for Ayurvedic Exports",
                "provision_ref": "California Health and Safety Code Section 25249.6",
                "authority": "OEHHA (California EPA)",
                "authority_score": 0.90,
                "content": "Exporters of Ayurvedic products to California must comply with Safe Drinking Water and Toxic Enforcement Act of 1986 (Proposition 65). Lead limits are extremely stringent (Maximum Allowable Dose Level: 0.5 mcg/day). Classical Ayurvedic formulations containing Rasaushadhis (processed heavy metals/bhasmas) face severe litigation risks and import alerts under Prop 65 unless certified safe and accompanied by clear warnings."
            }
        ]
    },
    {
        "source_id": "EU_THMPD_2004",
        "name": "EU Traditional Herbal Medicinal Products Directive (Directive 2004/24/EC)",
        "authority": "European Medicines Agency (EMA) - Committee on Herbal Medicinal Products (HMPC)",
        "authority_rank": 6,
        "jurisdiction": "EU",
        "domain": "Export",
        "source_type": "Directive",
        "source_url": "https://www.ema.europa.eu/",
        "version_tag": "Directive_2004_24_EC",
        "effective_from": "2004-04-30",
        "chunks": [
            {
                "section_title": "EU Registration for Traditional Herbal Medicinal Products (THMPD)",
                "provision_ref": "Directive 2004/24/EC Article 16a",
                "authority": "European Medicines Agency (EMA)",
                "authority_score": 0.90,
                "content": "To sell Ayurvedic products in the European Union as traditional herbal medicines, applicants must utilize the Simplified Registration Procedure under Directive 2004/24/EC. Requirements: Proof of traditional medicinal use throughout a period of at least 30 years preceding the application, including at least 15 years within the European Community. If 15-year EU history is absent, products must either enter as food supplements (with restricted claims and strict botanical positive lists per member state) or undergo standard EMA marketing authorisation with full toxicological documentation."
            }
        ]
    }
]
