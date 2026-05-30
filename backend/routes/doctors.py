from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database import get_connection
from psycopg2.extras import RealDictCursor
import hashlib

router = APIRouter()


class DoctorLogin(BaseModel):
    doctor_id: int
    password: str


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    sex: Optional[str] = None
    license_no: Optional[int] = None
    email: Optional[str] = None
    years_exp: Optional[int] = None
    specialization: Optional[str] = None
    contact_number: Optional[str] = None
    role: Optional[str] = "resident"
    password: Optional[str] = None


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    sex: Optional[str] = None
    license_no: Optional[int] = None
    email: Optional[str] = None
    years_exp: Optional[int] = None
    specialization: Optional[str] = None
    contact_number: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True


def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


@router.post("/login")
def doctor_login(payload: DoctorLogin):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT * FROM doctor WHERE doctor_id = %s",
        (payload.doctor_id,)
    )
    doctor = cur.fetchone()
    cur.close()
    conn.close()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if doctor.get("password_hash"):
        if _hash_password(payload.password) != doctor["password_hash"]:
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        # If no password set, allow login with any password (for demo)
        pass

    return doctor


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
                       'date_opened', pc.date_opened,
                       'description', pc.description,
                       'feedback', pc.feedback,
                       'patient', json_build_object(
                           'patientid', p.patientid,
                           'firstname', p.firstname,
                           'lastname', p.lastname
                       )
                   )
               ) FILTER (WHERE pc.case_id IS NOT NULL) AS cases
        FROM doctor d
        LEFT JOIN patient_case pc ON d.doctor_id = pc.doctor_id
        LEFT JOIN patient p ON pc.patientid = p.patientid
        WHERE d.doctor_id = %s
        GROUP BY d.doctor_id
    """, (doctor_id,))
    doctor = cur.fetchone()
    cur.close()
    conn.close()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    password_hash = None
    if payload.password:
        password_hash = _hash_password(payload.password)

    cur.execute("""
        INSERT INTO doctor (first_name, last_name, sex, license_no, email, years_exp, specialization, contact_number, role, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    """, (
        payload.first_name,
        payload.last_name,
        payload.sex,
        payload.license_no,
        payload.email,
        payload.years_exp,
        payload.specialization,
        payload.contact_number,
        payload.role,
        password_hash
    ))
    doctor = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return doctor


@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, payload: DoctorUpdate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Field name mapping for dynamic update
    field_mapping = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'sex': 'sex',
        'license_no': 'license_no',
        'email': 'email',
        'years_exp': 'years_exp',
        'specialization': 'specialization',
        'contact_number': 'contact_number',
        'role': 'role',
        'is_active': 'is_active'
    }
    
    fields = []
    values = []
    
    payload_dict = payload.dict(exclude_unset=True)
    
    for key, value in payload_dict.items():
        db_field = field_mapping.get(key)
        if db_field:
            fields.append(f"{db_field} = %s")
            values.append(value)
    
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(doctor_id)
    
    sql = f"UPDATE doctor SET {', '.join(fields)} WHERE doctor_id = %s RETURNING *"
    
    cur.execute(sql, tuple(values))
    doctor = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    # First check if doctor exists
    cur.execute("SELECT doctor_id FROM doctor WHERE doctor_id = %s", (doctor_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Delete doctor
    cur.execute("DELETE FROM doctor WHERE doctor_id = %s", (doctor_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    return None