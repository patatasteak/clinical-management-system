from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database import get_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()


class VitalCreate(BaseModel):
    PatientID: int
    weight: float = None
    height: float = None
    temperature: float = None
    blood_pressure: str = None
    pulse_rate: int = None


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vital(payload: VitalCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO vital_stats (patientid, weight, height, temperature, blood_pressure, pulse_rate) VALUES (%s,%s,%s,%s,%s,%s) RETURNING stat_id, recorded_at, weight, height, temperature, blood_pressure, pulse_rate",
        (
            payload.PatientID,
            payload.weight,
            payload.height,
            payload.temperature,
            payload.blood_pressure,
            payload.pulse_rate,
        ),
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_row
