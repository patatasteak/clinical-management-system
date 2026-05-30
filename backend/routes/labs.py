from typing import Optional, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()


class LabCreate(BaseModel):
    case_id: int
    catalog_id: Optional[str] = None
    catalog_ids: Optional[List[str]] = None
    date_released: Optional[str] = None
    date_taken: Optional[str] = None      # UI compat alias for date_released
    findings: Optional[str] = None


class LabUpdate(BaseModel):
    date_released: Optional[str] = None
    date_taken: Optional[str] = None      # UI compat alias for date_released
    findings: Optional[str] = None
    catalog_id: Optional[str] = None
    catalog_ids: Optional[List[str]] = None


def _normalize_catalog_ids(payload) -> List[str]:
    if getattr(payload, "catalog_ids", None):
        return [c for c in payload.catalog_ids if c is not None]
    if getattr(payload, "catalog_id", None):
        return [payload.catalog_id]
    return []


# Reusable SELECT for all lab queries
LAB_SELECT = """
    SELECT
        lr.result_id,
        lr.case_id,
        lr.date_released,
        lr.findings,
        lh.catalog_id,
        ltc.test_name,
        ltc.description  AS catalog_description,
        ltc.price
    FROM lab_result lr
    JOIN labhas lh      ON lh.result_id  = lr.result_id
    JOIN LabTestCatalog ltc ON ltc.catalog_id = lh.catalog_id
"""


@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict])
def list_lab_tests():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(LAB_SELECT + "ORDER BY lr.date_released DESC NULLS LAST, lr.result_id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@router.get("/cases/{case_id}", response_model=List[dict])
def get_labs_by_case(case_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        LAB_SELECT + "WHERE lr.case_id = %s ORDER BY lr.date_released DESC NULLS LAST, lr.result_id DESC",
        (case_id,),
    )
    labs = cur.fetchall()
    cur.close()
    conn.close()
    return labs


@router.get("/{lab_id}", response_model=List[dict])
def get_lab(lab_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(LAB_SELECT + "WHERE lr.result_id = %s", (lab_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Lab result not found")
    return rows


@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[dict])
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[dict])
def create_lab(payload: LabCreate):
    catalog_ids = _normalize_catalog_ids(payload)
    if not catalog_ids:
        raise HTTPException(status_code=400, detail="catalog_id or catalog_ids is required")

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Verify case exists
    cur.execute("SELECT case_id FROM patient_case WHERE case_id = %s", (payload.case_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Case not found")

    date_released = payload.date_released or payload.date_taken
    findings = payload.findings if payload.findings is not None else ""

    cur.execute(
        """
        INSERT INTO lab_result (case_id, date_released, findings)
        VALUES (%s, %s, %s)
        RETURNING result_id
        """,
        (payload.case_id, date_released, findings),
    )
    result_id = cur.fetchone()["result_id"]

    for cid in catalog_ids:
        cur.execute(
            "INSERT INTO labhas (result_id, catalog_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (result_id, cid),
        )

    cur.execute(LAB_SELECT + "WHERE lr.result_id = %s", (result_id,))
    new_rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return new_rows


@router.put("/{lab_id}", response_model=List[dict])
def update_lab(lab_id: int, payload: LabUpdate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Verify lab result exists
    cur.execute("SELECT result_id FROM lab_result WHERE result_id = %s", (lab_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Lab result not found")

    payload_dict = payload.dict(exclude_unset=True)

    # Normalize date_taken alias
    if "date_taken" in payload_dict and "date_released" not in payload_dict:
        payload_dict["date_released"] = payload_dict["date_taken"]

    # Update scalar fields if provided
    fields = []
    values = []
    if "date_released" in payload_dict:
        fields.append("date_released = %s")
        values.append(payload_dict["date_released"])
    if "findings" in payload_dict:
        fields.append("findings = %s")
        values.append(payload_dict["findings"])

    if fields:
        values.append(lab_id)
        cur.execute(
            f"UPDATE lab_result SET {', '.join(fields)} WHERE result_id = %s",
            tuple(values),
        )

    # Update catalog links if provided
    catalog_ids = _normalize_catalog_ids(payload)
    if catalog_ids:
        cur.execute("DELETE FROM labhas WHERE result_id = %s", (lab_id,))
        for cid in catalog_ids:
            cur.execute(
                "INSERT INTO labhas (result_id, catalog_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (lab_id, cid),
            )

    cur.execute(LAB_SELECT + "WHERE lr.result_id = %s", (lab_id,))
    updated = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return updated


@router.delete("/{lab_id}")
def delete_lab(lab_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "DELETE FROM lab_result WHERE result_id = %s RETURNING result_id",
        (lab_id,),
    )
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Lab result not found")
    return {"message": "Lab result deleted", "result_id": lab_id}