"""
Application Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = "ModelMatch API"

    APP_VERSION = "1.0.0"

    DATABASE_URL = os.getenv("DATABASE_URL")

    SUPABASE_URL = os.getenv("SUPABASE_URL")

    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    MAX_UPLOAD_SIZE = 20 * 1024 * 1024

    ALLOWED_EXTENSIONS = ["csv"]

    UPLOAD_FOLDER = "backend/uploads"

    OPTUNA_TRIALS = 20


settings = Settings()