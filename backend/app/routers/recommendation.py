"""Recommendation route — "What should I eat next?" """

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import RecommendationResponse
from app.services.meal_service import get_meals_today
from app.services.calorie_coach import get_recommendation

router = APIRouter(tags=["Recommendation"])


@router.post("/recommendation", response_model=RecommendationResponse)
def recommend_next_meal(
    user_id: int = Query(..., description="The user's ID"),
    db: Session = Depends(get_db),
):
    """
    Generate a smart meal recommendation based on:
    - Remaining calorie budget
    - Which meals have already been logged
    - Previously eaten foods (for variety)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meals_today = get_meals_today(db, user_id=user_id)
    return get_recommendation(user, meals_today)
