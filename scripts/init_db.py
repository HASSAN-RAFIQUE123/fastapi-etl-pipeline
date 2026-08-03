"""Initialize the project's database tables."""

from app.db import init_db


if __name__ == "__main__":
    init_db()
    print("Database initialized")
