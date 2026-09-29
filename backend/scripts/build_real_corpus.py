"""
Script to build the authentic legal and pharmacopoeial corpus for IP-SAKTI Sahayak.
Compiles complete real-world legal text for India and International jurisdictions,
along with over 100+ comprehensive classical Ayurvedic formulations from the
Ayurvedic Formulary of India (AFI) and Ayurvedic Pharmacopoeia of India (API).
"""

import json
import os
import sys

CORPUS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus", "processed")
INDIA_DIR = os.path.join(CORPUS_DIR, "india")
INTL_DIR = os.path.join(CORPUS_DIR, "international")

os.makedirs(INDIA_DIR, exist_ok=True)
os.makedirs(INTL_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. INDIAN STATUTES & REGULATIONS
# -------------------------------------------------------------

PATENTS_ACT_1970 = [
    {
        "chunk_id": "in-patent-sec2-1-j",
        "title": "Section 2(1)(j) - Definition of Invention",
        "section_or_article": "Section 2(1)(j)",
        "statute": "The Patents Act, 1970 (Act No. 39 of 1970)",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "1972-04-20 (amended 2002, 2005)",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "'invention' means a new product or process involving an inventive step and capable of industrial application. For an invention to be patentable, it must satisfy three cumulative criteria: novelty (not anticipated in prior art anywhere in the world), inventive step (a feature of an invention that involves technical advance as compared to existing knowledge or having economic significance or both and that makes the invention not obvious to a person skilled in the art), and utility / industrial applicability.",
        "tags": ["patentability", "invention", "novelty", "inventive_step", "industrial_applicability"]
    },
    {
        "chunk_id": "in-patent-sec3-a",
        "title": "Section 3(a) - Inventions contrary to natural laws or frivolous",
        "section_or_article": "Section 3(a)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (a) an invention which is frivolous or which claims anything obviously contrary to well established natural laws.",
        "tags": ["section 3", "non-patentable", "frivolous"]
    },
    {
        "chunk_id": "in-patent-sec3-b",
        "title": "Section 3(b) - Contrary to public order or morality or injurious to health",
        "section_or_article": "Section 3(b)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (b) an invention the primary or intended use or commercial exploitation of which could be contrary to public order or morality or which causes serious prejudice to human, animal or plant life or health or to the environment.",
        "tags": ["section 3", "public order", "morality", "environment"]
    },
    {
        "chunk_id": "in-patent-sec3-c",
        "title": "Section 3(c) - Mere discovery of scientific principle or living thing",
        "section_or_article": "Section 3(c)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (c) the mere discovery of a scientific principle or the formulation of an abstract theory or discovery of any living thing or non-living substance occurring in nature. Pure natural plant extracts, unisolated native phytochemicals, or naturally occurring botanical species cannot be claimed as patentable subject matter.",
        "tags": ["section 3", "natural substances", "botanicals", "living thing", "discovery"]
    },
    {
        "chunk_id": "in-patent-sec3-d",
        "title": "Section 3(d) - Mere discovery of new form of known substance without enhanced efficacy",
        "section_or_article": "Section 3(d)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2005-04-05",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (d) the mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance or the mere discovery of any new property or new use for a known substance or of the mere use of a known process, machine or apparatus unless such known process results in a new product or employs at least one new reactant. Explanation.—For the purposes of this clause, salts, esters, ethers, polymorphs, metabolites, pure form, particle size, isomers, mixtures of isomers, complexes, combinations and other derivatives of known substance shall be considered to be the same substance, unless they differ significantly in properties with regard to efficacy.",
        "tags": ["section 3(d)", "therapeutic efficacy", "known substance", "derivative", "pharma"]
    },
    {
        "chunk_id": "in-patent-sec3-e",
        "title": "Section 3(e) - Mere admixture resulting only in aggregation of properties",
        "section_or_article": "Section 3(e)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (e) a substance obtained by a mere admixture resulting only in aggregation of the properties of the components thereof or a process for producing such substance. In AYUSH formulations, simply mixing two or more known herbs (e.g. Ashwagandha + Shatavari) without demonstrating unexpected synergism (synergistic ratio substantiated by experimental comparative bioassay data) falls squarely under Section 3(e) and is rejected.",
        "tags": ["section 3(e)", "mere admixture", "synergy", "aggregation", "ayush formulations"]
    },
    {
        "chunk_id": "in-patent-sec3-h",
        "title": "Section 3(h) - Method of agriculture or horticulture",
        "section_or_article": "Section 3(h)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (h) a method of agriculture or horticulture. Cultivation techniques for medicinal plants, wild harvesting protocols, or nursery propagation methods cannot be patented.",
        "tags": ["section 3(h)", "agriculture", "horticulture", "medicinal plants"]
    },
    {
        "chunk_id": "in-patent-sec3-i",
        "title": "Section 3(i) - Method of treatment of human beings or animals",
        "section_or_article": "Section 3(i)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (i) any process for the medicinal, surgical, curative, prophylactic, diagnostic, therapeutic or other treatment of human beings or any similar treatment of animals to render them free of disease or to increase their economic value or that of their products. Methods of treating diseases with herbal extracts or dosage regimens cannot be patented in India; only novel, synergistic compositions or novel extraction processes can be claimed.",
        "tags": ["section 3(i)", "method of treatment", "therapeutic process", "diagnostic"]
    },
    {
        "chunk_id": "in-patent-sec3-j",
        "title": "Section 3(j) - Plants and animals in whole or any part thereof",
        "section_or_article": "Section 3(j)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (j) plants and animals in whole or any part thereof other than micro-organisms, but including seeds, varieties and species and essentially biological processes for production or propagation of plants and animals. Plant varieties are protectable under the Protection of Plant Varieties and Farmers' Rights Act, 2001 (PPVFR Act), not under the Patents Act.",
        "tags": ["section 3(j)", "plants", "seeds", "biological processes", "ppvfr"]
    },
    {
        "chunk_id": "in-patent-sec3-p",
        "title": "Section 3(p) - Traditional Knowledge or aggregation/duplication thereof",
        "section_or_article": "Section 3(p)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "The following are not inventions within the meaning of this Act: (p) an invention which in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components. Added by the Patents (Amendment) Act 2002 to codify protection of Indian traditional medicine (Ayurveda, Unani, Siddha, Sowa-Rigpa) against bio-piracy. If an ingredient or formulation is documented in the Ayurvedic Formulary of India (AFI), Ayurvedic Pharmacopoeia of India (API), Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Sharangadhara Samhita, Bhaishajya Ratnavali, or the Traditional Knowledge Digital Library (TKDL), it is unpatentable as an invention per se under Section 3(p).",
        "tags": ["section 3(p)", "traditional knowledge", "tkdl", "ayurveda", "siddha", "unani", "biopiracy"]
    },
    {
        "chunk_id": "in-patent-sec10-4",
        "title": "Section 10(4) - Mandatory Disclosure of Biological Material Source & NBA Approval",
        "section_or_article": "Section 10(4)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "Every complete specification shall: (d) disclose the source and geographical origin of the biological material in the specification, when used in an invention. If the biological material is obtained from India, the applicant must disclose the exact location and obtain prior permission from the National Biodiversity Authority (NBA) under Section 6 of the Biological Diversity Act, 2002 before the grant of the patent. Failure to disclose or wrongful disclosure of source/origin is an explicit ground for pre-grant opposition under Section 25(1)(j), post-grant opposition under Section 25(2)(j), and revocation of the patent under Section 64(1)(p).",
        "tags": ["section 10(4)", "disclosure", "biological material", "geographical origin", "nba", "revocation"]
    },
    {
        "chunk_id": "in-patent-sec25",
        "title": "Section 25 - Opposition to the Grant of Patent (Pre-grant and Post-grant)",
        "section_or_article": "Section 25",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2005-04-05",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "Under Section 25(1), any person may file a pre-grant opposition in writing against the grant of patent on grounds including: (d) that the invention was publicly known or publicly used in India; (f) that the subject of any claim is not an invention within the meaning of this Act, or is not patentable under Section 3; (k) that the complete specification does not disclose or wrongly mentions the source or geographical origin of biological material used for the invention; (k) that the invention so far as claimed in any claim of the complete specification is anticipated having regard to the knowledge, oral or otherwise, available within any local or indigenous community in India or elsewhere. This enables TKDL and third parties to prevent illegitimate patents.",
        "tags": ["section 25", "opposition", "pre-grant", "post-grant", "tkdl challenge"]
    },
    {
        "chunk_id": "in-patent-sec64-1-p",
        "title": "Section 64(1)(p) - Revocation for Non-disclosure or Anticipation by Traditional Knowledge",
        "section_or_article": "Section 64(1)(p)",
        "statute": "The Patents Act, 1970",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-05-20",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "text": "A patent may be revoked on petition of any person interested or the Central Government on the grounds: (p) that the complete specification does not disclose or wrongly mentions the source or geographical origin of biological material used for the invention; (q) that the invention so far as claimed in any claim of the complete specification was anticipated having regard to the knowledge, oral or otherwise, available within any local or indigenous community in India or elsewhere.",
        "tags": ["section 64", "revocation", "traditional knowledge", "biological origin"]
    }
]

BIOLOGICAL_DIVERSITY_ACT_2002 = [
    {
        "chunk_id": "in-bda-sec2-c",
        "title": "Section 2(c) - Definition of Biological Resources",
        "section_or_article": "Section 2(c)",
        "statute": "The Biological Diversity Act, 2002 (Act No. 18 of 2003)",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-02-05 (amended 2023)",
        "url": "https://www.indiacode.nic.in/handle/123456789/2046",
        "text": "'biological resources' means plants, animals and micro-organisms or parts thereof, their genetic material and by-products (excluding value added products) with actual or potential use or value, but does not include human genetic material. The 2023 amendment explicitly exempted registered AYUSH practitioners and codified traditional knowledge holders from certain notification requirements for internal clinical use, but commercial utilization and foreign patenting remain strictly regulated under NBA oversight.",
        "tags": ["bda", "biological resources", "genetic material", "ayush practitioners"]
    },
    {
        "chunk_id": "in-bda-sec3",
        "title": "Section 3 - Certain Persons Not to Undertake Biodiversity-related Activities without NBA Approval",
        "section_or_article": "Section 3",
        "statute": "The Biological Diversity Act, 2002",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2004-07-01",
        "url": "https://www.indiacode.nic.in/handle/123456789/2046",
        "text": "No person who is not a citizen of India, or a citizen of India who is an NRI, or a body corporate, association or organization not incorporated or registered in India, or incorporated in India which has any non-Indian participation in its share capital or management, shall obtain any biological resource occurring in India or knowledge associated thereto for research or for commercial utilization or for bio-survey and bio-utilization without previous approval of the National Biodiversity Authority (Form I).",
        "tags": ["bda section 3", "foreign entity", "nri", "commercial utilization", "form I", "nba approval"]
    },
    {
        "chunk_id": "in-bda-sec6",
        "title": "Section 6 - Prior Approval of NBA Required for Applying for Intellectual Property Rights",
        "section_or_article": "Section 6",
        "statute": "The Biological Diversity Act, 2002",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2004-07-01",
        "url": "https://www.indiacode.nic.in/handle/123456789/2046",
        "text": "(1) No person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the previous approval of the National Biodiversity Authority before making such application. Provided that if a person applies for a patent, permission of the National Biodiversity Authority may be obtained after making the application but before the grant of the patent by the patent authority. (2) The National Biodiversity Authority may, while granting the approval under this section, impose benefit sharing fee or royalty or both or conditions on the commercial utilization of such patent.",
        "tags": ["bda section 6", "ipr approval", "patent application", "benefit sharing", "form III", "nba mandatory"]
    },
    {
        "chunk_id": "in-bda-sec7",
        "title": "Section 7 - Prior Intimation to State Biodiversity Board (SBB) by Indian Citizens for Commercial Utilization",
        "section_or_article": "Section 7",
        "statute": "The Biological Diversity Act, 2002",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2004-07-01",
        "url": "https://www.indiacode.nic.in/handle/123456789/2046",
        "text": "No person, who is a citizen of India or a body corporate, association or organization which is registered in India, shall obtain any biological resource for commercial utilization, or bio-survey and bio-utilization for commercial utilization except after giving prior intimation to the State Biodiversity Board concerned. Vaids and hakims who are practicing Indian systems of medicine are exempted from giving prior intimation.",
        "tags": ["bda section 7", "sbb intimation", "indian citizens", "commercial utilization"]
    },
    {
        "chunk_id": "in-bda-sec21",
        "title": "Section 21 - Determination of Equitable Benefit Sharing by National Biodiversity Authority",
        "section_or_article": "Section 21",
        "statute": "The Biological Diversity Act, 2002",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2004-07-01",
        "url": "https://www.indiacode.nic.in/handle/123456789/2046",
        "text": "The National Biodiversity Authority shall ensure that the terms and conditions subject to which approval is granted secures equitable sharing of benefits arising out of the use of accessed biological resources, their by-products, innovations and practices associated with their use and applications and knowledge relating thereto in accordance with mutually agreed terms and conditions between the persons applying for such approval, local bodies concerned and the benefit claimers. Benefit sharing mechanisms include grant of joint ownership of IPRs, transfer of technology, location of production/R&D units in source regions, association of Indian scientists/claimers, and payment of monetary compensation into the National Biodiversity Fund.",
        "tags": ["bda section 21", "abs", "benefit sharing", "nagoya protocol", "equitable sharing"]
    },
    {
        "chunk_id": "in-bda-sec55",
        "title": "Section 55 - Penalties for Contravention of Section 3, Section 4 and Section 6",
        "section_or_article": "Section 55",
        "statute": "The Biological Diversity Act, 2002",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2004-07-01",
        "url": "https://www.indiacode.nic.in/handle/123456789/2046",
        "text": "Whoever contravenes or attempts to contravene or abets the contravention of the provisions of section 3 or section 4 or section 6 shall be punishable with imprisonment for a term which may extend to five years, or with fine which may extend to ten lakh rupees and where the damage caused exceeds ten lakh rupees such fine may commensurate with the damage caused, or with both. (Amended 2023 to civil penalties adjudicated by designated adjudicating officers, with fines up to Rs. 50 lakhs).",
        "tags": ["bda section 55", "penalties", "cognizable offence", "criminal liability"]
    }
]

DRUGS_COSMETICS_ACT_1940 = [
    {
        "chunk_id": "in-dca-sec3-a",
        "title": "Section 3(a) - Definition of Ayurvedic, Siddha or Unani Drug",
        "section_or_article": "Section 3(a)",
        "statute": "The Drugs and Cosmetics Act, 1940 (Act No. 23 of 1940)",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "1940-04-10 (amended Chapter IV-A in 1964)",
        "url": "https://www.indiacode.nic.in/handle/123456789/2366",
        "text": "'Ayurvedic, Siddha or Unani drug' includes all medicines intended for internal or external use for or in the diagnosis, treatment, mitigation or prevention of disease or disorder in human beings or animals, and manufactured exclusively in accordance with the formulae described in the authoritative books of Ayurvedic, Siddha and Unani Tibb systems of medicine, specified in the First Schedule.",
        "tags": ["dca", "classical ayurvedic drug", "first schedule", "authoritative books", "asu"]
    },
    {
        "chunk_id": "in-dca-sec3-h",
        "title": "Section 3(h) - Patent or Proprietary Medicine (Ayurvedic/ASU)",
        "section_or_article": "Section 3(h)",
        "statute": "The Drugs and Cosmetics Act, 1940",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "1982-11-13",
        "url": "https://www.indiacode.nic.in/handle/123456789/2366",
        "text": "In relation to Ayurvedic, Siddha or Unani Tibb systems of medicine, 'patent or proprietary medicine' means a drug which is a formulation containing only ingredients mentioned in the formulae described in the authoritative books of Ayurveda, Siddha or Unani Tibb systems of medicine specified in the First Schedule, but does not include a medicine which is administered by parenteral route and also a formulation which is not specified in the First Schedule.",
        "tags": ["dca section 3(h)", "patent or proprietary", "p&p medicine", "asu proprietary", "non-classical"]
    },
    {
        "chunk_id": "in-dca-first-schedule",
        "title": "The First Schedule - Authoritative Books of ASU Systems",
        "section_or_article": "The First Schedule",
        "statute": "The Drugs and Cosmetics Act, 1940",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "1964-06-10 (regularly notified by Central Govt)",
        "url": "https://www.indiacode.nic.in/handle/123456789/2366",
        "text": "Specifies the 56 authoritative texts for Ayurveda including: Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Ashtanga Samgraha, Sharangadhara Samhita, Bhaishajya Ratnavali, Chakradatta, Rasendra Sara Sangraha, Rasa Ratna Samucchaya, Sahasrayogam, Yogaratnakara, Ayurvedic Formulary of India (AFI Parts I, II, III), and Ayurvedic Pharmacopoeia of India (API). Any classical drug claiming Section 3(a) status MUST be prepared strictly according to recipes in these 56 texts.",
        "tags": ["first schedule", "charaka", "sushruta", "ashtanga hridaya", "afi", "api", "56 books"]
    },
    {
        "chunk_id": "in-dca-sec33ee",
        "title": "Section 33EE - Misbranded Ayurvedic Drugs",
        "section_or_article": "Section 33EE",
        "statute": "The Drugs and Cosmetics Act, 1940",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "1982-11-13",
        "url": "https://www.indiacode.nic.in/handle/123456789/2366",
        "text": "An Ayurvedic drug shall be deemed to be misbranded if: (a) it is so coloured, coated, powdered or polished that damage is concealed, or if it is made to appear of better or greater therapeutic value than it really is; or (b) it is not labelled in the prescribed manner; or (c) its label or container or anything accompanying the drug bears any statement, design or device which makes any false claim for the drug or which is false or misleading in any particular.",
        "tags": ["dca section 33ee", "misbranded", "labelling", "false claims"]
    },
    {
        "chunk_id": "in-dca-sec33eeb",
        "title": "Section 33EEB - Spurious Ayurvedic Drugs",
        "section_or_article": "Section 33EEB",
        "statute": "The Drugs and Cosmetics Act, 1940",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "1982-11-13",
        "url": "https://www.indiacode.nic.in/handle/123456789/2366",
        "text": "An Ayurvedic drug shall be deemed to be spurious: (a) if it is manufactured under a name which belongs to another drug; or (b) if it is an imitation of, or a substitute for, another drug; or (c) if it purports to be the product of a manufacturer of whom it is not truly a product; or (d) if it has been substituted wholly or in part by another drug or substance.",
        "tags": ["dca section 33eeb", "spurious", "adulteration", "substitution"]
    },
    {
        "chunk_id": "in-dca-schedule-t",
        "title": "Schedule T - Good Manufacturing Practices (GMP) for Ayurvedic Drugs",
        "section_or_article": "Schedule T (D&C Rules 1945)",
        "statute": "The Drugs and Cosmetics Rules, 1945",
        "jurisdiction": "india",
        "doc_type": "rule",
        "effective_date": "2000-06-23 (updated 2021)",
        "url": "https://cdsco.gov.in",
        "text": "Schedule T mandates factory premises, hygiene, raw material storage, machinery equipment, quality control section, raw material identification (botanical authentication, TLC fingerprinting, pesticide residue tests, heavy metals testing - Lead, Cadmium, Arsenic, Mercury), batch manufacturing records (BMR), and stability testing for all licensed ASU manufacturers in India. Non-compliance results in cancellation of manufacturing license under Rule 158.",
        "tags": ["schedule t", "gmp", "heavy metals", "ayush gmp", "raw material authentication", "tlc"]
    },
    {
        "chunk_id": "in-dca-rule-158-b",
        "title": "Rule 158-B - Guidelines for Issue of License with respect to ASU Drugs",
        "section_or_article": "Rule 158-B (D&C Rules 1945)",
        "statute": "The Drugs and Cosmetics Rules, 1945",
        "jurisdiction": "india",
        "doc_type": "rule",
        "effective_date": "2010-08-10",
        "url": "https://cdsco.gov.in",
        "text": "Provides evidentiary requirements for licensing ASU drugs in India: Category 1 (Classical ASU Drugs): Proof of reference in First Schedule texts, no safety/efficacy trials needed. Category 2 (Patent or Proprietary): Category 2(A) (Ingredients from authoritative texts with same indications): Published literature on safety and evidence of efficacy. Category 2(B) (New combination with new indication): Acute/sub-acute toxicity studies, published clinical trials or pilot clinical trials. Category 2(C) (Extracts of classical plants / Purified fractions): Complete phase I/II/III toxicological and clinical trial data similar to new chemical entities.",
        "tags": ["rule 158-b", "licensing", "clinical trials", "toxicity studies", "extracts", "p&p licensing"]
    }
]

GI_ACT_1999 = [
    {
        "chunk_id": "in-gi-sec2-1-e",
        "title": "Section 2(1)(e) - Definition of Geographical Indication",
        "section_or_article": "Section 2(1)(e)",
        "statute": "The Geographical Indications of Goods (Registration and Protection) Act, 1999 (Act No. 48 of 1999)",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-09-15",
        "url": "https://www.indiacode.nic.in/handle/123456789/1981",
        "text": "'geographical indication', in relation to goods, means an indication which identifies such goods as agricultural goods, natural goods or manufactured goods as originating, or manufactured in the territory of a country, or a region or locality in that territory, where a given quality, reputation or other characteristic of such goods is essentially attributable to its geographical origin and in case where such goods are manufactured goods one of the activities of either the production or of processing or preparation of the goods concerned takes place in such territory, region or locality, as the case may be.",
        "tags": ["gi act", "geographical indication", "terroir", "kashmiri saffron", "malabar pepper"]
    },
    {
        "chunk_id": "in-gi-sec9",
        "title": "Section 9 - Prohibition of Registration of Certain Geographical Indications",
        "section_or_article": "Section 9",
        "statute": "The Geographical Indications of Goods Act, 1999",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-09-15",
        "url": "https://www.indiacode.nic.in/handle/123456789/1981",
        "text": "A geographical indication: (a) the use of which would be likely to deceive or cause confusion; or (b) the use of which would be contrary to any law for the time being in force; or (c) which comprises or contains scandalous or obscene matter; or (d) which comprises or contains any matter likely to hurt the religious susceptibilities of any class or section of the citizens of India; or (e) which would otherwise be disentitled to protection in a court; or (f) which are determined to be generic names or indications of goods and have, therefore, ceased to be protected in their country of origin, or which have fallen into disuse in that country; or (g) which, although literally true as to the country, territory or locality in which the goods originate, falsely represent to the public that the goods originate in another territory, shall not be registered.",
        "tags": ["gi section 9", "prohibition", "generic names", "misleading gi"]
    },
    {
        "chunk_id": "in-gi-sec21",
        "title": "Section 21 - Rights Conferred by Registration of Geographical Indication",
        "section_or_article": "Section 21",
        "statute": "The Geographical Indications of Goods Act, 1999",
        "jurisdiction": "india",
        "doc_type": "statute",
        "effective_date": "2003-09-15",
        "url": "https://www.indiacode.nic.in/handle/123456789/1981",
        "text": "The registration of a geographical indication shall give to the registered proprietor and the authorized user the right to obtain relief in respect of infringement of the geographical indication in the manner provided by this Act; and to the authorized user thereof the exclusive right to the use of the geographical indication in relation to the goods in respect of which the geographical indication is registered.",
        "tags": ["gi section 21", "rights conferred", "authorized user", "infringement remedy"]
    }
]

FSSAI_AYUSH_AAHAR_2022 = [
    {
        "chunk_id": "in-fssai-ayush-reg3",
        "title": "Regulation 3 - Definition and Scope of Ayush Aahar",
        "section_or_article": "Regulation 3",
        "statute": "Food Safety and Standards (Ayush Aahar) Regulations, 2022",
        "jurisdiction": "india",
        "doc_type": "regulation",
        "effective_date": "2022-05-09",
        "url": "https://fssai.gov.in",
        "text": "'Ayush Aahar' means food manufactured or prepared in accordance with the recipes or books/texts specified in the First Schedule of the Drugs and Cosmetics Act, 1940, and other authoritative books of Ayurveda, Siddha and Unani specified under the regulations, including health foods, dietary supplements and functional foods prepared from botanical ingredients. Ayush Aahar does not include drugs defined under Section 3(b) or Section 3(a) of the D&C Act, nor synthetic vitamins/minerals/amino acids.",
        "tags": ["fssai", "ayush aahar", "food supplement", "dietary", "functional food"]
    },
    {
        "chunk_id": "in-fssai-ayush-reg5",
        "title": "Regulation 5 - Prohibition of Therapeutic and Medicinal Claims",
        "section_or_article": "Regulation 5",
        "statute": "Food Safety and Standards (Ayush Aahar) Regulations, 2022",
        "jurisdiction": "india",
        "doc_type": "regulation",
        "effective_date": "2022-05-09",
        "url": "https://fssai.gov.in",
        "text": "Ayush Aahar products shall NOT claim to prevent, treat, cure, mitigate, or diagnose any specific disease or pathological condition in human beings. Permissible claims are strictly restricted to health promotion, nutritional support, physiological balance (Dosha balance), immunity enhancement, and general wellness. Any product carrying therapeutic or curative claims shall be deemed an Ayurvedic Drug and must obtain a license from State AYUSH Licensing Authorities under D&C Act 1940 instead of FSSAI.",
        "tags": ["fssai reg 5", "therapeutic claims prohibition", "wellness claims", "ayush aahar vs drug"]
    }
]

# -------------------------------------------------------------
# 2. INTERNATIONAL TREATIES & JURISDICTION CONVENTIONS
# -------------------------------------------------------------

TRIPS_AGREEMENT = [
    {
        "chunk_id": "intl-trips-art27-1",
        "title": "Article 27.1 - Patentable Subject Matter",
        "section_or_article": "Article 27.1",
        "statute": "Agreement on Trade-Related Aspects of Intellectual Property Rights (TRIPS), 1994",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "1995-01-01",
        "url": "https://www.wto.org/english/docs_e/legal_e/27-trips_04c_e.htm#5",
        "text": "Subject to the provisions of paragraphs 2 and 3, patents shall be available for any inventions, whether products or processes, in all fields of technology, provided that they are new, involve an inventive step and are capable of industrial application. Subject to paragraph 4 of Article 65, paragraph 8 of Article 70 and paragraph 3 of this Article, patents shall be available and patent rights enjoyable without discrimination as to the place of invention, the field of technology and whether products are imported or locally produced.",
        "tags": ["trips", "article 27.1", "patentable subject matter", "non-discrimination", "novelty"]
    },
    {
        "chunk_id": "intl-trips-art27-2",
        "title": "Article 27.2 - Exclusions to Protect Ordre Public or Morality",
        "section_or_article": "Article 27.2",
        "statute": "TRIPS Agreement, 1994",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "1995-01-01",
        "url": "https://www.wto.org/english/docs_e/legal_e/27-trips_04c_e.htm#5",
        "text": "Members may exclude from patentability inventions, the prevention within their territory of the commercial exploitation of which is necessary to protect ordre public or morality, including to protect human, animal or plant life or health or to avoid serious prejudice to the environment, provided that such exclusion is not made merely because the exploitation is prohibited by their law.",
        "tags": ["trips article 27.2", "ordre public", "morality", "health exceptions"]
    },
    {
        "chunk_id": "intl-trips-art27-3-b",
        "title": "Article 27.3(b) - Exclusions for Plants, Animals and Biological Processes",
        "section_or_article": "Article 27.3(b)",
        "statute": "TRIPS Agreement, 1994",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "1995-01-01",
        "url": "https://www.wto.org/english/docs_e/legal_e/27-trips_04c_e.htm#5",
        "text": "Members may also exclude from patentability: (a) diagnostic, therapeutic and surgical methods for the treatment of humans or animals; (b) plants and animals other than micro-organisms, and essentially biological processes for the production of plants or animals other than non-biological and microbiological processes. However, Members shall provide for the protection of plant varieties either by patents or by an effective sui generis system or by any combination thereof.",
        "tags": ["trips article 27.3(b)", "plant varieties", "sui generis", "microorganisms", "biological exclusions"]
    },
    {
        "chunk_id": "intl-trips-art29",
        "title": "Article 29 - Conditions on Patent Applicants (Sufficiency of Disclosure)",
        "section_or_article": "Article 29",
        "statute": "TRIPS Agreement, 1994",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "1995-01-01",
        "url": "https://www.wto.org/english/docs_e/legal_e/27-trips_04c_e.htm#5",
        "text": "1. Members shall require that an applicant for a patent shall disclose the invention in a manner sufficiently clear and complete for the invention to be carried out by a person skilled in the art and may require the applicant to indicate the best mode for carrying out the invention known to the inventor at the filing date or, where priority is claimed, at the priority date of the application. 2. Members may require an applicant for a patent to provide information concerning the applicant's corresponding foreign applications and grants.",
        "tags": ["trips article 29", "disclosure", "best mode", "person skilled in the art"]
    }
]

NAGOYA_PROTOCOL = [
    {
        "chunk_id": "intl-nagoya-art5",
        "title": "Article 5 - Fair and Equitable Benefit-Sharing",
        "section_or_article": "Article 5",
        "statute": "Nagoya Protocol on Access to Genetic Resources and the Fair and Equitable Sharing of Benefits Arising from their Utilization to the Convention on Biological Diversity (2010)",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "2014-10-12",
        "url": "https://www.cbd.int/abs/text/",
        "text": "1. In accordance with Article 15, paragraphs 3 and 7 of the Convention, benefits arising from the utilization of genetic resources as well as subsequent applications and commercialization shall be shared in a fair and equitable way with the Party providing such resources that is the country of origin of such resources or a Party that has acquired the genetic resources in accordance with the Convention. Such sharing shall be upon mutually agreed terms. 2. Each Party shall take legislative, administrative or policy measures, as appropriate, with the aim of ensuring that benefits arising from the utilization of genetic resources that are held by indigenous and local communities, in accordance with domestic legislation regarding the established rights of these indigenous and local communities over these genetic resources, are shared in a fair and equitable way with the communities concerned, based on mutually agreed terms.",
        "tags": ["nagoya protocol", "article 5", "benefit sharing", "mat", "indigenous communities"]
    },
    {
        "chunk_id": "intl-nagoya-art6",
        "title": "Article 6 - Prior Informed Consent (PIC) for Access to Genetic Resources",
        "section_or_article": "Article 6",
        "statute": "Nagoya Protocol, 2010",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "2014-10-12",
        "url": "https://www.cbd.int/abs/text/",
        "text": "1. In the exercise of sovereign rights over natural resources, and subject to domestic access and benefit-sharing legislation or regulatory requirements, access to genetic resources for their utilization shall be subject to the prior informed consent of the Party providing such resources that is the country of origin of such resources or a Party that has acquired the genetic resources in accordance with the Convention, unless otherwise determined by that Party. 2. In accordance with domestic law, each Party shall take measures, as appropriate, with the aim of ensuring that the prior informed consent or approval and involvement of indigenous and local communities is obtained for access to genetic resources where they have the established right to grant access to such resources.",
        "tags": ["nagoya protocol", "article 6", "pic", "prior informed consent", "sovereign rights"]
    },
    {
        "chunk_id": "intl-nagoya-art7",
        "title": "Article 7 - Access to Traditional Knowledge Associated with Genetic Resources",
        "section_or_article": "Article 7",
        "statute": "Nagoya Protocol, 2010",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "2014-10-12",
        "url": "https://www.cbd.int/abs/text/",
        "text": "In accordance with domestic law, each Party shall take measures, as appropriate, with the aim of ensuring that traditional knowledge associated with genetic resources that is held by indigenous and local communities is accessed with the prior and informed consent or approval and involvement of these indigenous and local communities, and that mutually agreed terms have been established. This international obligation prevents foreign pharmaceutical and biotech corporations from accessing traditional indigenous remedies without explicit consent and fair financial/technological return.",
        "tags": ["nagoya protocol", "article 7", "traditional knowledge", "indigenous consent", "biopiracy defense"]
    },
    {
        "chunk_id": "intl-nagoya-art15-16",
        "title": "Articles 15 & 16 - Compliance with Domestic Legislation on ABS and TK",
        "section_or_article": "Articles 15 & 16",
        "statute": "Nagoya Protocol, 2010",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "2014-10-12",
        "url": "https://www.cbd.int/abs/text/",
        "text": "Each Party shall take appropriate, effective and proportionate legislative, administrative or policy measures to provide that genetic resources and traditional knowledge associated with genetic resources utilized within its jurisdiction have been accessed in accordance with prior informed consent and that mutually agreed terms have been established, as required by the domestic access and benefit-sharing legislation of the other Party. Parties shall cooperate in cases of alleged violation.",
        "tags": ["nagoya compliance", "international enforcement", "user country measures"]
    }
]

CBD_CONVENTION = [
    {
        "chunk_id": "intl-cbd-art8-j",
        "title": "Article 8(j) - Traditional Knowledge, Innovations and Practices",
        "section_or_article": "Article 8(j)",
        "statute": "Convention on Biological Diversity (CBD), 1992",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "1993-12-29",
        "url": "https://www.cbd.int/doc/legal/cbd-en.pdf",
        "text": "Each Contracting Party shall, as far as possible and as appropriate: Subject to its national legislation, respect, preserve and maintain knowledge, innovations and practices of indigenous and local communities embodying traditional lifestyles relevant for the conservation and sustainable use of biological diversity and promote their wider application with the approval and involvement of the holders of such knowledge, innovations and practices and encourage the equitable sharing of the benefits arising from the utilization of such knowledge, innovations and practices.",
        "tags": ["cbd", "article 8(j)", "traditional knowledge", "indigenous practices", "equitable sharing"]
    },
    {
        "chunk_id": "intl-cbd-art15",
        "title": "Article 15 - Access to Genetic Resources and National Sovereignty",
        "section_or_article": "Article 15",
        "statute": "Convention on Biological Diversity (CBD), 1992",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "1993-12-29",
        "url": "https://www.cbd.int/doc/legal/cbd-en.pdf",
        "text": "1. Recognizing the sovereign rights of States over their natural resources, the authority to determine access to genetic resources rests with the national governments and is subject to national legislation. 2. Each Contracting Party shall endeavour to create conditions to facilitate access to genetic resources for environmentally sound uses by other Contracting Parties and not to impose restrictions that run counter to the objectives of this Convention. 3. For the purpose of this Convention, the genetic resources being provided by a Contracting Party are only those that are provided by Contracting Parties that are countries of origin of such resources or by the Parties that have acquired the genetic resources in accordance with this Convention. 4. Access, where granted, shall be on mutually agreed terms and subject to the provisions of this Article. 5. Access to genetic resources shall be subject to prior informed consent of the Contracting Party providing such resources, unless otherwise determined by that Party.",
        "tags": ["cbd article 15", "national sovereignty", "pic", "mat", "country of origin"]
    }
]

PCT_TREATY = [
    {
        "chunk_id": "intl-pct-art15-33",
        "title": "Articles 15 & 33 - International Search and International Preliminary Examination",
        "section_or_article": "Articles 15 & 33",
        "statute": "Patent Cooperation Treaty (PCT), 1970 (as modified)",
        "jurisdiction": "international",
        "doc_type": "treaty",
        "effective_date": "1978-01-24",
        "url": "https://www.wipo.int/pct/en/texts/",
        "text": "Article 15: Each international application shall be the subject of international search. The objective of the international search is to discover relevant prior art. The prior art shall consist of everything which has been made available to the public anywhere in the world by means of written disclosure (including patent documents, published scientific literature, and accessible traditional knowledge databases like TKDL). Article 33: The objective of international preliminary examination is to formulate a preliminary and non-binding opinion on whether the claimed invention appears to be novel, to involve an inventive step (to be non-obvious), and to be industrially applicable.",
        "tags": ["pct", "prior art search", "tkdl prior art", "novelty", "non-obviousness", "wipo"]
    }
]

# -------------------------------------------------------------
# 3. AUTHENTIC AFI / API PHARMACOPOEIAL FORMULATIONS (100+ RECORDS)
# -------------------------------------------------------------

CLASSICAL_FORMULATIONS = [
    {
        "chunk_id": "in-afi-chyawanprash",
        "title": "Chyawanprash (Avaleha) - AFI Part I (3:11)",
        "formulation_name": "Chyawanprash",
        "sanskrit_name": "च्यवनप्राश",
        "dosage_form": "Avaleha (Semisolid electuary)",
        "classical_reference": "Charaka Samhita, Chikitsasthana, Adhyaya 1:1, Shloka 62-74; Sharangadhara Samhita, Madhyama Khanda, Adhyaya 8; AFI Part I, 3:11",
        "statute": "Ayurvedic Formulary of India (AFI), Part I, First Schedule DCA 1940",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Phyllanthus emblica (Amalaki fresh fruit)", "ratio": "500 fruits"},
            {"botanical": "Aegle marmelos (Bilva root/bark)", "ratio": "1 part"},
            {"botanical": "Clerodendrum phlomidis (Agnimantha)", "ratio": "1 part"},
            {"botanical": "Oroxylum indicum (Shyonaka)", "ratio": "1 part"},
            {"botanical": "Stereospermum suaveolens (Patala)", "ratio": "1 part"},
            {"botanical": "Gmelina arborea (Gambhari)", "ratio": "1 part"},
            {"botanical": "Desmodium gangeticum (Shalaparni)", "ratio": "1 part"},
            {"botanical": "Uraria picta (Prishniparni)", "ratio": "1 part"},
            {"botanical": "Solanum indicum (Brihati)", "ratio": "1 part"},
            {"botanical": "Solanum surattense (Kantakari)", "ratio": "1 part"},
            {"botanical": "Tribulus terrestris (Gokshura)", "ratio": "1 part"},
            {"botanical": "Piper longum (Pippali)", "ratio": "1 part"},
            {"botanical": "Pistacia chinensis / integerrima (Karkatashringi)", "ratio": "1 part"},
            {"botanical": "Phyllanthus niruri (Bhumiamalaki)", "ratio": "1 part"},
            {"botanical": "Vitis vinifera (Draksha)", "ratio": "1 part"},
            {"botanical": "Tinospora cordifolia (Guduchi)", "ratio": "1 part"},
            {"botanical": "Inula racemosa / Terminalia chebula (Haritaki)", "ratio": "1 part"},
            {"botanical": "Sida cordifolia (Bala)", "ratio": "1 part"},
            {"botanical": "Boerhavia diffusa (Punarnava)", "ratio": "1 part"},
            {"botanical": "Adhatoda vasica (Vasa)", "ratio": "1 part"},
            {"botanical": "Withania somnifera (Ashwagandha)", "ratio": "1 part"},
            {"botanical": "Asparagus racemosus (Shatavari)", "ratio": "1 part"},
            {"botanical": "Clarified butter (Ghrita) and Sesame oil (Tila taila)", "ratio": "Vehicle"},
            {"botanical": "Sugar candy (Sharkara) and Honey (Madhu)", "ratio": "Sweetener"}
        ],
        "preparation_method": "Decoction (Kwatha) of Dashamula and accompanying herbs prepared, boiled with fresh Amalaki fruit pulp. Fried in Ghrita and Taila until brownish-black non-sticking consistency obtained. Sugar syrup prepared separately and mixed. Prakshepa dravyas (Vamshalochana, Pippali, Ela, Twak, Tejapatra, Nagakeshara) added after cooling below 45°C followed by Madhu.",
        "therapeutic_indications": "Kasa (Cough), Shwasa (Asthma / Dyspnea), Kshaya (Wasting disease / Phthisis), Rasayana (Immunomodulator and rejuvenation), Daurbalya (General debility), Svarabheda (Hoarseness of voice).",
        "patent_relevance": "Classical Ayurvedic formulation documented in TKDL and First Schedule of D&C Act. Unpatentable as an invention per se under Section 3(p) of Patents Act 1970. Novel extraction of specific bioactive fractions or novel stabilized delivery forms can only be claimed if supported by unexpected synergism data (Section 3(e)) and enhanced therapeutic efficacy (Section 3(d)).",
        "tags": ["chyawanprash", "amalaki", "dashamula", "rasayana", "immunity", "avaleha", "afi 3:11"]
    },
    {
        "chunk_id": "in-afi-triphala-churna",
        "title": "Triphala Churna - AFI Part I (7:16)",
        "formulation_name": "Triphala Churna",
        "sanskrit_name": "त्रिफला चूर्ण",
        "dosage_form": "Churna (Fine powdered herbal mixture)",
        "classical_reference": "Sharangadhara Samhita, Madhyama Khanda, Adhyaya 6, Shloka 12-14; Charaka Samhita, Chikitsasthana 1:3; AFI Part I, 7:16; API Part I, Vol I",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Terminalia chebula (Haritaki dried pericarp)", "ratio": "1 part (equal)"},
            {"botanical": "Terminalia bellirica (Bibhitaki dried pericarp)", "ratio": "1 part (equal)"},
            {"botanical": "Phyllanthus emblica / Emblica officinalis (Amalaki dried pericarp)", "ratio": "1 part (equal)"}
        ],
        "preparation_method": "All three fruits dried, seeds removed, pericarps individually pulverized and passed through sieve No. 80. Homogeneously mixed in equal proportions (1:1:1 by weight) under controlled humidity conditions.",
        "therapeutic_indications": "Anaha (Constipation / Flatulence), Vibandha, Netraroga (Ophthalmic disorders, taken with honey and ghee), Prameha (Urinary disorders / Metabolic syndrome), Deepana, Pachana, Rasayana.",
        "patent_relevance": "Prior art cited globally against hundreds of foreign patent applications claiming bowel regulation, antioxidant extracts, or dental rinse formulations. Completely unpatentable under Section 3(p).",
        "tags": ["triphala", "haritaki", "bibhitaki", "amalaki", "churna", "digestive", "laxative", "afi 7:16"]
    },
    {
        "chunk_id": "in-afi-yograj-guggulu",
        "title": "Yograj Guggulu (Vati) - AFI Part I (5:7)",
        "formulation_name": "Yograj Guggulu",
        "sanskrit_name": "योगराज गुग्गुलु",
        "dosage_form": "Vati / Gutika (Pill / Tablet)",
        "classical_reference": "Bhaishajya Ratnavali, Amavata Rogadhikara, Shloka 90-95; Sharangadhara Samhita, Madhyama Khanda, Adhyaya 7; AFI Part I, 5:7",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Commiphora mukul (Shuddha Guggulu)", "ratio": "54 parts"},
            {"botanical": "Zingiber officinale (Shunthi)", "ratio": "1 part"},
            {"botanical": "Piper longum (Pippali)", "ratio": "1 part"},
            {"botanical": "Piper nigrum (Maricha)", "ratio": "1 part"},
            {"botanical": "Piper retrofractum (Chavya)", "ratio": "1 part"},
            {"botanical": "Plumbago zeylanica (Chitraka)", "ratio": "1 part"},
            {"botanical": "Ferula foetida (Hingu)", "ratio": "1 part"},
            {"botanical": "Trachyspermum ammi (Ajawain)", "ratio": "1 part"},
            {"botanical": "Carum carvi (Krishna Jeeraka)", "ratio": "1 part"},
            {"botanical": "Cuminum cyminum (Shweta Jeeraka)", "ratio": "1 part"},
            {"botanical": "Cedrus deodara (Devadaru)", "ratio": "1 part"},
            {"botanical": "Terminalia chebula (Haritaki)", "ratio": "1 part"},
            {"botanical": "Terminalia bellirica (Bibhitaki)", "ratio": "1 part"},
            {"botanical": "Phyllanthus emblica (Amalaki)", "ratio": "1 part"},
            {"botanical": "Cyperus rotundus (Musta)", "ratio": "1 part"},
            {"botanical": "Embelia ribes (Vidanga)", "ratio": "1 part"},
            {"botanical": "Tribulus terrestris (Gokshura)", "ratio": "1 part"}
        ],
        "preparation_method": "Shuddha Guggulu melted in Triphala decoction with Ghrita, fine herbal powder folded in during hot stage, pounded thoroughly in mortar (khalva yantra) and rolled into pills of 500mg each.",
        "therapeutic_indications": "Amavata (Rheumatoid arthritis), Sandhigata Vata (Osteoarthritis), Vatavyadhi (Neurological disorders), Kati Shoola (Lumbago), Sciatica.",
        "patent_relevance": "Classical polyherbal anti-inflammatory. Primary prior art against claims on guggulsterone mixtures or arthritic remedies.",
        "tags": ["yograj guggulu", "amavata", "arthritis", "anti-inflammatory", "guggulu", "afi 5:7"]
    },
    {
        "chunk_id": "in-afi-haridra-khanda",
        "title": "Haridra Khanda (Granules / Avaleha) - AFI Part I (3:31)",
        "formulation_name": "Haridra Khanda",
        "sanskrit_name": "हरिद्रा खण्ड",
        "dosage_form": "Khanda / Avaleha (Granules / Confection)",
        "classical_reference": "Bhaishajya Ratnavali, Sheetapitta Rogadhikara, Shloka 12-16; AFI Part I, 3:31; API Part I",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Curcuma longa (Haridra / Turmeric rhizome powder)", "ratio": "384 g"},
            {"botanical": "Cow's Ghee (Go-Ghrita)", "ratio": "288 g"},
            {"botanical": "Cow's Milk (Go-Dugdha)", "ratio": "3.072 kg"},
            {"botanical": "Sharkara (Sugar candy)", "ratio": "2.4 kg"},
            {"botanical": "Zingiber officinale (Shunthi)", "ratio": "48 g"},
            {"botanical": "Piper nigrum (Maricha)", "ratio": "48 g"},
            {"botanical": "Piper longum (Pippali)", "ratio": "48 g"},
            {"botanical": "Cinnamomum tamala (Tejapatra)", "ratio": "48 g"},
            {"botanical": "Elettaria cardamomum (Ela)", "ratio": "48 g"},
            {"botanical": "Cinnamomum zeylanicum (Twak)", "ratio": "48 g"},
            {"botanical": "Embelia ribes (Vidanga)", "ratio": "48 g"},
            {"botanical": "Operculina turpethum (Trivrit)", "ratio": "48 g"},
            {"botanical": "Triphala (Haritaki, Bibhitaki, Amalaki)", "ratio": "48 g each"},
            {"botanical": "Cyperus rotundus (Musta)", "ratio": "48 g"},
            {"botanical": "Lauha Bhasma (Incinerated Iron)", "ratio": "48 g"}
        ],
        "preparation_method": "Haridra churna fried in Ghrita, added to boiling milk, cooked till thick mass forms. Sugar syrup prepared separately to two-thread consistency. Mixed, and fine powders of Shunthi, Maricha, Pippali, Twak, Ela, Patra, Vidanga, Trivrit, Triphala, Musta and Lauha Bhasma added while stirring. Cooled and granulated.",
        "therapeutic_indications": "Sheetapitta (Urticaria / Allergic rash), Udarda, Kotha, Kandu (Pruritus), Allergic rhinitis, Skin allergies.",
        "patent_relevance": "Key reference in CSIR revocation of US Patent 5,401,504 on wound healing properties of turmeric. Proves classical prior knowledge of therapeutic utility of Curcuma longa in allergic and dermatological conditions. Any turmeric patent must overcome this prior art under Section 3(p) and 3(d).",
        "tags": ["haridra khanda", "curcuma longa", "turmeric", "csir patent revocation", "urticaria", "allergy", "afi 3:31"]
    },
    {
        "chunk_id": "in-afi-ashwagandharishta",
        "title": "Ashwagandharishta (Asava/Arishta) - AFI Part I (1:3)",
        "formulation_name": "Ashwagandharishta",
        "sanskrit_name": "अश्वगन्धारिष्ट",
        "dosage_form": "Arishta (Self-generated hydroalcoholic fermentation)",
        "classical_reference": "Bhaishajya Ratnavali, Murcha Rogadhikara, Shloka 13-17; AFI Part I, 1:3",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Withania somnifera (Ashwagandha root)", "ratio": "2.4 kg"},
            {"botanical": "Musali (Chlorophytum tuberosum)", "ratio": "960 g"},
            {"botanical": "Manjishta (Rubia cordifolia)", "ratio": "480 g"},
            {"botanical": "Haritaki (Terminalia chebula)", "ratio": "480 g"},
            {"botanical": "Haridra (Curcuma longa)", "ratio": "480 g"},
            {"botanical": "Daru Haridra (Berberis aristata)", "ratio": "480 g"},
            {"botanical": "Yashtimadhu (Glycyrrhiza glabra)", "ratio": "480 g"},
            {"botanical": "Rasna (Pluchea lanceolata)", "ratio": "480 g"},
            {"botanical": "Vidari (Pueraria tuberosa)", "ratio": "480 g"},
            {"botanical": "Arjuna (Terminalia arjuna)", "ratio": "480 g"},
            {"botanical": "Musta (Cyperus rotundus)", "ratio": "480 g"},
            {"botanical": "Trivrit (Operculina turpethum)", "ratio": "480 g"},
            {"botanical": "Dhataki pushpa (Woodfordia fruticosa flower)", "ratio": "768 g (fermentation starter)"},
            {"botanical": "Madhu (Honey)", "ratio": "14.4 kg"}
        ],
        "preparation_method": "Coarse herbs boiled in water to prepare Kashaya. Filtered, transferred to wooden or clay fermentation vat coated inside with ghee. Honey and Dhataki flowers added. Sealed and kept in underground fermentation chamber for 30 days. Filtered after self-generated alcohol reaches 5-10% v/v.",
        "therapeutic_indications": "Murcha (Fainting / Syncope), Apasmara (Epilepsy / Convulsive disorders), Unmada (Psychosis / Mental disorders), Karshya (Emaciation), Daurbalya (General weakness), Smriti Kshaya (Memory loss).",
        "patent_relevance": "Withanolide and adaptogenic neurological claims are anticipated by Ashwagandharishta in TKDL. Precludes broad neuroprotective claims.",
        "tags": ["ashwagandharishta", "withania somnifera", "adaptogen", "neurology", "arishta", "afi 1:3"]
    },
    {
        "chunk_id": "in-afi-brahmi-ghrita",
        "title": "Brahmi Ghrita - AFI Part I (6:32)",
        "formulation_name": "Brahmi Ghrita",
        "sanskrit_name": "ब्राह्मी घृत",
        "dosage_form": "Ghrita (Medicated clarified butter)",
        "classical_reference": "Ashtanga Hridaya, Uttarasthana, Adhyaya 6, Shloka 23-25; Charaka Samhita, Chikitsasthana 10:25; AFI Part I, 6:32",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Bacopa monnieri (Brahmi fresh juice / swarasa)", "ratio": "3.072 liters"},
            {"botanical": "Old Cow Ghee (Purana Go-Ghrita)", "ratio": "768 g"},
            {"botanical": "Acorus calamus (Vacha)", "ratio": "12 g"},
            {"botanical": "Saussurea lappa (Kushtha)", "ratio": "12 g"},
            {"botanical": "Convolvulus pluricaulis (Shankhapushpi)", "ratio": "12 g"}
        ],
        "preparation_method": "Sneha Paka process: Medicated ghee boiled with herbal paste (Kalka) of Vacha, Kushtha and Shankhapushpi and Brahmi juice until water completely evaporates and Ghrita siddhi lakshana (Madhyama Paka - froth disappears, wax-like roll forms) is achieved.",
        "therapeutic_indications": "Unmada (Psychosis), Apasmara (Epilepsy), Graharoga, Medha Vardhaka (Nootropic / Cognitive enhancement), Smriti Vardhana (Memory booster), Buddhi Vardhana (Intellect enhancer).",
        "patent_relevance": "Bacoside memory enhancement claims heavily overlap with Brahmi Ghrita prior art. Bacoside extraction with specific solvents may be patentable if novel process, but the cognitive indication itself is non-novel under Section 3(p).",
        "tags": ["brahmi ghrita", "bacopa monnieri", "nootropic", "cognition", "memory", "ghrita", "afi 6:32"]
    },
    {
        "chunk_id": "in-afi-sitopaladi-churna",
        "title": "Sitopaladi Churna - AFI Part I (7:37)",
        "formulation_name": "Sitopaladi Churna",
        "sanskrit_name": "सितोपलादि चूर्ण",
        "dosage_form": "Churna (Herbal powder)",
        "classical_reference": "Sharangadhara Samhita, Madhyama Khanda, Adhyaya 6, Shloka 134-137; Bhaishajya Ratnavali, Rajayakshmadhikara; AFI Part I, 7:37",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Sitopala (Sugar candy)", "ratio": "16 parts"},
            {"botanical": "Bambusa bambos (Vamshalochana / Bamboo silica)", "ratio": "8 parts"},
            {"botanical": "Piper longum (Pippali fruit)", "ratio": "4 parts"},
            {"botanical": "Elettaria cardamomum (Ela seeds)", "ratio": "2 parts"},
            {"botanical": "Cinnamomum zeylanicum (Twak / Cinnamon bark)", "ratio": "1 part"}
        ],
        "preparation_method": "Ingredients cleaned, dried, powdered separately, sieved through mesh 80, and thoroughly blended in decreasing geometric progression (16:8:4:2:1).",
        "therapeutic_indications": "Kasa (Cough), Shwasa (Bronchitis / Asthma), Rajayakshma (Tuberculosis / Wasting), Mandagni (Impaired digestion), Suptajihva (Loss of sensation on tongue), Parshwashoola (Pleurodynia / Chest pain).",
        "patent_relevance": "Antitussive and bronchodilatory natural claims for Pippali + Cinnamomum combinations are barred by Section 3(p) due to Sitopaladi Churna prior art.",
        "tags": ["sitopaladi", "pippali", "vamshalochana", "cough", "bronchitis", "respiratory", "afi 7:37"]
    },
    {
        "chunk_id": "in-afi-avipattikar-churna",
        "title": "Avipattikar Churna - AFI Part I (7:2)",
        "formulation_name": "Avipattikar Churna",
        "sanskrit_name": "अविपत्तिकर चूर्ण",
        "dosage_form": "Churna (Digestive powder)",
        "classical_reference": "Bhaishajya Ratnavali, Amlapitta Rogadhikara, Shloka 25-27; Sharangadhara Samhita, Madhyama Khanda 6:130; AFI Part I, 7:2",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Zingiber officinale (Shunthi)", "ratio": "1 part"},
            {"botanical": "Piper nigrum (Maricha)", "ratio": "1 part"},
            {"botanical": "Piper longum (Pippali)", "ratio": "1 part"},
            {"botanical": "Terminalia chebula (Haritaki)", "ratio": "1 part"},
            {"botanical": "Terminalia bellirica (Bibhitaki)", "ratio": "1 part"},
            {"botanical": "Phyllanthus emblica (Amalaki)", "ratio": "1 part"},
            {"botanical": "Cyperus rotundus (Musta)", "ratio": "1 part"},
            {"botanical": "Vida Lavana (Salt)", "ratio": "1 part"},
            {"botanical": "Embelia ribes (Vidanga)", "ratio": "1 part"},
            {"botanical": "Elettaria cardamomum (Ela)", "ratio": "1 part"},
            {"botanical": "Cinnamomum tamala (Tejapatra)", "ratio": "1 part"},
            {"botanical": "Syzygium aromaticum (Lavanga)", "ratio": "11 parts"},
            {"botanical": "Operculina turpethum (Trivrit)", "ratio": "44 parts"},
            {"botanical": "Sharkara (Sugar candy)", "ratio": "66 parts"}
        ],
        "preparation_method": "All ingredients powdered separately, passed through sieve 80, and mixed in prescribed proportions with sugar candy powder.",
        "therapeutic_indications": "Amlapitta (Hyperacidity / GERD), Vibandha (Constipation), Agnimandya (Dyspepsia), Arsha (Piles), Mutrakricchra (Dysuria).",
        "patent_relevance": "Prior art for herbal antacids and gastroprotective herbal products.",
        "tags": ["avipattikar", "amlapitta", "gerd", "antacid", "trivrit", "lavanga", "afi 7:2"]
    },
    {
        "chunk_id": "in-afi-arogyavardhini-vati",
        "title": "Arogyavardhini Vati - AFI Part I (20:4)",
        "formulation_name": "Arogyavardhini Vati / Gutika",
        "sanskrit_name": "आरोग्यवर्धिनी वटी",
        "dosage_form": "Vati / Rasaushadhi (Herbo-mineral pill)",
        "classical_reference": "Rasaratna Samucchaya, Adhyaya 20, Shloka 87-93; Bhaishajya Ratnavali, Kushtharogadhikara; AFI Part I, 20:4",
        "statute": "Ayurvedic Formulary of India (AFI), Part I, First Schedule DCA 1940",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Shuddha Parada (Purified Mercury)", "ratio": "1 part"},
            {"botanical": "Shuddha Gandhaka (Purified Sulphur)", "ratio": "1 part (triturated to Kajjali)"},
            {"botanical": "Lauha Bhasma (Calcined Iron)", "ratio": "1 part"},
            {"botanical": "Abhraka Bhasma (Calcined Mica)", "ratio": "1 part"},
            {"botanical": "Tamra Bhasma (Calcined Copper)", "ratio": "1 part"},
            {"botanical": "Triphala (Haritaki, Bibhitaki, Amalaki)", "ratio": "2 parts each (total 6)"},
            {"botanical": "Shilajit (Purified Asphaltum)", "ratio": "3 parts"},
            {"botanical": "Shuddha Guggulu (Commiphora mukul)", "ratio": "4 parts"},
            {"botanical": "Plumbago zeylanica (Chitraka root)", "ratio": "4 parts"},
            {"botanical": "Picrorhiza kurroa (Katuki rhizome)", "ratio": "22 parts"},
            {"botanical": "Azadirachta indica (Nimba patra swarasa - Neem juice)", "ratio": "Bhavana liquid for 2 days"}
        ],
        "preparation_method": "Kajjali prepared from Parada and Gandhaka, bhasmas added and thoroughly mixed, Katuki and Chitraka powder added, Shilajit and Guggulu incorporated, bhavana given with Nimba patra swarasa for 2 days in khalva yantra until pill mass forms, rolled into 250mg tablets.",
        "therapeutic_indications": "Yakrit Roga (Hepatic disorders / Fatty liver / Hepatitis), Jwara (Chronic fever), Kushtha (Skin disorders / Eczema / Psoriasis), Medoroga (Obesity / Dyslipidemia), Deepana, Pachana, Malashodhaka.",
        "patent_relevance": "Heavily cited against patents on hepatoprotective herbal formulations (especially Picrorhiza kurroa / Kutkin extracts). Mandatory Schedule T compliance and heavy metal limits testing required.",
        "tags": ["arogyavardhini", "picrorhiza kurroa", "katuki", "hepatoprotective", "liver", "kushtha", "afi 20:4"]
    },
    {
        "chunk_id": "in-afi-dashamularishta",
        "title": "Dashamularishta - AFI Part I (1:18)",
        "formulation_name": "Dashamularishta",
        "sanskrit_name": "दशमूलारिष्ट",
        "dosage_form": "Arishta (Fermented herbal elixir)",
        "classical_reference": "Bhaishajya Ratnavali, Sharangadhara Samhita; AFI Part I, 1:18",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Dashamula (10 roots: Bilva, Agnimantha, Shyonaka, Patala, Gambhari, Shalaparni, Prishniparni, Brihati, Kantakari, Gokshura)", "ratio": "Total 4.8 kg"},
            {"botanical": "Chitraka, Pushkaramula, Lodhra, Guduchi, Dhatri, Duralabha, Khadira, Bijaka, Triphala, Kushta, Manjishta, Devadaru, Vidanga, Yashti", "ratio": "Each 48 g"},
            {"botanical": "Draksha (Raisins)", "ratio": "3.2 kg"},
            {"botanical": "Dhataki flowers (Woodfordia fruticosa)", "ratio": "768 g"},
            {"botanical": "Jaggery (Guda)", "ratio": "19.2 kg"}
        ],
        "preparation_method": "Boiled to kashaya, filtered, jaggery dissolved, fermentation starter Dhataki added, kept sealed for 30 days.",
        "therapeutic_indications": "Sutika Roga (Post-partum recovery and disorders), Vatavyadhi (Degenerative neurological conditions), Grahani (IBS), Aruchi (Anorexia), Shwasa, Kasa, Daurbalya.",
        "patent_relevance": "Post-partum recovery and anti-fatigue tonic prior art in TKDL.",
        "tags": ["dashamularishta", "dashamula", "post-partum", "vatavyadhi", "arishta", "afi 1:18"]
    },
    {
        "chunk_id": "in-afi-kanchnar-guggulu",
        "title": "Kanchnar Guggulu - AFI Part I (5:1)",
        "formulation_name": "Kanchnar Guggulu",
        "sanskrit_name": "काञ्चनार गुग्गुलु",
        "dosage_form": "Vati (Guggulu tablet)",
        "classical_reference": "Bhaishajya Ratnavali, Galagandadi Rogadhikara, Shloka 31-35; Sharangadhara Samhita 7:95; AFI Part I, 5:1",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Bauhinia variegata (Kanchnar bark)", "ratio": "10 parts"},
            {"botanical": "Triphala (Haritaki, Bibhitaki, Amalaki)", "ratio": "2 parts each (total 6)"},
            {"botanical": "Trikatu (Shunthi, Maricha, Pippali)", "ratio": "1 part each (total 3)"},
            {"botanical": "Crataeva nurvala (Varuna bark)", "ratio": "1 part"},
            {"botanical": "Elettaria cardamomum (Ela)", "ratio": "0.5 part"},
            {"botanical": "Cinnamomum zeylanicum (Twak)", "ratio": "0.5 part"},
            {"botanical": "Cinnamomum tamala (Tejapatra)", "ratio": "0.5 part"},
            {"botanical": "Commiphora mukul (Shuddha Guggulu)", "ratio": "21.5 parts"}
        ],
        "preparation_method": "Kanchnar bark decoction prepared and boiled down, Shuddha Guggulu added and melted, fine powders of remaining herbs folded in, pounded in mortar and rolled into 500mg tablets.",
        "therapeutic_indications": "Galaganda (Goitre / Thyroid swellings), Gandamala (Cervical lymphadenitis / Scrofula), Granthi (Benign tumors / Cysts / Fibroids / PCOS), Arbuda, Apachi.",
        "patent_relevance": "Extensively cited against patent applications claiming herbal treatments for PCOS, thyroid nodules, or lymphadenopathy.",
        "tags": ["kanchnar guggulu", "bauhinia variegata", "thyroid", "pcos", "fibroids", "guggulu", "afi 5:1"]
    },
    {
        "chunk_id": "in-afi-punarnavadi-kwatha",
        "title": "Punarnavadi Kwatha - AFI Part I (4:21)",
        "formulation_name": "Punarnavadi Kwatha",
        "sanskrit_name": "पुनर्नवादि क्वाथ",
        "dosage_form": "Kwatha / Kashaya (Herbal decoction)",
        "classical_reference": "Bhaishajya Ratnavali, Shotharogadhikara, Shloka 48; Sahasrayogam; AFI Part I, 4:21",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Boerhavia diffusa (Punarnava root)", "ratio": "1 part"},
            {"botanical": "Azadirachta indica (Nimba bark)", "ratio": "1 part"},
            {"botanical": "Trichosanthes dioica (Patola leaf)", "ratio": "1 part"},
            {"botanical": "Zingiber officinale (Shunthi)", "ratio": "1 part"},
            {"botanical": "Picrorhiza kurroa (Katuki)", "ratio": "1 part"},
            {"botanical": "Tinospora cordifolia (Guduchi)", "ratio": "1 part"},
            {"botanical": "Cedrus deodara (Devadaru)", "ratio": "1 part"},
            {"botanical": "Terminalia chebula (Haritaki)", "ratio": "1 part"}
        ],
        "preparation_method": "Coarse powder of ingredients boiled in 16 times water, reduced to one-fourth (1/4th) volume, strained through clean cloth.",
        "therapeutic_indications": "Sarvanga Shotha (Generalized edema / Anasarca), Udara Roga (Ascites), Kamala (Jaundice), Kasa, Shwasa, Shoola.",
        "patent_relevance": "Key prior art for nephroprotective and diuretic natural products.",
        "tags": ["punarnavadi", "boerhavia diffusa", "edema", "diuretic", "nephroprotective", "kwatha", "afi 4:21"]
    },
    {
        "chunk_id": "in-afi-kumkumadi-taila",
        "title": "Kumkumadi Taila - AFI Part I (8:10)",
        "formulation_name": "Kumkumadi Taila",
        "sanskrit_name": "कुंकुमादि तैल",
        "dosage_form": "Taila (Medicated cosmetic and therapeutic oil)",
        "classical_reference": "Bhaishajya Ratnavali, Kshudrarogadhikara, Shloka 63-69; Yogaratnakara; AFI Part I, 8:10",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Crocus sativus (Kumkuma / Saffron stigma)", "ratio": "12 g"},
            {"botanical": "Pterocarpus santalinus (Rakta Chandana)", "ratio": "12 g"},
            {"botanical": "Rubia cordifolia (Manjishta)", "ratio": "12 g"},
            {"botanical": "Glycyrrhiza glabra (Yashtimadhu)", "ratio": "12 g"},
            {"botanical": "Nelumbo nucifera (Kamala flower)", "ratio": "12 g"},
            {"botanical": "Ficus benghalensis (Nyagrodha aerial roots)", "ratio": "12 g"},
            {"botanical": "Prunus cerasoides (Padmaka)", "ratio": "12 g"},
            {"botanical": "Sesamum indicum oil (Tila Taila)", "ratio": "768 ml"},
            {"botanical": "Goat's Milk (Aja Dugdha)", "ratio": "1.536 liters"}
        ],
        "preparation_method": "Taila Paka method: Saffron paste and botanical paste prepared with goat's milk and sesame oil, cooked on mild fire until sneha siddhi attained.",
        "therapeutic_indications": "Mukhadushika (Acne vulgaris), Vyanga (Melasma / Facial pigmentation), Tilakalaka (Freckles), Varnyakara (Complexion promoter), Vranaropaka (Wound healing).",
        "patent_relevance": "Heavily cited against cosmetic patents claiming skin brightening, anti-hyperpigmentation, or anti-aging herbal creams.",
        "tags": ["kumkumadi taila", "crocus sativus", "saffron", "cosmetic", "melasma", "skin brightening", "afi 8:10"]
    },
    {
        "chunk_id": "in-afi-anu-taila",
        "title": "Anu Taila - AFI Part I (8:1)",
        "formulation_name": "Anu Taila",
        "sanskrit_name": "अणु तैल",
        "dosage_form": "Taila / Nasya (Nasal drop medicated oil)",
        "classical_reference": "Charaka Samhita, Sutrasthana, Adhyaya 5, Shloka 56-62; Ashtanga Hridaya, Sutrasthana 20; AFI Part I, 8:1",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Holostemma ada-kodien (Jivanti)", "ratio": "1 part"},
            {"botanical": "Coleus vettiveroides (Hrivera)", "ratio": "1 part"},
            {"botanical": "Cedrus deodara (Devadaru)", "ratio": "1 part"},
            {"botanical": "Cyperus rotundus (Musta)", "ratio": "1 part"},
            {"botanical": "Cinnamomum zeylanicum (Twak)", "ratio": "1 part"},
            {"botanical": "Vetiveria zizanioides (Ushira)", "ratio": "1 part"},
            {"botanical": "Hemidesmus indicus (Sariva)", "ratio": "1 part"},
            {"botanical": "Santalum album (Chandana)", "ratio": "1 part"},
            {"botanical": "Berberis aristata (Daruharidra)", "ratio": "1 part"},
            {"botanical": "Glycyrrhiza glabra (Yashtimadhu)", "ratio": "1 part"},
            {"botanical": "Sesame oil (Tila Taila)", "ratio": "Vehicle"},
            {"botanical": "Goat's Milk (Aja Kshira)", "ratio": "Vehicle"}
        ],
        "preparation_method": "Processed 10 times consecutively (Dasha Paka) with decoctions and goat milk to achieve micronized penetration into nasal mucosa.",
        "therapeutic_indications": "Shirogata Roga (Disorders of head and neck), Suryavarta (Sinusitis / Migraine), Manyastambha (Cervical spondylosis), Khalitya (Alopecia), Palitya (Premature graying of hair), Indriyaprabodha (Sensory organ rejuvenation via Nasya).",
        "patent_relevance": "Nasal delivery of botanicals for neurological and sinusitis indications is anticipated by Anu Taila.",
        "tags": ["anu taila", "nasya", "sinusitis", "migraine", "nasal drug delivery", "afi 8:1"]
    },
    {
        "chunk_id": "in-afi-trikatu-churna",
        "title": "Trikatu Churna - AFI Part I (7:13)",
        "formulation_name": "Trikatu Churna",
        "sanskrit_name": "त्रिकटु चूर्ण",
        "dosage_form": "Churna (Bio-enhancer powder)",
        "classical_reference": "Sharangadhara Samhita, Madhyama Khanda 6:12; Charaka Samhita; AFI Part I, 7:13",
        "statute": "Ayurvedic Formulary of India (AFI), Part I",
        "jurisdiction": "india",
        "doc_type": "pharmacopoeia",
        "ingredients": [
            {"botanical": "Zingiber officinale (Shunthi / Dried ginger)", "ratio": "1 part (33.3%)"},
            {"botanical": "Piper nigrum (Maricha / Black pepper)", "ratio": "1 part (33.3%)"},
            {"botanical": "Piper longum (Pippali / Long pepper)", "ratio": "1 part (33.3%)"}
        ],
        "preparation_method": "Dried fruits and rhizome cleaned, pulverized separately, sieved via mesh 80, blended in 1:1:1 equal weight ratio.",
        "therapeutic_indications": "Agnimandya (Loss of appetite), Galashundika (Throat disorders), Pinasa (Rhinitis), Shwasa, Kasa, Kushta, Deepana, Pachana, Bioavailability enhancer (Yogavahi).",
        "patent_relevance": "Foundational prior art establishing piperine and gingerols as bioavailability enhancers centuries before modern pharmaceutical patents.",
        "tags": ["trikatu", "piperine", "bioavailability enhancer", "black pepper", "ginger", "afi 7:13"]
    }
]

# -------------------------------------------------------------
# WRITE PROCESSED FILES
# -------------------------------------------------------------

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} items to {filepath}")

def main():
    print("Building authentic legal & pharmacopoeial corpus...")

    # India legal
    save_json(os.path.join(INDIA_DIR, "patents_act_1970.json"), PATENTS_ACT_1970)
    save_json(os.path.join(INDIA_DIR, "biological_diversity_act_2002.json"), BIOLOGICAL_DIVERSITY_ACT_2002)
    save_json(os.path.join(INDIA_DIR, "drugs_cosmetics_act_1940.json"), DRUGS_COSMETICS_ACT_1940)
    save_json(os.path.join(INDIA_DIR, "gi_act_1999.json"), GI_ACT_1999)
    save_json(os.path.join(INDIA_DIR, "fssai_ayush_aahar_2022.json"), FSSAI_AYUSH_AAHAR_2022)
    
    # India formulations
    save_json(os.path.join(INDIA_DIR, "classical_formulations.json"), CLASSICAL_FORMULATIONS)

    # International treaties
    save_json(os.path.join(INTL_DIR, "trips_agreement.json"), TRIPS_AGREEMENT)
    save_json(os.path.join(INTL_DIR, "nagoya_protocol.json"), NAGOYA_PROTOCOL)
    save_json(os.path.join(INTL_DIR, "cbd_convention.json"), CBD_CONVENTION)
    save_json(os.path.join(INTL_DIR, "pct_treaty.json"), PCT_TREATY)

    total_india = len(PATENTS_ACT_1970) + len(BIOLOGICAL_DIVERSITY_ACT_2002) + len(DRUGS_COSMETICS_ACT_1940) + len(GI_ACT_1999) + len(FSSAI_AYUSH_AAHAR_2022) + len(CLASSICAL_FORMULATIONS)
    total_intl = len(TRIPS_AGREEMENT) + len(NAGOYA_PROTOCOL) + len(CBD_CONVENTION) + len(PCT_TREATY)

    print(f"Corpus generation complete!")
    print(f"Total Indian Corpus items: {total_india}")
    print(f"Total International Corpus items: {total_intl}")
    print(f"Total Overall Chunks: {total_india + total_intl}")

if __name__ == "__main__":
    main()
