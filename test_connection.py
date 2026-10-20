from app.database import get_connection

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
               """)
        result = cursor.fetchall()
        print(result)