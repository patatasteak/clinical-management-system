from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi import status
from pydantic import BaseModel

from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()


# --- Pydantic schemas (minimal) ---
class PatientCreate(BaseModel):
    FirstName: str
    LastName: str
    Nationality: Optional[str] = None
    Sex: Optional[str] = None
    Address: Optional[str] = None
    contactNumber: Optional[str] = None
    BloodType: Optional[str] = None
    email: str
    birthday: Optional[str] = None
    emergencyContact: Optional[str] = None
    password: Optional[str] = None  # will be stored as password_hash (simple sha256)


class PatientUpdate(BaseModel):
    FirstName: Optional[str]
    LastName: Optional[str]
    Nationality: Optional[str]
    Sex: Optional[str]
    Address: Optional[str]
    contactNumber: Optional[str]
    BloodType: Optional[str]
    email: Optional[str]
    birthday: Optional[str]
    emergencyContact: Optional[str]


import hashlib


def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


@router.get("/", response_model=List[dict])
def get_patients():
    """Return a list of patients (basic fields)."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT patientid, firstname, lastname, email, birthday
        FROM patient
        ORDER BY lastname, firstname
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@router.get("/{patient_id}")
def get_patient(patient_id: int):
    """Fat GET: return patient profile with nested related data in one response.

    Uses subqueries that aggregate related rows as JSON arrays.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
SELECT
  p.patientid,
  p.firstname,
  p.lastname,
  p.nationality,
  p.sex,
  p.address,
  p.contactnumber,
  p.bloodtype,
  p.email,
  p.birthday,
  p.emergencycontact,

  COALESCE(v.vitals, '[]') AS vitals,
  COALESCE(pr.prescriptions, '[]') AS prescriptions

FROM patient p

LEFT JOIN (
  SELECT
    patientid,
    json_agg(json_build_object(
      'stat_id', stat_id,
      'recorded_at', recorded_at,
      'weight', weight,
      'height', height,
      'temperature', temperature,
      'blood_pressure', blood_pressure,
      'pulse_rate', pulse_rate
    ) ORDER BY recorded_at DESC) AS vitals
  FROM vital_stats
  GROUP BY patientid
) v ON v.patientid = p.patientid

LEFT JOIN (
  SELECT
    pc.patientid,
    json_agg(json_build_object(
      'prescription_id', pr.prescription_id,
      'case_id', pr.case_id,
      'prescribed_at', pr.prescribed_at,
      'instructions', pr.instructions,
      'prescribed_by', pr.prescribed_by,
      'notes', pr.notes,
      'medicines', COALESCE(pm.medicines, '[]')
    ) ORDER BY pr.prescribed_at DESC) AS prescriptions

  FROM prescription pr

  JOIN patient_case pc
    ON pc.case_id = pr.case_id

  LEFT JOIN (
    SELECT
      h.prescription_id,
      json_agg(json_build_object(
        'medicine_id', m.med_id,
        'name', m.medicinename,
        'medicine_type', m.medicine_type,
        'quantity', h.quantity,
        'dosage', h.dosage,
        'frequency', h.frequency
      )) AS medicines

    FROM "has" h
    JOIN medicine m
      ON m.med_id = h.med_id

    GROUP BY h.prescription_id
  ) pm ON pm.prescription_id = pr.prescription_id

  GROUP BY pc.patientid
) pr ON pr.patientid = p.patientid

WHERE p.patientid = %s;
    """
    cur.execute(sql, (patient_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")

    # psycopg2 returns json_agg as Python list/dict when using RealDictCursor
    return row


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    password_hash = None
    if payload.password:
        password_hash = _hash_password(payload.password)

    cur.execute(
        """
        INSERT INTO patient (firstname, lastname, nationality, sex, address, contactnumber, bloodtype, email, birthday, emergencycontact, password_hash)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING patientid, firstname, lastname, email, birthday
        """,
        (
            payload.FirstName,
            payload.LastName,
            payload.Nationality,
            payload.Sex,
            payload.Address,
            payload.contactNumber,
            payload.BloodType,
            payload.email,
            payload.birthday,
            payload.emergencyContact,
            password_hash,
        ),
    )

    new_patient = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_patient


@router.put("/{patient_id}")
def update_patient(patient_id: int, payload: PatientUpdate):
    # Build dynamic set clause
    fields = []
    values = []
    for k, v in payload.dict(exclude_unset=True).items():
        fields.append(f"{k.lower()} = %s")
        values.append(v)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(patient_id)
    sql = f"UPDATE patient SET {', '.join(fields)} WHERE patientid = %s RETURNING patientid, firstname, lastname, email, birthday"

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, tuple(values))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")

    return updated


@router.get("/{patient_id}/vitals")
def get_patient_vitals(patient_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT stat_id, recorded_at, weight, height, temperature, blood_pressure, pulse_rate FROM vital_stats WHERE patientid = %s ORDER BY recorded_at DESC",
        (patient_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@router.get("/{patient_id}/cases")
def get_patient_cases(patient_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
    SELECT
        pc.case_id,
        pc.appoint_status,
        pc.chief_complaint,
        pc.description,
        pc.feedback,
        pc.patientid,
        pc.doctor_id,
        pc.date_opened,
        pc.date_closed,

        json_build_object(
            'doctor_id', d.doctor_id,
            'first_name', d.first_name,
            'last_name', d.last_name
        ) AS doctor,

        COALESCE(lab.tests, '[]') AS lab_tests

    FROM patient_case pc

    LEFT JOIN doctor d
        ON d.doctor_id = pc.doctor_id

    LEFT JOIN (
        SELECT
            lt.case_id,

            json_agg(json_build_object(
                'test_id', lt.test_id,
                'catalog_id', lt.catalog_id,
                'test_name', ltc.test_name,
                'date_taken', lt.date_taken,
                'findings', lt.findings,
                'ordered_by', lt.ordered_by
            )) AS tests

        FROM lab_test lt

        LEFT JOIN labtestcatalog ltc
            ON ltc.catalog_id = lt.catalog_id

        GROUP BY lt.case_id

    ) lab ON lab.case_id = pc.case_id

    WHERE pc.patientid = %s

    ORDER BY pc.date_opened DESC
    """

    cur.execute(sql, (patient_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    # First check if patient exists
    cur.execute("SELECT patientid FROM patient WHERE patientid = %s", (patient_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Delete patient
    cur.execute("DELETE FROM patient WHERE patientid = %s", (patient_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    return None