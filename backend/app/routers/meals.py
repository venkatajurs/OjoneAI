"""Meal logging routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import MealCreate, MealOut
from app.services.meal_service import (
    create_meal,
    get_meals_today,
    delete_meal,
)

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.post("/", response_model=MealOut, status_code=201)
def log_meal(
    payload: MealCreate,
    user_id: int = Query(..., description="The user's ID"),
    db: Session = Depends(get_db),
):
    """Log a new meal with its food items."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    meal = create_meal(db, user_id=user_id, payload=payload)
    return meal


@router.get("/today", response_model=list[MealOut])
def list_meals_today(
    user_id: int = Query(..., description="The user's ID"),
    db: Session = Depends(get_db),
):
    """Get all meals logged today for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_meals_today(db, user_id=user_id)


@router.delete("/{meal_id}", status_code=204)
def remove_meal(
    meal_id: int,
    user_id: int = Query(..., description="The user's ID"),
    db: Session = Depends(get_db),
):
    """Delete a meal by ID."""
    success = delete_meal(db, meal_id=meal_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meal not found")
    return None
