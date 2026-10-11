# Compatibility wrapper for older db.py imports
from backend.database.connection import engine, SessionLocal, Base
from backend.database.models import Prediction

# Keep existing references working
DATABASE_URL = str(engine.url)
