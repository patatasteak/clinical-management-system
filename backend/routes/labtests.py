from fastapi import APIRouter, HTTPException
from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()

@router.get("/cases/{case_id}/labs")
def get_labs_by_case(case_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT lt.*,
               ltc.test_name,
               ltc.description,
               ltc.price,
               d.first_name || ' ' || d.last_name AS ordered_by_name
        FROM lab_test lt
        JOIN labtestcatalog ltc ON lt.catalog_id = ltc.catalog_id
        LEFT JOIN doctor d ON lt.ordered_by = d.doctor_id
        WHERE lt.case_id = %s
        ORDER BY lt.date_taken DESC
    """, (case_id,))
    labs = cur.fetchall()
    cur.close()
    conn.close()
    return labs

@router.post("/")
def create_lab_test(payload: dict):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO lab_test (case_id, catalog_id, date_taken, findings, ordered_by)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
    """, (
        payload.get("case_id"),
        payload.get("catalog_id"),
        payload.get("date_taken"),
        payload.get("findings"),
        payload.get("ordered_by")
    ))
    lab = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return lab

@router.put("/{test_id}")
def update_lab_test(test_id: int, payload: dict):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        UPDATE lab_test
        SET findings = %s,
            date_taken = %s,
            catalog_id = %s,
            ordered_by = %s
        WHERE test_id = %s
        RETURNING *
    """, (
        payload.get("findings"),
        payload.get("date_taken"),
        payload.get("catalog_id"),
        payload.get("ordered_by"),
        test_id
    ))
    lab = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return lab

@router.delete("/{test_id}")
def delete_lab_test(test_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM lab_test WHERE test_id = %s RETURNING *", (test_id,))
    lab = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return {"message": "Lab test deleted", "test_id": test_id}