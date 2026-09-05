from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """A user with a daily calorie goal."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="User")
    daily_calorie_goal = Column(Integer, nullable=False, default=2000)
    created_at = Column(DateTime, default=datetime.utcnow)

    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")


class Meal(Base):
    """A single meal entry (breakfast, lunch, snack, or dinner)."""

    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_type = Column(
        String,
        nullable=False,
        # Enforce valid meal types at the DB level
    )
    timestamp = Column(DateTime, default=datetime.utcnow)
    total_calories = Column(Float, default=0.0)
    notes = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "meal_type IN ('breakfast', 'lunch', 'snack', 'dinner')",
            name="valid_meal_type",
        ),
    )

    user = relationship("User", back_populates="meals")
    food_items = relationship(
        "FoodItem", back_populates="meal", cascade="all, delete-orphan"
    )


class FoodItem(Base):
    """An individual food item within a meal."""

    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=True)
    calories = Column(Float, default=0.0)
    protein = Column(Float, default=0.0)
    carbs = Column(Float, default=0.0)
    fat = Column(Float, default=0.0)
    confidence = Column(Float, default=1.0)

    meal = relationship("Meal", back_populates="food_items")
