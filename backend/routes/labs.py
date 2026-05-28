from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()


class LabCreate(BaseModel):
    case_id: int
    catalog_id: str
    date_taken: Optional[str]
    findings: Optional[str]
    ordered_by: Optional[int]


class LabUpdate(BaseModel):
    date_taken: Optional[str]
    findings: Optional[str]
    ordered_by: Optional[int]


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
