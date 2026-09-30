const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export interface SourceReference {
  doc_id: string;
  doc_title: string;
  section_id: string;
  section_title: string;
  jurisdiction: string;
  citation_key: string;
  excerpt: string;
  relevance_score: number;
}

export interface QueryResponse {
  answer: string;
  language: string;
  jurisdiction: string;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  sources: SourceReference[];
  product_category?: string;
  disclaimer?: string;
}

export interface ClassificationOption {
  id: string;
  label_en: string;
  label_hi: string;
  next_question_id?: string;
  target_category?: string;
}

export interface ClassificationQuestion {
  question_id: string;
  title_en: string;
  title_hi: string;
  description_en?: string;
  description_hi?: string;
  options: ClassificationOption[];
}

export interface ClassificationResult {
  category: string;
  category_name_en: string;
  category_name_hi: string;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  reasoning: string;
  cited_rules: string[];
  regulatory_implications: string[];
  applicable_ip_instruments: string[];
  next_steps: string[];
}

export interface PriorArtMatch {
  id: string;
  name: string;
  sanskrit_name: string;
  source_text: string;
  afi_reference: string;
  category: string;
  ingredients: string[];
  indication: string;
  patentability_status: string;
  match_score: number;
  matched_ingredients: string[];
}

export interface PriorArtResponse {
  matches: PriorArtMatch[];
  summary_verdict: string;
  recommendation: string;
}

export async function sendQuery(
  query: string,
  jurisdiction: "india" | "international" | "both" = "india",
  language: string = "en",
  productCategory?: string
): Promise<QueryResponse> {
  const res = await fetch(`${API_BASE_URL}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      jurisdiction,
      language,
      product_category: productCategory,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to process query.");
  }
  return res.json();
}

export async function startClassification(): Promise<ClassificationQuestion> {
  const res = await fetch(`${API_BASE_URL}/api/classify/start`);
  if (!res.ok) throw new Error("Failed to start classification.");
  return res.json();
}

export async function submitClassificationAnswer(
  sessionId: string,
  questionId: string,
  optionId: string
): Promise<ClassificationQuestion | ClassificationResult> {
  const res = await fetch(`${API_BASE_URL}/api/classify/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      question_id: questionId,
      option_id: optionId,
    }),
  });
  if (!res.ok) throw new Error("Failed to submit classification answer.");
  return res.json();
}

export async function searchPriorArt(
  ingredients: string[],
  freeText?: string
): Promise<PriorArtResponse> {
  const res = await fetch(`${API_BASE_URL}/api/search/prior-art`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ingredients, free_text: freeText }),
  });
  if (!res.ok) throw new Error("Failed to search prior art.");
  return res.json();
}

export async function getPathwayRecommendation(category: string) {
  const res = await fetch(`${API_BASE_URL}/api/pathway/recommend/${category}`);
  if (!res.ok) throw new Error("Failed to fetch pathway recommendation.");
  return res.json();
}
