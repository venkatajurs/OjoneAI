"""Dashboard route — returns the full daily calorie summary."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import DashboardResponse
from app.services.meal_service import get_meals_today
from app.services.calorie_coach import build_dashboard

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    user_id: int = Query(..., description="The user's ID"),
    db: Session = Depends(get_db),
):
    """
    Get the full daily dashboard for a user:
    - Goal, consumed, remaining calories
    - Progress percentage
    - Today's meals
    - Budget suggestions for remaining meals
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meals_today = get_meals_today(db, user_id=user_id)
    return build_dashboard(user, meals_today)
