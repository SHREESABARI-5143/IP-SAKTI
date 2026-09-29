from fastapi import APIRouter
from app.models.schemas import PriorArtSearchRequest, PriorArtSearchResponse, PriorArtMatch
from app.services.vector_service import vector_service

router = APIRouter(prefix="/api/search", tags=["Prior-Art Search"])

@router.post("/prior-art", response_model=PriorArtSearchResponse)
def search_prior_art(req: PriorArtSearchRequest):
    """Search authoritative AFI/API classical formulation dataset for matching ingredients and prior art."""
    raw_matches = vector_service.search_prior_art(
        ingredients=req.ingredients,
        query_text=req.free_text or ""
    )

    matches = [PriorArtMatch(**m) for m in raw_matches]

    if matches and matches[0].match_score > 0.6:
        summary_verdict = f"High similarity prior-art found: '{matches[0].name}' in {matches[0].source_text}."
        recommendation = "Formulation exists in codified traditional knowledge. Direct patenting as a composition is barred under Patents Act Section 3(p). Focus on novel processing/extraction or trademarking."
    elif matches:
        summary_verdict = f"Partial similarity match found with {len(matches)} classical formulation(s)."
        recommendation = "Check component ratios and ingredient overlap before filing patent specification. Ensure NBA clearance for bio-resources."
    else:
        summary_verdict = "No direct match found in AFI top formulation database."
        recommendation = "Formulation appears novel in initial classical sample search. Perform comprehensive TKDL search before provisional patent filing."

    return PriorArtSearchResponse(
        matches=matches,
        summary_verdict=summary_verdict,
        recommendation=recommendation
    )
