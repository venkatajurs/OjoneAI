"""
Placeholder AI service — for Developer 1.

Dev 1 will replace these functions with actual Gemini API calls
and USDA FoodData Central lookups.
"""


async def analyze_image(image_bytes: bytes) -> dict:
    """
    TODO (Dev 1): Send image to Gemini multimodal API.
    Return structured JSON with identified foods, portions, and calories.
    """
    raise NotImplementedError("Dev 1 will implement this")


async def search_usda(query: str) -> list[dict]:
    """
    TODO (Dev 1): Query USDA FoodData Central API.
    Return matching foods with nutrition data.
    """
    raise NotImplementedError("Dev 1 will implement this")
