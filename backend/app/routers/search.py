"""
Food search route — STUB for Developer 1.

This returns mock search results so the manual food entry
feature can be built. Dev 1 will integrate the USDA FoodData
Central API here.
"""

from fastapi import APIRouter
from app.schemas import FoodSearchQuery, FoodSearchResult

router = APIRouter(tags=["Food Search"])

# Simple mock database for demo purposes
_MOCK_FOODS: dict[str, FoodSearchResult] = {
    "egg": FoodSearchResult(
        name="Egg (boiled)", serving_size="1 large (50g)",
        calories=78, protein=6.3, carbs=0.6, fat=5.3, source="USDA",
    ),
    "rice": FoodSearchResult(
        name="White Rice (cooked)", serving_size="1 cup (158g)",
        calories=206, protein=4.3, carbs=44.5, fat=0.4, source="USDA",
    ),
    "roti": FoodSearchResult(
        name="Roti / Chapati", serving_size="1 medium (40g)",
        calories=104, protein=3.0, carbs=18.0, fat=2.5, source="USDA",
    ),
    "dal": FoodSearchResult(
        name="Dal (Lentil Curry)", serving_size="1 bowl (200ml)",
        calories=180, protein=9.0, carbs=28.0, fat=4.0, source="USDA",
    ),
    "chicken": FoodSearchResult(
        name="Chicken Breast (grilled)", serving_size="100g",
        calories=165, protein=31.0, carbs=0.0, fat=3.6, source="USDA",
    ),
    "paneer": FoodSearchResult(
        name="Paneer (Cottage Cheese)", serving_size="100g",
        calories=265, protein=18.3, carbs=1.2, fat=20.8, source="USDA",
    ),
    "banana": FoodSearchResult(
        name="Banana", serving_size="1 medium (118g)",
        calories=105, protein=1.3, carbs=27.0, fat=0.4, source="USDA",
    ),
    "milk": FoodSearchResult(
        name="Whole Milk", serving_size="1 cup (244ml)",
        calories=149, protein=8.0, carbs=12.0, fat=8.0, source="USDA",
    ),
    "idli": FoodSearchResult(
        name="Idli", serving_size="2 pieces",
        calories=130, protein=4.0, carbs=26.0, fat=0.5, source="USDA",
    ),
    "dosa": FoodSearchResult(
        name="Dosa (plain)", serving_size="1 medium",
        calories=133, protein=3.5, carbs=22.0, fat=3.5, source="USDA",
    ),
    "curd": FoodSearchResult(
        name="Curd / Yogurt", serving_size="1 cup (200g)",
        calories=100, protein=4.0, carbs=8.0, fat=5.0, source="USDA",
    ),
    "sambar": FoodSearchResult(
        name="Sambar", serving_size="1 bowl (200ml)",
        calories=130, protein=6.0, carbs=18.0, fat=3.0, source="USDA",
    ),
}


@router.post("/foods/search", response_model=list[FoodSearchResult])
def search_foods(payload: FoodSearchQuery):
    """
    Search for foods by name.

    **Currently uses a mock database.**
    Dev 1 will integrate the USDA FoodData Central API here.
    """
    query = payload.query.lower().strip()
    results = []
    for key, food in _MOCK_FOODS.items():
        if query in key or query in food.name.lower():
            results.append(food)
    return results
