import os
import unittest
from sqlalchemy import text
from starlette.testclient import TestClient

from backend.main import app
from backend.config.config import get_settings
from backend.database.connection import engine, SessionLocal, get_db, Base
from backend.database import crud, schemas, models
from backend.services.database_service import get_prediction_history

settings = get_settings()
client = TestClient(app, raise_server_exceptions=False)


class DatabaseReliabilityTests(unittest.TestCase):

    def test_01_database_connectivity(self):
        """Verify that the database engine can connect and execute a basic query."""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            self.assertEqual(result, 1)

    def test_02_tables_created(self):
        """Verify that predictions, users, and diseases tables exist."""
        with engine.connect() as conn:
            if settings.DATABASE_URL.startswith("sqlite"):
                rows = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
                table_names = [r[0] for r in rows]
                self.assertIn("predictions", table_names)
                self.assertIn("users", table_names)
                self.assertIn("diseases", table_names)

    def test_03_create_and_retrieve_prediction(self):
        """Verify prediction record creation and retrieval via CRUD."""
        db = SessionLocal()
        try:
            record_in = schemas.PredictionCreate(
                filename="unit_test_leaf.jpg",
                image_path="backend/uploads/original/unit_test_leaf.jpg",
                crop_name="Tomato",
                disease_name="Early blight",
                confidence=92.5,
                severity=None,
                processing_time=0.45
            )
            saved = crud.create_prediction(db, record_in)
            self.assertIsNotNone(saved.id)
            self.assertEqual(saved.crop_name, "Tomato")
            self.assertEqual(saved.disease_name, "Early blight")
            self.assertEqual(saved.confidence, 92.5)

            history = crud.get_history(db, limit=10)
            self.assertGreater(len(history), 0)
            found = any(h.filename == "unit_test_leaf.jpg" for h in history)
            self.assertTrue(found)
        finally:
            db.close()

    def test_04_transaction_rollback_on_failure(self):
        """Verify that invalid operations trigger rollback without session corruption."""
        db = SessionLocal()
        try:
            bad_pred = models.Prediction(
                filename=None,
                crop_name=None,
                disease_name=None,
                confidence=None
            )
            try:
                db.add(bad_pred)
                db.commit()
            except Exception:
                db.rollback()

            # Session should still be completely usable after rollback
            res = db.execute(text("SELECT 1")).scalar()
            self.assertEqual(res, 1)
        finally:
            db.close()

    def test_05_health_check_endpoint(self):
        """Verify /health and /api/v1/health report healthy and database connected."""
        res = client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
        self.assertEqual(data["model"], "loaded")

        v1_res = client.get("/api/v1/health")
        self.assertEqual(v1_res.status_code, 200)
        v1_data = v1_res.json()
        self.assertEqual(v1_data["status"], "healthy")
        self.assertEqual(v1_data["database"], "connected")

    def test_06_health_check_degraded_when_db_down(self):
        """Verify /health reports disconnected and degraded when database fails."""
        def broken_db():
            class MockBrokenSession:
                def execute(self, *args, **kwargs):
                    raise ConnectionError("Simulated DB connection failure")
                def close(self):
                    pass
            yield MockBrokenSession()

        app.dependency_overrides[get_db] = broken_db
        try:
            res = client.get("/health")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["database"], "disconnected")
            self.assertEqual(data["status"], "degraded")
        finally:
            app.dependency_overrides.clear()

    def test_07_predict_persistence_end_to_end(self):
        """Verify POST /predict saves to database and returns saved_to_history=True."""
        img_path = "backend/uploads/test/2.jpg"
        with open(img_path, "rb") as f:
            img_bytes = f.read()

        res = client.post("/predict", files={"file": ("2.jpg", img_bytes, "image/jpeg")})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["confidence"], 60.0)
        self.assertTrue(data.get("saved_to_history"))

        # Verify record in GET /history
        hist_res = client.get("/history")
        self.assertEqual(hist_res.status_code, 200)
        hist_items = hist_res.json()
        self.assertGreater(len(hist_items), 0)
        self.assertTrue(any(h["filename"] == "2.jpg" for h in hist_items))

    def test_08_predict_graceful_when_db_fails_no_credential_leakage(self):
        """Verify prediction succeeds even if DB fails, without leaking credentials or stack traces."""
        def broken_db():
            class MockBrokenSession:
                def execute(self, *args, **kwargs):
                    raise ConnectionError("Simulated database failure: postgresql://fake_user:fake_password@localhost:5432/cropsense")
                def add(self, *args, **kwargs):
                    raise ConnectionError("Simulated write failure")
                def commit(self):
                    raise ConnectionError("Simulated commit failure")
                def rollback(self):
                    pass
                def close(self):
                    pass
            yield MockBrokenSession()

        app.dependency_overrides[get_db] = broken_db
        try:
            img_path = "backend/uploads/test/2.jpg"
            with open(img_path, "rb") as f:
                img_bytes = f.read()

            res = client.post("/predict", files={"file": ("2.jpg", img_bytes, "image/jpeg")})
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertNotEqual(data["plant"], "")
            self.assertFalse(data.get("saved_to_history"))

            raw_text = res.text
            self.assertNotIn("fake_password", raw_text)
            self.assertNotIn("Traceback", raw_text)
        finally:
            app.dependency_overrides.clear()

    def test_09_history_endpoints_work(self):
        """Verify GET /history and GET /api/v1/history return valid JSON lists."""
        res = client.get("/history")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

        v1_res = client.get("/api/v1/history")
        self.assertEqual(v1_res.status_code, 200)
        self.assertIsInstance(v1_res.json(), list)

    def test_10_legacy_cropsense_db_file_intact(self):
        """Verify legacy cropsense.db file has not been deleted or overwritten."""
        import sqlite3
        self.assertTrue(os.path.exists("cropsense.db"), "cropsense.db must not be deleted")
        conn = sqlite3.connect("cropsense.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM predictions;")
        count = c.fetchone()[0]
        conn.close()
        self.assertEqual(count, 17, f"cropsense.db row count must remain 17, got {count}")


if __name__ == "__main__":
    unittest.main()
