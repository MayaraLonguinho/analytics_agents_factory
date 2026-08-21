import os

def get_env() -> str:
    return os.getenv("APP_ENV", "development")
