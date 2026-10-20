from pathlib import Path

from app.database import get_connection

schema_path = Path(__file__).with_name("schema.sql")
schema = schema_path.read_bytes()

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(schema)

print("Database tables created successfully.")