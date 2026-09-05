"""User management routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut, CalorieGoalUpdate

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    user = User(name=payload.name, daily_calorie_goal=payload.daily_calorie_goal)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}/calorie-goal", response_model=UserOut)
def update_calorie_goal(
    user_id: int,
    payload: CalorieGoalUpdate,
    db: Session = Depends(get_db),
):
    """Set or update a user's daily calorie goal."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.daily_calorie_goal = payload.daily_calorie_goal
    db.commit()
    db.refresh(user)
    return user
