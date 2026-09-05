"""Seed the development database with the MVP's default user."""

from app.database import SessionLocal, init_db
from app.models import User


def seed_default_user() -> User:
    """Create user ID 1 for the demo if it does not already exist."""
    init_db()
    db = SessionLocal()
    try:
        user = db.get(User, 1)
        if user is None:
            user = User(id=1, name="Demo User", daily_calorie_goal=2000)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()


if __name__ == "__main__":
    user = seed_default_user()
    print(f"Default user ready: id={user.id}, goal={user.daily_calorie_goal} kcal")
