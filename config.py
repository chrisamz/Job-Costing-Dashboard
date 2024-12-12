import os

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "job_costing")
}

# SQLite fallback (if using a local SQLite database)
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/job_costing.db")

# Debugging and development settings
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# Application settings
APP_SETTINGS = {
    "secret_key": os.getenv("SECRET_KEY", "your_secret_key"),
    "host": os.getenv("APP_HOST", "127.0.0.1"),
    "port": int(os.getenv("APP_PORT", 8050))
}

# Logging configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": os.getenv("LOG_FILE", "app.log")
}

# Example usage for connecting to the database
if __name__ == "__main__":
    print("Database Configuration:")
    print(DB_CONFIG)
    print("SQLite Path:", SQLITE_DB_PATH)
    print("Debug Mode:", DEBUG)
