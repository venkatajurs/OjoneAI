# OjoneAI 🍽️

**AI-powered Food Tracking & Calorie Coaching Assistant**

> Instead of manually tracking every calorie, simply take a picture of your food. The AI estimates the meal, logs it, tracks your remaining calorie budget, and helps you decide what to eat next.

## Core Features

1. **AI Food Image Calorie Estimator** — Upload a meal photo → AI identifies foods → estimates calories → user confirms → logged
2. **Smart Calorie Coach** — Tracks daily progress → recommends what to eat next → stays within your goal

## Architecture

```
frontend/        → React UI (Dev 3)
backend/         → FastAPI + SQLite (Dev 2)
  app/
    routers/     → API endpoints
    services/    → Business logic (calorie coach, meal service)
    models.py    → SQLAlchemy ORM models
    schemas.py   → Pydantic request/response schemas
```

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env          # Edit with your API keys
python -m app.seed            # Create the default demo user (id=1)
uvicorn app.main:app --reload --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Run the Phase 2 API checks with `python -m unittest discover -s tests` from
the `backend` directory.

### Frontend

```bash
cd frontend
# Dev 3 will set up the frontend framework here
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/user/` | Create a new user |
| `GET` | `/user/{id}` | Get user details |
| `PUT` | `/user/{id}/calorie-goal` | Set daily calorie goal |
| `POST` | `/meals/?user_id=` | Log a meal with food items |
| `GET` | `/meals/today?user_id=` | Today's meal log |
| `DELETE` | `/meals/{id}?user_id=` | Delete a meal |
| `GET` | `/dashboard?user_id=` | Full daily calorie dashboard |
| `POST` | `/recommendation?user_id=` | AI Coach meal suggestions |
| `POST` | `/analyze-food-image` | Image → calorie estimate (stub) |
| `POST` | `/foods/search` | Search food database (stub) |

## Team

| Role | Responsibility |
|------|---------------|
| Dev 1 | AI/Image Pipeline — Gemini multimodal + USDA API |
| Dev 2 | Backend/Data — FastAPI, SQLite, Calorie Coach Logic |
| Dev 3 | Frontend/UI — Dashboard, image upload, calorie progress |

## Environment Variables

```env
GEMINI_API_KEY=your_key       # Google AI Studio (free)
USDA_API_KEY=your_key         # USDA FoodData Central (free)
DATABASE_URL=sqlite:///./ojone.db
```

## License

Hackathon project — BMSCE 7th Semester
