"""Pydantic schemas for request/response validation."""

from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Food Item
# ---------------------------------------------------------------------------

class FoodItemBase(BaseModel):
    name: str
    quantity: str | None = None
    calories: float = 0.0
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0
    confidence: float = 1.0


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemOut(FoodItemBase):
    id: int

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Meal
# ---------------------------------------------------------------------------

class MealCreate(BaseModel):
    meal_type: str = Field(
        ..., pattern="^(breakfast|lunch|snack|dinner)$",
        description="One of: breakfast, lunch, snack, dinner",
    )
    foods: list[FoodItemCreate]
    notes: str | None = None


class MealOut(BaseModel):
    id: int
    meal_type: str
    timestamp: datetime
    total_calories: float
    notes: str | None = None
    food_items: list[FoodItemOut] = []

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str = "User"
    daily_calorie_goal: int = 2000


class UserOut(BaseModel):
    id: int
    name: str
    daily_calorie_goal: int

    model_config = {"from_attributes": True}


class CalorieGoalUpdate(BaseModel):
    daily_calorie_goal: int = Field(..., gt=0, le=10000)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class MealBudget(BaseModel):
    meal_type: str
    suggested_calories: int


class DashboardResponse(BaseModel):
    user: UserOut
    goal: int
    consumed: float
    remaining: float
    progress_pct: float
    meals_today: list[MealOut]
    remaining_meal_budgets: list[MealBudget]


# ---------------------------------------------------------------------------
# Recommendation
# ---------------------------------------------------------------------------

class RecommendedItem(BaseModel):
    name: str
    calories: int
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0


class MealSuggestion(BaseModel):
    name: str
    meal_type: str
    total_calories: int
    items: list[RecommendedItem]


class RecommendationResponse(BaseModel):
    remaining_calories: float
    next_meal_type: str
    coaching_message: str
    suggestions: list[MealSuggestion]


# ---------------------------------------------------------------------------
# AI Analysis (stub schemas for Dev 1)
# ---------------------------------------------------------------------------

class AnalyzedFood(BaseModel):
    name: str
    quantity: str
    estimated_calories: int
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0
    confidence: float = 0.8


class AnalysisResponse(BaseModel):
    foods: list[AnalyzedFood]
    total_calories: int
    disclaimer: str = (
        "These are approximate estimates based on image analysis. "
        "Actual values may vary."
    )


class FoodSearchQuery(BaseModel):
    query: str


class FoodSearchResult(BaseModel):
    name: str
    serving_size: str
    calories: float
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0
    source: str = "database"
