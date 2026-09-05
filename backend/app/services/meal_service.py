"""Meal CRUD service — handles creating, reading, and deleting meals."""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Meal, FoodItem
from app.schemas import MealCreate


def create_meal(db: Session, user_id: int, payload: MealCreate) -> Meal:
    """Create a meal with its food items and compute total calories."""
    total_calories = sum(f.calories for f in payload.foods)

    meal = Meal(
        user_id=user_id,
        meal_type=payload.meal_type,
        total_calories=total_calories,
        notes=payload.notes,
    )
    db.add(meal)
    db.flush()  # get meal.id before adding food items

    for food in payload.foods:
        item = FoodItem(
            meal_id=meal.id,
            name=food.name,
            quantity=food.quantity,
            calories=food.calories,
            protein=food.protein,
            carbs=food.carbs,
            fat=food.fat,
            confidence=food.confidence,
        )
        db.add(item)

    db.commit()
    db.refresh(meal)
    return meal


def get_meals_today(db: Session, user_id: int) -> list[Meal]:
    """Get all meals logged today for a user (since midnight local time)."""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    return (
        db.query(Meal)
        .filter(
            Meal.user_id == user_id,
            Meal.timestamp >= today_start,
            Meal.timestamp < today_end,
        )
        .order_by(Meal.timestamp.asc())
        .all()
    )


def delete_meal(db: Session, meal_id: int, user_id: int) -> bool:
    """Delete a meal by ID. Returns True if deleted, False if not found."""
    meal = (
        db.query(Meal)
        .filter(Meal.id == meal_id, Meal.user_id == user_id)
        .first()
    )
    if not meal:
        return False
    db.delete(meal)
    db.commit()
    return True
