from typing import Optional, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()


class LabCreate(BaseModel):
    case_id: int
    catalog_id: str
    date_taken: Optional[str] = None
    findings: Optional[str] = None
    ordered_by: Optional[int] = None


class LabUpdate(BaseModel):
    date_taken: Optional[str] = None
    findings: Optional[str] = None
    catalog_id: Optional[str] = None
    ordered_by: Optional[int] = None


@router.get("/", response_model=List[dict])
def list_lab_tests():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT lt.*, ltc.test_name, ltc.description AS catalog_description, ltc.price,
               d.first_name || ' ' || d.last_name AS ordered_by_name
        FROM lab_test lt
        LEFT JOIN LabTestCatalog ltc ON lt.catalog_id = ltc.catalog_id
        LEFT JOIN doctor d ON lt.ordered_by = d.doctor_id
        ORDER BY lt.date_taken DESC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@router.get("/cases/{case_id}")
def get_labs_by_case(case_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT lt.*,
               ltc.test_name,
               ltc.description AS catalog_description,
               ltc.price,
               d.first_name || ' ' || d.last_name AS ordered_by_name
        FROM lab_test lt
        JOIN LabTestCatalog ltc ON lt.catalog_id = ltc.catalog_id
        LEFT JOIN doctor d ON lt.ordered_by = d.doctor_id
        WHERE lt.case_id = %s
        ORDER BY lt.date_taken DESC
    """, (case_id,))
    labs = cur.fetchall()
    cur.close()
    conn.close()
    return labs


@router.get("/{lab_id}")
def get_lab(lab_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT lt.*, ltc.test_name, ltc.description AS catalog_description, ltc.price,
               d.first_name || ' ' || d.last_name AS ordered_by_name
        FROM lab_test lt
        LEFT JOIN LabTestCatalog ltc ON lt.catalog_id = ltc.catalog_id
        LEFT JOIN doctor d ON lt.ordered_by = d.doctor_id
        WHERE lt.test_id = %s
        """,
        (lab_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return row


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_lab(payload: LabCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO lab_test (case_id, catalog_id, date_taken, findings, ordered_by) VALUES (%s,%s,%s,%s,%s) RETURNING test_id, case_id, catalog_id, date_taken, findings, ordered_by",
        (
            payload.case_id,
            payload.catalog_id,
            payload.date_taken,
            payload.findings,
            payload.ordered_by,
        ),
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_row


@router.put("/{lab_id}")
def update_lab(lab_id: int, payload: LabUpdate):
    fields = []
    values = []
    for k, v in payload.dict(exclude_unset=True).items():
        fields.append(f"{k} = %s")
        values.append(v)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(lab_id)
    sql = f"UPDATE lab_test SET {', '.join(fields)} WHERE test_id = %s RETURNING test_id, case_id, catalog_id, date_taken, findings, ordered_by"

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, tuple(values))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        raise HTTPException(status_code=404, detail="Lab test not found")

    return updated


@router.delete("/{lab_id}")
def delete_lab(lab_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM lab_test WHERE test_id = %s RETURNING test_id", (lab_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return {"message": "Lab test deleted", "test_id": lab_id}
