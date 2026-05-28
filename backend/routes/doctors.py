from fastapi import APIRouter, HTTPException
from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()

@router.get("/")
def get_doctors():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM doctor ORDER BY last_name")
    doctors = cur.fetchall()
    cur.close()
    conn.close()
    return doctors

@router.get("/{doctor_id}")
def get_doctor(doctor_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT d.*,
               json_agg(
                   json_build_object(
                       'case_id', pc.case_id,
                       'chief_complaint', pc.chief_complaint,
                       'appoint_status', pc.appoint_status,
                       'date_opened', pc.date_opened
                   )
               ) FILTER (WHERE pc.case_id IS NOT NULL) AS cases
        FROM doctor d
        LEFT JOIN patient_case pc ON d.doctor_id = pc.doctor_id
        WHERE d.doctor_id = %s
        GROUP BY d.doctor_id
    """, (doctor_id,))
    doctor = cur.fetchone()
    cur.close()
    conn.close()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/")
def create_doctor(payload: dict):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO doctor (first_name, last_name, sex, license_no, email, years_exp, specialization, contact_number, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    """, (
        payload.get("first_name"),
        payload.get("last_name"),
        payload.get("sex"),
        payload.get("license_no"),
        payload.get("email"),
        payload.get("years_exp"),
        payload.get("specialization"),
        payload.get("contact_number"),
        payload.get("role", "resident")
    ))
    doctor = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return doctor

@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, payload: dict):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        UPDATE doctor
        SET first_name = %s, last_name = %s, specialization = %s,
            role = %s, contact_number = %s, email = %s, is_active = %s
        WHERE doctor_id = %s
        RETURNING *
    """, (
        payload.get("first_name"),
        payload.get("last_name"),
        payload.get("specialization"),
        payload.get("role"),
        payload.get("contact_number"),
        payload.get("email"),
        payload.get("is_active", True),
        doctor_id
    ))
    doctor = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor