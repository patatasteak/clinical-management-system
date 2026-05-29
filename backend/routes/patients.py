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

  COALESCE(cb.clinical_background, '[]') AS clinical_background,
  COALESCE(a.allergies, '[]') AS allergies,
  COALESCE(d.disabilities, '[]') AS disabilities,
  COALESCE(ps.past_surgeries, '[]') AS past_surgeries,
  COALESCE(v.vitals, '[]') AS vitals,
  COALESCE(pr.prescriptions, '[]') AS prescriptions

FROM patient p

LEFT JOIN (
  SELECT
    pc.patientid,
    json_agg(json_build_object(
      'clinical_id', cb.clinical_id,
      'case_id', cb.case_id,
      'smoking_status', cb.smoking_status,
      'alcohol_use', cb.alcohol_use,
      'notes', cb.notes
    )) AS clinical_background
  FROM clinical_background cb
  JOIN patient_case pc
    ON pc.case_id = cb.case_id
  GROUP BY pc.patientid
) cb ON cb.patientid = p.patientid

LEFT JOIN (
  SELECT
    pc.patientid,
    json_agg(json_build_object(
      'allergy_id', a.allergy_id,
      'allergen', a.allergen,
      'reaction', a.reaction,
      'severity', a.severity,
      'noted_date', a.noted_date
    )) AS allergies
  FROM allergy a
  JOIN clinical_background cb
    ON cb.clinical_id = a.clinical_id
  JOIN patient_case pc
    ON pc.case_id = cb.case_id
  GROUP BY pc.patientid
) a ON a.patientid = p.patientid

LEFT JOIN (
  SELECT
    pc.patientid,
    json_agg(json_build_object(
      'disability_id', d.disability_id,
      'description', d.description,
      'congenital', d.congenital,
      'notes', d.notes
    )) AS disabilities
  FROM disability d
  JOIN clinical_background cb
    ON cb.clinical_id = d.clinical_id
  JOIN patient_case pc
    ON pc.case_id = cb.case_id
  GROUP BY pc.patientid
) d ON d.patientid = p.patientid

LEFT JOIN (
  SELECT
    pc.patientid,
    json_agg(json_build_object(
      'surgery_id', ps.surgery_id,
      'procedure_name', ps.procedure_name,
      'date_performed', ps.date_performed,
      'hospital', ps.hospital,
      'notes', ps.notes
    )) AS past_surgeries
  FROM past_surgery ps
  JOIN clinical_background cb
    ON cb.clinical_id = ps.clinical_id
  JOIN patient_case pc
    ON pc.case_id = cb.case_id
  GROUP BY pc.patientid
) ps ON ps.patientid = p.patientid

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
        'medicine_id', m.medicine_id,
        'name', m.medicine_name,
        'medicine_type', m.medicine_type,
        'quantity', h.quantity,
        'dosage', h.dosage,
        'frequency', h.frequency
      )) AS medicines

    FROM "has" h
    JOIN medicine m
      ON m.medicine_id = h.medicine_id

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


def _get_or_create_clinical_id(patient_id: int, cur):
    cur.execute(
        "SELECT clinical_id FROM clinical_background WHERE patientid = %s",
        (patient_id,),
    )
    row = cur.fetchone()
    if row:
        return row["clinical_id"]
    cur.execute(
        "INSERT INTO clinical_background (patientid) VALUES (%s) RETURNING clinical_id",
        (patient_id,),
    )
    return cur.fetchone()["clinical_id"]


@router.post("/{patient_id}/allergies", status_code=status.HTTP_201_CREATED)
def add_allergy(patient_id: int, payload: dict):
    # payload expected keys: allergen, reaction, severity, noted_date
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    clinical_id = _get_or_create_clinical_id(patient_id, cur)
    cur.execute(
        "INSERT INTO allergy (clinical_id, allergen, reaction, severity, noted_date) VALUES (%s,%s,%s,%s,%s) RETURNING allergy_id, allergen, reaction, severity, noted_date",
        (
            clinical_id,
            payload.get("allergen"),
            payload.get("reaction"),
            payload.get("severity"),
            payload.get("noted_date"),
        ),
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_row


@router.delete("/allergies/{allergy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_allergy(allergy_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM allergy WHERE allergy_id = %s RETURNING allergy_id", (allergy_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return None


@router.post("/{patient_id}/conditions", status_code=status.HTTP_201_CREATED)
def add_condition(patient_id: int, payload: dict):
    # payload expected keys: condition_name, date_diagnosed, status, notes
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    clinical_id = _get_or_create_clinical_id(patient_id, cur)
    cur.execute(
        "INSERT INTO chronic_condition (clinical_id, condition_name, date_diagnosed, status, notes) VALUES (%s,%s,%s,%s,%s) RETURNING condition_id, condition_name, date_diagnosed, status, notes",
        (
            clinical_id,
            payload.get("condition_name"),
            payload.get("date_diagnosed"),
            payload.get("status"),
            payload.get("notes"),
        ),
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_row


@router.delete("/conditions/{condition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_condition(condition_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM chronic_condition WHERE condition_id = %s RETURNING condition_id", (condition_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Condition not found")
    return None


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