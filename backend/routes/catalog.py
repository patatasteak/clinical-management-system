from fastapi import APIRouter, HTTPException
from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()

@router.get("/")
def get_catalog():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM labtestcatalog ORDER BY test_name")
    catalog = cur.fetchall()
    cur.close()
    conn.close()
    return catalog

@router.get("/{catalog_id}")
def get_catalog_item(catalog_id: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM labtestcatalog WHERE catalog_id = %s", (catalog_id,))
    item = cur.fetchone()
    cur.close()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Test not found")
    return item

@router.post("/")
def create_catalog_item(payload: dict):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO labtestcatalog (catalog_id, test_name, description, price)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (
        payload.get("catalog_id"),
        payload.get("test_name"),
        payload.get("description"),
        payload.get("price")
    ))
    item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return item