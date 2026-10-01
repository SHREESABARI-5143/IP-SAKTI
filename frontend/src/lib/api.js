const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "https://ip-sakti-backend-edge.shreesabari5143.workers.dev";

/**
 * Sends an IP legal or regulatory query to the Ayush RAG backend.
 * Grounded in authentic database records and vector corpus.
 * @param {string} query - The user query text
 * @param {"india" | "international" | "both"} jurisdiction - Legal jurisdiction filter
 * @param {string} language - ISO language code (en, hi, sa, ta, te, mr, bn, gu)
 * @param {string} [productCategory] - Optional product category filter
 * @param {string} [sessionId] - Optional session ID for conversation history
 */
export async function sendQuery(
  query,
  jurisdiction = "india",
  language = "en",
  productCategory = null,
  sessionId = null
) {
  const res = await fetch(`${API_BASE_URL}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      jurisdiction,
      language,
      product_category: productCategory,
      session_id: sessionId,
    }),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(
      errData.detail || `Legal query execution failed with status ${res.status}`
    );
  }

  return await res.json();
}

/**
 * Searches the classical formulation database (AFI/API) for matching prior art.
 * Queries actual Qdrant vector database and pharmacopoeia corpus.
 * @param {string[]} ingredients - List of botanical or formulation ingredients
 * @param {string} [freeText] - Free-text description or indication
 */
export async function searchPriorArt(ingredients, freeText = "") {
  const res = await fetch(`${API_BASE_URL}/api/search/prior-art`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ingredients,
      free_text: freeText,
    }),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(
      errData.detail || `Prior art database search failed with status ${res.status}`
    );
  }

  return await res.json();
}

/**
 * Initiates the 6-tier AYUSH product classification flow from the backend statutory engine.
 */
export async function startClassification() {
  const res = await fetch(`${API_BASE_URL}/api/classify/start`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(
      errData.detail || `Failed to initiate classification flow: status ${res.status}`
    );
  }
  return await res.json();
}

/**
 * Submits an answer to a classification question to process the next step or final categorization.
 * @param {string} sessionId
 * @param {string} questionId
 * @param {string} optionId
 */
export async function submitClassificationAnswer(sessionId, questionId, optionId) {
  const res = await fetch(`${API_BASE_URL}/api/classify/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      question_id: questionId,
      option_id: optionId,
    }),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(
      errData.detail || `Classification answer submission failed with status ${res.status}`
    );
  }

  return await res.json();
}

/**
 * Fetches statutory IP pathway recommendations and fee structures for a specific category.
 * @param {string} category
 */
export async function getPathwayRecommendation(category) {
  const res = await fetch(`${API_BASE_URL}/api/pathway/recommend/${category}`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(
      errData.detail || `Pathway retrieval failed with status ${res.status}`
    );
  }
  return await res.json();
}
