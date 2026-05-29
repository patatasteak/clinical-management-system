from database import get_connection
from psycopg2.extras import RealDictCursor

conn = get_connection()
cur = conn.cursor(cursor_factory=RealDictCursor)

print("=== Medicine Table Structure ===")
cur.execute("""
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_name = 'medicine'
    ORDER BY ordinal_position
""")
for col in cur.fetchall():
    print(f"- {col['column_name']}: {col['data_type']} (nullable: {col['is_nullable']}, default: {col['column_default']})")

print("\n=== Current Medicine Data ===")
cur.execute("SELECT * FROM medicine")
for med in cur.fetchall():
    print(dict(med))

cur.close()
conn.close()
