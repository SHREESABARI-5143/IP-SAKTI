-- IP-SAKTI Cloudflare D1 Database Schema
-- Run with: npx wrangler d1 execute ip-sakti-db --file=schema_d1.sql --config wrangler.edge.toml

CREATE TABLE IF NOT EXISTS corpus_chunks (
    chunk_id TEXT PRIMARY KEY,
    statute TEXT NOT NULL,
    section_or_article TEXT NOT NULL,
    title TEXT,
    jurisdiction TEXT DEFAULT 'India',
    doc_type TEXT DEFAULT 'statute',
    url TEXT NOT NULL,
    text_content TEXT NOT NULL,
    indexed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS graph_edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_chunk_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    label TEXT NOT NULL,
    target_chunk_id TEXT,
    FOREIGN KEY(source_chunk_id) REFERENCES corpus_chunks(chunk_id)
);

CREATE TABLE IF NOT EXISTS query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    jurisdiction TEXT,
    response TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Seed Baseline Ayurvedic IP Statutory Provisions
INSERT OR IGNORE INTO corpus_chunks (chunk_id, statute, section_or_article, title, jurisdiction, doc_type, url, text_content)
VALUES 
(
    'in_patents_act_1970_sec_3p',
    'The Patents Act, 1970',
    'Section 3(p)',
    'Traditional Knowledge Patent Exclusions',
    'India',
    'statute',
    'https://www.indiacode.nic.in/show-data?actid=AC_CEN_3_44_00007_197039_1517807323983&sectionId=15154&sectionno=3&orderno=3',
    'An invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not patentable.'
),
(
    'in_patents_act_1970_sec_3j',
    'The Patents Act, 1970',
    'Section 3(j)',
    'Plants and Animals Exclusions',
    'India',
    'statute',
    'https://www.indiacode.nic.in/show-data?actid=AC_CEN_3_44_00007_197039_1517807323983&sectionId=15154&sectionno=3&orderno=3',
    'Plants and animals in whole or any part thereof other than micro-organisms but including seeds, varieties and species and essentially biological processes for production or propagation of plants and animals are not patentable inventions.'
),
(
    'in_biodiversity_act_2002_sec_6',
    'Biological Diversity Act, 2002',
    'Section 6',
    'Mandatory NBA Approval for IP Filing',
    'India',
    'statute',
    'http://nbaindia.org/content/26/59/1/rules.html',
    'No person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the previous approval of the National Biodiversity Authority.'
);

-- Seed Baseline Knowledge Graph Edges
INSERT OR IGNORE INTO graph_edges (source_chunk_id, edge_type, label, target_chunk_id)
VALUES
('in_patents_act_1970_sec_3p', 'CROSS_REFERENCES', 'Requires biological source clearance under Biological Diversity Act 2002', 'in_biodiversity_act_2002_sec_6'),
('in_biodiversity_act_2002_sec_6', 'MANDATES', 'Prior NBA approval mandatory before patent filing', 'in_patents_act_1970_sec_3p');
