"""
Food image analysis route — STUB for Developer 1.

This returns mock data so the frontend can be built and tested
independently. Dev 1 will replace the mock logic with actual
Gemini multimodal API calls.
"""

from fastapi import APIRouter, File, UploadFile
from app.schemas import AnalysisResponse, AnalyzedFood

router = APIRouter(tags=["AI Analysis"])


@router.post("/analyze-food-image", response_model=AnalysisResponse)
async def analyze_food_image(image: UploadFile = File(...)):
    """
    Analyze a food image and return estimated nutrition info.

    **Currently returns mock data.**
    Dev 1 will integrate the Gemini multimodal API here.
    """
    # Read the image bytes (so the upload doesn't error out)
    _ = await image.read()

    # --- MOCK RESPONSE ---
    mock_foods = [
        AnalyzedFood(
            name="Roti",
            quantity="2 medium",
            estimated_calories=200,
            protein=6.0,
            carbs=36.0,
            fat=3.0,
            confidence=0.85,
        ),
        AnalyzedFood(
            name="Dal (Lentil Curry)",
            quantity="1 bowl (~200ml)",
            estimated_calories=180,
            protein=9.0,
            carbs=28.0,
            fat=4.0,
            confidence=0.80,
        ),
        AnalyzedFood(
            name="Paneer Butter Masala",
            quantity="1 serving (~150g)",
            estimated_calories=250,
            protein=12.0,
            carbs=10.0,
            fat=18.0,
            confidence=0.75,
        ),
    ]

    return AnalysisResponse(
        foods=mock_foods,
        total_calories=sum(f.estimated_calories for f in mock_foods),
    )
