from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()


class CaseCreate(BaseModel):
	chief_Complaint: str
	description: Optional[str] = None
	PatientID: int
	doctor_id: int


class CaseUpdate(BaseModel):
    chief_complaint: Optional[str] = None
    chief_Complaint: Optional[str] = None  # Alias for backwards compatibility
    description: Optional[str] = None
    appoint_status: Optional[str] = None
    doctor_id: Optional[int] = None
    feedback: Optional[str] = None


@router.get("/{case_id}")
def get_case(case_id: int):
    """Return full case detail with nested lab_tests (including test name and ordering doctor's name)."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
    SELECT pc.case_id, pc.appoint_status, pc.chief_complaint, pc.description, pc.feedback, pc.patientid, pc.doctor_id, pc.date_opened, pc.date_closed,
     json_build_object('doctor_id', d.doctor_id, 'first_name', d.first_name, 'last_name', d.last_name) AS doctor,
     json_build_object('patientid', p.patientid, 'firstname', p.firstname, 'lastname', p.lastname, 'email', p.email) AS patient,
     COALESCE(lab.tests, '[]') AS lab_tests,
     COALESCE(pr.prescriptions, '[]') AS prescriptions
    FROM patient_case pc
    LEFT JOIN doctor d ON d.doctor_id = pc.doctor_id
    LEFT JOIN patient p ON p.patientid = pc.patientid
    LEFT JOIN (
      SELECT lt.case_id, json_agg(json_build_object(
          'test_id',    lt.test_id,
          'catalog_id', lt.catalog_id,
          'test_name',  ltc.test_name,
          'date_taken', lt.date_taken,
          'findings',   lt.findings,
          'ordered_by', lt.ordered_by
      )) AS tests
      FROM lab_test lt
      LEFT JOIN labtestcatalog ltc ON ltc.catalog_id = lt.catalog_id
      GROUP BY lt.case_id
  ) lab ON lab.case_id = pc.case_id
    LEFT JOIN (
      SELECT p.case_id,
             json_agg(json_build_object(
                 'prescription_id', p.prescription_id,
                 'prescribed_at', p.prescribed_at,
                 'instructions', p.instructions,
                 'prescribed_by', p.prescribed_by,
                 'notes', p.notes,
                 'medicines', COALESCE(pm.medicines, '[]')
             ) ORDER BY p.prescribed_at DESC) AS prescriptions
      FROM prescription p
      LEFT JOIN (
        SELECT "has".prescription_id,
               json_agg(json_build_object(
 'medicine_id', m.medicine_id,
 'medicine_name', m.medicine_name,
 'medicine_type', m.medicine_type,
 'quantity', "has".quantity,
 'dosage', "has".dosage,
 'frequency', "has".frequency
)) AS medicines
        FROM "has"
        JOIN medicine m ON m.medicine_id = "has".medicine_id
        GROUP BY "has".prescription_id
      ) pm ON pm.prescription_id = p.prescription_id
      GROUP BY p.case_id
  ) pr ON pr.case_id = pc.case_id
WHERE pc.case_id = %s
    """

    cur.execute(sql, (case_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Case not found")

    # For each lab test, enrich ordered_by with doctor's name if possible
    # (ordered_by currently returns doctor id; client can join if needed)
    return row


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate):
	conn = get_connection()
	cur = conn.cursor(cursor_factory=RealDictCursor)
	cur.execute(
		"INSERT INTO patient_case (appoint_status, chief_complaint, description, patientid, doctor_id) VALUES (%s,%s,%s,%s,%s) RETURNING case_id, appoint_status, chief_complaint, patientid, doctor_id, date_opened",
		(
			'Pending',
			payload.chief_Complaint,
			payload.description,
			payload.PatientID,
			payload.doctor_id,
		),
	)
	new_row = cur.fetchone()
	conn.commit()
	cur.close()
	conn.close()
	return new_row


@router.put("/{case_id}")
def update_case(case_id: int, payload: CaseUpdate):
	# Field name mapping from model fields to database columns
	field_mapping = {
		"chief_complaint": "chief_complaint",
		"chief_Complaint": "chief_complaint",
		"description": "description",
		"appoint_status": "appoint_status",
		"doctor_id": "doctor_id",
		"feedback": "feedback"
	}
	
	fields = []
	values = []
	processed_fields = set()
	
	payload_dict = payload.dict(exclude_unset=True)
	
	for k, v in payload_dict.items():
		db_column = field_mapping.get(k)
		if db_column and db_column not in processed_fields:
			fields.append(f"{db_column} = %s")
			values.append(v)
			processed_fields.add(db_column)

	if not fields:
		raise HTTPException(status_code=400, detail="No fields to update")

	values.append(case_id)
	sql = f"UPDATE patient_case SET {', '.join(fields)} WHERE case_id = %s RETURNING case_id, appoint_status, chief_complaint, patientid, doctor_id, date_opened, date_closed"

	conn = get_connection()
	cur = conn.cursor(cursor_factory=RealDictCursor)
	cur.execute(sql, tuple(values))
	updated = cur.fetchone()
	conn.commit()
	cur.close()
	conn.close()

	if not updated:
		raise HTTPException(status_code=404, detail="Case not found")

	return updated


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    # First check if case exists
    cur.execute("SELECT case_id FROM patient_case WHERE case_id = %s", (case_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Delete case
    cur.execute("DELETE FROM patient_case WHERE case_id = %s", (case_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    return None

