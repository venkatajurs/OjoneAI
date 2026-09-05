"""
Calorie Coach Service — The core intelligence of OjoneAI.

This module implements:
1. Daily calorie summary & progress tracking
2. Dynamic meal budget redistribution
3. Smart "What should I eat next?" recommendations
4. Contextual coaching messages

All logic is deterministic (no ML) for the hackathon MVP.
"""

from __future__ import annotations

from app.models import User, Meal
from app.schemas import (
    DashboardResponse,
    MealBudget,
    MealOut,
    UserOut,
    RecommendationResponse,
    MealSuggestion,
    RecommendedItem,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Default calorie distribution across meal types (must sum to 1.0)
MEAL_BUDGET_RATIOS: dict[str, float] = {
    "breakfast": 0.25,
    "lunch": 0.35,
    "snack": 0.10,
    "dinner": 0.30,
}

# Ordered meal sequence — used to determine "next" meal
MEAL_ORDER: list[str] = ["breakfast", "lunch", "snack", "dinner"]

# ---------------------------------------------------------------------------
# Curated meal suggestions — diverse options for the recommendation engine.
# Each suggestion includes itemized foods with macros for a realistic demo.
# ---------------------------------------------------------------------------

MEAL_SUGGESTIONS: dict[str, list[dict]] = {
    "breakfast": [
        {
            "name": "Oats with Banana & Honey",
            "total_calories": 350,
            "items": [
                {"name": "Oats (cooked)", "calories": 180, "protein": 6.0, "carbs": 30.0, "fat": 3.5},
                {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27.0, "fat": 0.4},
                {"name": "Honey (1 tbsp)", "calories": 65, "protein": 0.0, "carbs": 17.0, "fat": 0.0},
            ],
        },
        {
            "name": "2 Idli + Sambar + Chutney",
            "total_calories": 300,
            "items": [
                {"name": "Idli (2 pcs)", "calories": 130, "protein": 4.0, "carbs": 26.0, "fat": 0.5},
                {"name": "Sambar (1 bowl)", "calories": 130, "protein": 6.0, "carbs": 18.0, "fat": 3.0},
                {"name": "Coconut Chutney", "calories": 40, "protein": 0.5, "carbs": 2.0, "fat": 3.0},
            ],
        },
        {
            "name": "Bread Toast with Eggs",
            "total_calories": 320,
            "items": [
                {"name": "Whole Wheat Toast (2 slices)", "calories": 160, "protein": 6.0, "carbs": 26.0, "fat": 2.0},
                {"name": "Boiled Egg (2)", "calories": 156, "protein": 12.6, "carbs": 1.2, "fat": 10.6},
            ],
        },
        {
            "name": "Poha with Peanuts",
            "total_calories": 280,
            "items": [
                {"name": "Poha (flattened rice)", "calories": 200, "protein": 4.0, "carbs": 40.0, "fat": 2.0},
                {"name": "Peanuts (handful)", "calories": 80, "protein": 3.5, "carbs": 2.5, "fat": 7.0},
            ],
        },
        {
            "name": "Dosa + Chutney",
            "total_calories": 200,
            "items": [
                {"name": "Plain Dosa", "calories": 133, "protein": 3.5, "carbs": 22.0, "fat": 3.5},
                {"name": "Coconut Chutney", "calories": 40, "protein": 0.5, "carbs": 2.0, "fat": 3.0},
                {"name": "Sambar (small)", "calories": 27, "protein": 1.5, "carbs": 4.0, "fat": 0.5},
            ],
        },
    ],
    "lunch": [
        {
            "name": "Rice + Dal + Sabzi",
            "total_calories": 550,
            "items": [
                {"name": "White Rice (1 cup)", "calories": 206, "protein": 4.3, "carbs": 44.5, "fat": 0.4},
                {"name": "Dal (1 bowl)", "calories": 180, "protein": 9.0, "carbs": 28.0, "fat": 4.0},
                {"name": "Mixed Veg Sabzi", "calories": 120, "protein": 3.0, "carbs": 12.0, "fat": 6.0},
                {"name": "Curd (small)", "calories": 50, "protein": 2.0, "carbs": 4.0, "fat": 2.5},
            ],
        },
        {
            "name": "2 Rotis + Chicken Curry",
            "total_calories": 520,
            "items": [
                {"name": "Roti (2 medium)", "calories": 200, "protein": 6.0, "carbs": 36.0, "fat": 3.0},
                {"name": "Chicken Curry (1 serving)", "calories": 250, "protein": 25.0, "carbs": 8.0, "fat": 12.0},
                {"name": "Salad", "calories": 30, "protein": 1.0, "carbs": 6.0, "fat": 0.2},
                {"name": "Buttermilk", "calories": 40, "protein": 2.0, "carbs": 4.0, "fat": 1.5},
            ],
        },
        {
            "name": "Rajma Chawal",
            "total_calories": 500,
            "items": [
                {"name": "Rajma (Kidney Bean Curry)", "calories": 210, "protein": 10.0, "carbs": 30.0, "fat": 5.0},
                {"name": "White Rice (1 cup)", "calories": 206, "protein": 4.3, "carbs": 44.5, "fat": 0.4},
                {"name": "Onion Salad", "calories": 25, "protein": 0.5, "carbs": 5.0, "fat": 0.1},
                {"name": "Pickle (small)", "calories": 15, "protein": 0.2, "carbs": 2.0, "fat": 0.5},
            ],
        },
        {
            "name": "Chole + 2 Rotis",
            "total_calories": 480,
            "items": [
                {"name": "Chole (Chickpea Curry)", "calories": 220, "protein": 9.0, "carbs": 30.0, "fat": 7.0},
                {"name": "Roti (2 medium)", "calories": 200, "protein": 6.0, "carbs": 36.0, "fat": 3.0},
                {"name": "Raita", "calories": 60, "protein": 2.0, "carbs": 4.0, "fat": 3.0},
            ],
        },
        {
            "name": "Light Veg Wrap",
            "total_calories": 350,
            "items": [
                {"name": "Whole Wheat Wrap", "calories": 130, "protein": 4.0, "carbs": 22.0, "fat": 3.0},
                {"name": "Paneer Filling", "calories": 150, "protein": 10.0, "carbs": 3.0, "fat": 10.0},
                {"name": "Veggies & Chutney", "calories": 70, "protein": 1.5, "carbs": 10.0, "fat": 2.0},
            ],
        },
    ],
    "snack": [
        {
            "name": "Fruit Bowl",
            "total_calories": 150,
            "items": [
                {"name": "Apple (1 medium)", "calories": 95, "protein": 0.5, "carbs": 25.0, "fat": 0.3},
                {"name": "Handful of Almonds (6-8)", "calories": 55, "protein": 2.0, "carbs": 2.0, "fat": 5.0},
            ],
        },
        {
            "name": "Tea + Biscuits",
            "total_calories": 120,
            "items": [
                {"name": "Tea with Milk", "calories": 50, "protein": 1.5, "carbs": 5.0, "fat": 2.0},
                {"name": "Digestive Biscuits (3)", "calories": 70, "protein": 1.0, "carbs": 12.0, "fat": 2.5},
            ],
        },
        {
            "name": "Sprouts Chaat",
            "total_calories": 180,
            "items": [
                {"name": "Sprouts (boiled)", "calories": 120, "protein": 8.0, "carbs": 18.0, "fat": 1.0},
                {"name": "Onion, Tomato, Lemon", "calories": 30, "protein": 0.5, "carbs": 6.0, "fat": 0.2},
                {"name": "Chaat Masala", "calories": 5, "protein": 0.0, "carbs": 1.0, "fat": 0.0},
                {"name": "Sev Topping", "calories": 25, "protein": 0.5, "carbs": 3.0, "fat": 1.5},
            ],
        },
        {
            "name": "Banana + Peanut Butter",
            "total_calories": 200,
            "items": [
                {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27.0, "fat": 0.4},
                {"name": "Peanut Butter (1 tbsp)", "calories": 95, "protein": 4.0, "carbs": 3.0, "fat": 8.0},
            ],
        },
        {
            "name": "Makhana (Fox Nuts)",
            "total_calories": 100,
            "items": [
                {"name": "Roasted Makhana (1 cup)", "calories": 100, "protein": 3.0, "carbs": 18.0, "fat": 0.5},
            ],
        },
    ],
    "dinner": [
        {
            "name": "2 Rotis + Dal + Sabzi",
            "total_calories": 500,
            "items": [
                {"name": "Roti (2 medium)", "calories": 200, "protein": 6.0, "carbs": 36.0, "fat": 3.0},
                {"name": "Dal (1 bowl)", "calories": 180, "protein": 9.0, "carbs": 28.0, "fat": 4.0},
                {"name": "Mixed Veg Sabzi", "calories": 120, "protein": 3.0, "carbs": 12.0, "fat": 6.0},
            ],
        },
        {
            "name": "Khichdi + Curd",
            "total_calories": 350,
            "items": [
                {"name": "Moong Dal Khichdi", "calories": 250, "protein": 8.0, "carbs": 40.0, "fat": 5.0},
                {"name": "Curd (1 cup)", "calories": 100, "protein": 4.0, "carbs": 8.0, "fat": 5.0},
            ],
        },
        {
            "name": "Paneer Tikka + Roti",
            "total_calories": 450,
            "items": [
                {"name": "Paneer Tikka (6 pcs)", "calories": 250, "protein": 16.0, "carbs": 6.0, "fat": 18.0},
                {"name": "Roti (2 medium)", "calories": 200, "protein": 6.0, "carbs": 36.0, "fat": 3.0},
            ],
        },
        {
            "name": "Veg Pulao + Raita",
            "total_calories": 400,
            "items": [
                {"name": "Veg Pulao (1 plate)", "calories": 300, "protein": 6.0, "carbs": 50.0, "fat": 8.0},
                {"name": "Raita", "calories": 60, "protein": 2.0, "carbs": 4.0, "fat": 3.0},
                {"name": "Papad", "calories": 40, "protein": 2.0, "carbs": 6.0, "fat": 1.0},
            ],
        },
        {
            "name": "Light Soup + Bread",
            "total_calories": 250,
            "items": [
                {"name": "Tomato Soup", "calories": 120, "protein": 2.0, "carbs": 18.0, "fat": 4.0},
                {"name": "Bread Roll (1)", "calories": 80, "protein": 2.5, "carbs": 15.0, "fat": 1.0},
                {"name": "Salad", "calories": 50, "protein": 1.0, "carbs": 8.0, "fat": 1.0},
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# Dashboard Builder
# ---------------------------------------------------------------------------

def build_dashboard(user: User, meals_today: list[Meal]) -> DashboardResponse:
    """
    Build the complete daily dashboard response.

    Calculates consumed/remaining calories, progress percentage,
    and dynamically redistributes the remaining calorie budget
    across unlogged meal slots.
    """
    goal = user.daily_calorie_goal
    total_consumed = sum(m.total_calories for m in meals_today)
    remaining = max(goal - total_consumed, 0)
    progress_pct = round((total_consumed / goal) * 100, 1) if goal > 0 else 0.0

    # Which meal types have been logged already?
    logged_types = {m.meal_type for m in meals_today}
    remaining_types = [t for t in MEAL_ORDER if t not in logged_types]

    # Redistribute remaining calories proportionally across unlogged meals
    remaining_weight = sum(MEAL_BUDGET_RATIOS[t] for t in remaining_types)
    meal_budgets: list[MealBudget] = []
    for meal_type in remaining_types:
        if remaining_weight > 0:
            share = MEAL_BUDGET_RATIOS[meal_type] / remaining_weight
            suggested = round(remaining * share)
        else:
            suggested = 0
        meal_budgets.append(
            MealBudget(meal_type=meal_type, suggested_calories=suggested)
        )

    # Serialize meals
    meals_out = [
        MealOut(
            id=m.id,
            meal_type=m.meal_type,
            timestamp=m.timestamp,
            total_calories=m.total_calories,
            notes=m.notes,
            food_items=[
                {
                    "id": fi.id,
                    "name": fi.name,
                    "quantity": fi.quantity,
                    "calories": fi.calories,
                    "protein": fi.protein,
                    "carbs": fi.carbs,
                    "fat": fi.fat,
                    "confidence": fi.confidence,
                }
                for fi in m.food_items
            ],
        )
        for m in meals_today
    ]

    return DashboardResponse(
        user=UserOut(
            id=user.id,
            name=user.name,
            daily_calorie_goal=user.daily_calorie_goal,
        ),
        goal=goal,
        consumed=round(total_consumed, 1),
        remaining=round(remaining, 1),
        progress_pct=progress_pct,
        meals_today=meals_out,
        remaining_meal_budgets=meal_budgets,
    )


# ---------------------------------------------------------------------------
# Recommendation Engine
# ---------------------------------------------------------------------------

def _determine_next_meal(logged_types: set[str]) -> str:
    """Determine which meal type to recommend next based on what's logged."""
    for meal_type in MEAL_ORDER:
        if meal_type not in logged_types:
            return meal_type
    # All meals logged — suggest a lighter option
    return "snack"


def _generate_coaching_message(
    remaining: float,
    goal: int,
    next_meal: str,
    consumed: float,
) -> str:
    """
    Generate a dynamic, context-aware coaching message.

    Adjusts tone and advice based on the user's progress:
    - Well under budget  → encourage a hearty meal
    - On track           → balanced encouragement
    - Slightly over      → gentle nudge toward lighter options
    - Significantly over → supportive, non-judgmental reminder
    """
    pct_consumed = (consumed / goal) * 100 if goal > 0 else 0

    if consumed == 0:
        return (
            f"Good morning! You have {goal} kcal to work with today. "
            f"Start with a nutritious {next_meal} to fuel your day! 🌅"
        )

    if remaining <= 0:
        over_by = abs(remaining)
        return (
            f"You've reached your daily goal of {goal} kcal "
            f"(over by ~{round(over_by)} kcal). "
            f"If you're still hungry, opt for something very light "
            f"like a salad or some fruit. No worries — tomorrow's a fresh start! 💪"
        )

    if remaining < 200:
        return (
            f"You're almost at your daily goal with only ~{round(remaining)} kcal remaining. "
            f"A light {next_meal} like a fruit bowl or a cup of soup would be perfect. 🍃"
        )

    if pct_consumed > 75:
        return (
            f"You've consumed {round(consumed)} kcal so far ({round(pct_consumed)}% of your goal). "
            f"You have ~{round(remaining)} kcal remaining. "
            f"A lighter {next_meal} would keep you comfortably within your target. ✨"
        )

    if pct_consumed > 50:
        return (
            f"You're doing great! {round(consumed)} kcal consumed, "
            f"~{round(remaining)} kcal remaining. "
            f"A balanced {next_meal} around {round(remaining * 0.5)}–{round(remaining * 0.7)} kcal "
            f"would be a solid choice. 🎯"
        )

    # Under 50% consumed
    return (
        f"You still have plenty of room today — ~{round(remaining)} kcal remaining. "
        f"Make sure to eat a hearty {next_meal} to stay energized! 🔥"
    )


def _filter_and_rank_suggestions(
    suggestions: list[dict],
    budget: float,
    logged_food_names: set[str],
    tolerance: float = 0.20,
) -> list[dict]:
    """
    Filter meal suggestions to fit within the calorie budget and
    rank them by fitness and diversity.

    - Filters out meals exceeding budget by more than `tolerance` (20%)
    - Penalizes meals containing foods the user already ate today
    - Sorts by calorie proximity to budget (closest first)
    """
    max_allowed = budget * (1 + tolerance)
    candidates: list[tuple[float, dict]] = []

    for suggestion in suggestions:
        total = suggestion["total_calories"]
        if total > max_allowed:
            continue

        # Score: lower is better
        # Primary: distance from budget (prefer meals that use most of budget)
        calorie_distance = abs(budget - total) / max(budget, 1)

        # Secondary: penalize if the user already ate similar foods
        item_names = {item["name"].lower() for item in suggestion["items"]}
        overlap = len(item_names & logged_food_names)
        diversity_penalty = overlap * 0.3

        score = calorie_distance + diversity_penalty
        candidates.append((score, suggestion))

    # Sort by score (lower = better fit)
    candidates.sort(key=lambda x: x[0])
    return [c[1] for c in candidates]


def get_recommendation(user: User, meals_today: list[Meal]) -> RecommendationResponse:
    """
    Generate the "What should I eat next?" recommendation.

    1. Calculate remaining calories
    2. Determine the next meal type
    3. Compute a budget for that meal
    4. Filter curated suggestions to fit the budget
    5. Generate a coaching message
    6. Return top 2-3 suggestions
    """
    goal = user.daily_calorie_goal
    total_consumed = sum(m.total_calories for m in meals_today)
    remaining = max(goal - total_consumed, 0)

    logged_types = {m.meal_type for m in meals_today}
    next_meal = _determine_next_meal(logged_types)

    # Calculate the budget for the next meal
    remaining_types = [t for t in MEAL_ORDER if t not in logged_types]
    remaining_weight = sum(MEAL_BUDGET_RATIOS[t] for t in remaining_types)

    if remaining_weight > 0 and remaining > 0:
        meal_budget = remaining * (MEAL_BUDGET_RATIOS[next_meal] / remaining_weight)
    elif remaining > 0:
        meal_budget = remaining  # last meal gets everything
    else:
        meal_budget = 150  # minimal budget when over goal

    # Collect food names already eaten today (for diversity)
    logged_food_names: set[str] = set()
    for meal in meals_today:
        for fi in meal.food_items:
            logged_food_names.add(fi.name.lower())

    # Filter and rank suggestions
    available = MEAL_SUGGESTIONS.get(next_meal, [])
    ranked = _filter_and_rank_suggestions(
        available, meal_budget, logged_food_names
    )

    # Take top 3
    top_suggestions = ranked[:3]

    # Fallback: if no suggestions fit, take the lightest available option
    if not top_suggestions and available:
        lightest = min(available, key=lambda s: s["total_calories"])
        top_suggestions = [lightest]

    # Build response
    coaching_message = _generate_coaching_message(
        remaining=remaining,
        goal=goal,
        next_meal=next_meal,
        consumed=total_consumed,
    )

    suggestion_models = [
        MealSuggestion(
            name=s["name"],
            meal_type=next_meal,
            total_calories=s["total_calories"],
            items=[
                RecommendedItem(
                    name=item["name"],
                    calories=item["calories"],
                    protein=item.get("protein", 0),
                    carbs=item.get("carbs", 0),
                    fat=item.get("fat", 0),
                )
                for item in s["items"]
            ],
        )
        for s in top_suggestions
    ]

    return RecommendationResponse(
        remaining_calories=round(remaining, 1),
        next_meal_type=next_meal,
        coaching_message=coaching_message,
        suggestions=suggestion_models,
    )
