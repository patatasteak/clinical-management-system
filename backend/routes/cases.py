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
	chief_Complaint: Optional[str]
	description: Optional[str]
	appoint_status: Optional[str]
	doctor_id: Optional[int]


@router.get("/{case_id}")
def get_case(case_id: int):
	"""Return full case detail with nested lab_tests (including test name and ordering doctor's name)."""
	conn = get_connection()
	cur = conn.cursor(cursor_factory=RealDictCursor)

	sql = """
	SELECT pc.case_id, pc.appoint_status, pc.chief_Complaint, pc.description, pc.patientid, pc.doctor_id, pc.date_opened, pc.date_closed,
	  json_build_object('doctor_id', d.doctor_id, 'first_name', d.first_name, 'last_name', d.last_name) AS doctor,
	  json_build_object('patientid', p.patientid, 'firstname', p.firstname, 'lastname', p.lastname, 'email', p.email) AS patient,
	  COALESCE(lab.tests, '[]') AS lab_tests
	FROM patient_case pc
	LEFT JOIN doctor d ON d.doctor_id = pc.doctor_id
	LEFT JOIN patient p ON p.patientid = pc.patientid
	LEFT JOIN (
	  SELECT case_id, json_agg(json_build_object('test_id', test_id, 'catalog_id', catalog_id, 'test_name', lt.test_name, 'date_taken', date_taken, 'findings', findings, 'ordered_by', ordered_by)) AS tests
	  FROM lab_test lt
	  LEFT JOIN LabTestCatalog ltc ON ltc.catalog_id = lt.catalog_id
	  GROUP BY case_id
	) lab ON lab.case_id = pc.case_id
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
		"INSERT INTO patient_case (appoint_status, chief_Complaint, description, patientid, doctor_id) VALUES (%s,%s,%s,%s,%s) RETURNING case_id, appoint_status, chief_Complaint, patientid, doctor_id, date_opened",
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
	fields = []
	values = []
	for k, v in payload.dict(exclude_unset=True).items():
		fields.append(f"{k} = %s")
		values.append(v)

	if not fields:
		raise HTTPException(status_code=400, detail="No fields to update")

	values.append(case_id)
	sql = f"UPDATE patient_case SET {', '.join(fields)} WHERE case_id = %s RETURNING case_id, appoint_status, chief_Complaint, patientid, doctor_id, date_opened, date_closed"

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

