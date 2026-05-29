from typing import Optional, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()


class MedicineCreate(BaseModel):
    name: str
    description: Optional[str] = None
    form: Optional[str] = None
    strength: Optional[str] = None
    unit_price: Optional[float] = None


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    form: Optional[str] = None
    strength: Optional[str] = None
    unit_price: Optional[float] = None


class PrescriptionCreate(BaseModel):
    case_id: int
    prescribed_by: int
    instructions: Optional[str] = None
    notes: Optional[str] = None


class PrescriptionUpdate(BaseModel):
    case_id: Optional[int] = None
    prescribed_by: Optional[int] = None
    instructions: Optional[str] = None
    notes: Optional[str] = None


class PrescriptionMedicineCreate(BaseModel):
    medicine_id: int
    quantity: Optional[int] = 1
    dosage: Optional[str] = None
    frequency: Optional[str] = None


class PrescriptionMedicineUpdate(BaseModel):
    quantity: Optional[int] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None


@router.get("/", response_model=List[dict])
def list_prescriptions():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT
            p.*, 
            json_agg(json_build_object(
                'medicine_id', m.medicine_id,
                'name', m.name,
                'description', m.description,
                'form', m.form,
                'strength', m.strength,
                'unit_price', m.unit_price,
                'quantity', h.quantity,
                'dosage', h.dosage,
                'frequency', h.frequency
            )) FILTER (WHERE m.medicine_id IS NOT NULL) AS medicines
        FROM prescription p
        LEFT JOIN "has" h ON h.prescription_id = p.prescription_id
        LEFT JOIN medicine m ON m.medicine_id = h.medicine_id
        GROUP BY p.prescription_id
        ORDER BY p.prescribed_at DESC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@router.get("/{prescription_id}")
def get_prescription(prescription_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT
            p.*, 
            json_agg(json_build_object(
                'medicine_id', m.medicine_id,
                'name', m.name,
                'description', m.description,
                'form', m.form,
                'strength', m.strength,
                'unit_price', m.unit_price,
                'quantity', h.quantity,
                'dosage', h.dosage,
                'frequency', h.frequency
            )) FILTER (WHERE m.medicine_id IS NOT NULL) AS medicines
        FROM prescription p
        LEFT JOIN "has" h ON h.prescription_id = p.prescription_id
        LEFT JOIN medicine m ON m.medicine_id = h.medicine_id
        WHERE p.prescription_id = %s
        GROUP BY p.prescription_id
        """,
        (prescription_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return row


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_prescription(payload: PrescriptionCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO prescription (case_id, prescribed_by, instructions, notes) VALUES (%s,%s,%s,%s) RETURNING *",
        (payload.case_id, payload.prescribed_by, payload.instructions, payload.notes),
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_row


@router.put("/{prescription_id}")
def update_prescription(prescription_id: int, payload: PrescriptionUpdate):
    fields = []
    values = []
    for key, value in payload.dict(exclude_unset=True).items():
        fields.append(f"{key} = %s")
        values.append(value)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    values.append(prescription_id)
    sql = f"UPDATE prescription SET {', '.join(fields)} WHERE prescription_id = %s RETURNING *"
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, tuple(values))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return updated


@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM prescription WHERE prescription_id = %s RETURNING prescription_id", (prescription_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return {"message": "Prescription deleted", "prescription_id": prescription_id}


@router.get("/medicines", response_model=List[dict])
def list_medicines():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM medicine ORDER BY name")
    medicines = cur.fetchall()
    cur.close()
    conn.close()
    return medicines


@router.get("/medicines/{medicine_id}")
def get_medicine(medicine_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM medicine WHERE medicine_id = %s", (medicine_id,))
    medicine = cur.fetchone()
    cur.close()
    conn.close()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.post("/medicines", status_code=status.HTTP_201_CREATED)
def create_medicine(payload: MedicineCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO medicine (name, description, form, strength, unit_price) VALUES (%s,%s,%s,%s,%s) RETURNING *",
        (payload.name, payload.description, payload.form, payload.strength, payload.unit_price),
    )
    new_med = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_med


@router.put("/medicines/{medicine_id}")
def update_medicine(medicine_id: int, payload: MedicineUpdate):
    fields = []
    values = []
    for key, value in payload.dict(exclude_unset=True).items():
        fields.append(f"{key} = %s")
        values.append(value)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    values.append(medicine_id)
    sql = f"UPDATE medicine SET {', '.join(fields)} WHERE medicine_id = %s RETURNING *"
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, tuple(values))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return updated


@router.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM medicine WHERE medicine_id = %s RETURNING medicine_id", (medicine_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {"message": "Medicine deleted", "medicine_id": medicine_id}


@router.post("/{prescription_id}/medicines", status_code=status.HTTP_201_CREATED)
def add_medicine_to_prescription(prescription_id: int, payload: PrescriptionMedicineCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO \"has\" (prescription_id, medicine_id, quantity, dosage, frequency) VALUES (%s,%s,%s,%s,%s) RETURNING *",
        (prescription_id, payload.medicine_id, payload.quantity, payload.dosage, payload.frequency),
    )
    inserted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return inserted


@router.put("/{prescription_id}/medicines/{medicine_id}")
def update_prescription_medicine(prescription_id: int, medicine_id: int, payload: PrescriptionMedicineUpdate):
    fields = []
    values = []
    for key, value in payload.dict(exclude_unset=True).items():
        fields.append(f"{key} = %s")
        values.append(value)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    values.extend([prescription_id, medicine_id])
    sql = f"UPDATE \"has\" SET {', '.join(fields)} WHERE prescription_id = %s AND medicine_id = %s RETURNING *"
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, tuple(values))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Prescription medicine entry not found")
    return updated


@router.delete("/{prescription_id}/medicines/{medicine_id}")
def delete_prescription_medicine(prescription_id: int, medicine_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM \"has\" WHERE prescription_id = %s AND medicine_id = %s RETURNING *", (prescription_id, medicine_id))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Prescription medicine entry not found")
    return {"message": "Prescription medicine entry deleted", "prescription_id": prescription_id, "medicine_id": medicine_id}
