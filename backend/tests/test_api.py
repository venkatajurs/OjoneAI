"""End-to-end API checks for the Phase 2 calorie-coach flow."""

import os
import tempfile
import unittest
from pathlib import Path


class CalorieCoachApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls.temp_dir.name) / "test_ojone.db"
        os.environ["DATABASE_URL"] = f"sqlite:///{db_path.as_posix()}"

        # Imports happen after DATABASE_URL is configured.
        from fastapi.testclient import TestClient
        from app.database import engine
        from app.main import app

        cls.engine = engine
        cls.client_context = TestClient(app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client_context.__exit__(None, None, None)
        cls.engine.dispose()
        cls.temp_dir.cleanup()

    def create_user(self) -> int:
        response = self.client.post(
            "/user/", json={"name": "Test User", "daily_calorie_goal": 2000}
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()["id"]

    def test_complete_calorie_coach_flow(self):
        user_id = self.create_user()

        response = self.client.get(f"/user/{user_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["name"], "Test User")

        response = self.client.put(
            f"/user/{user_id}/calorie-goal", json={"daily_calorie_goal": 2200}
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["daily_calorie_goal"], 2200)

        response = self.client.post(
            f"/meals/?user_id={user_id}",
            json={
                "meal_type": "breakfast",
                "foods": [
                    {"name": "Oats", "calories": 180},
                    {"name": "Banana", "calories": 105},
                ],
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        meal_id = response.json()["id"]
        self.assertEqual(response.json()["total_calories"], 285)

        response = self.client.get(f"/meals/today?user_id={user_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(f"/dashboard?user_id={user_id}")
        self.assertEqual(response.status_code, 200, response.text)
        dashboard = response.json()
        self.assertEqual(dashboard["goal"], 2200)
        self.assertEqual(dashboard["consumed"], 285)
        self.assertEqual(dashboard["remaining"], 1915)
        self.assertEqual(
            {budget["meal_type"] for budget in dashboard["remaining_meal_budgets"]},
            {"lunch", "snack", "dinner"},
        )

        response = self.client.post(f"/recommendation?user_id={user_id}")
        self.assertEqual(response.status_code, 200, response.text)
        recommendation = response.json()
        self.assertEqual(recommendation["next_meal_type"], "lunch")
        self.assertGreater(len(recommendation["suggestions"]), 0)

        response = self.client.delete(f"/meals/{meal_id}?user_id={user_id}")
        self.assertEqual(response.status_code, 204, response.text)

        response = self.client.get(f"/meals/today?user_id={user_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), [])

    def test_stubs_and_validation(self):
        self.assertEqual(
            self.client.post("/foods/search", json={"query": "egg"}).status_code, 200
        )

        image_response = self.client.post(
            "/analyze-food-image",
            files={"image": ("meal.jpg", b"mock-image", "image/jpeg")},
        )
        self.assertEqual(image_response.status_code, 200, image_response.text)
        self.assertGreater(image_response.json()["total_calories"], 0)

        invalid_goal = self.client.post(
            "/user/", json={"name": "Invalid", "daily_calorie_goal": 0}
        )
        self.assertEqual(invalid_goal.status_code, 422)

        user_id = self.create_user()
        invalid_meal = self.client.post(
            f"/meals/?user_id={user_id}",
            json={"meal_type": "breakfast", "foods": []},
        )
        self.assertEqual(invalid_meal.status_code, 422)


if __name__ == "__main__":
    unittest.main()
