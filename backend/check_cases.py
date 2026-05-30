
from database import get_connection

def check_cases():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT case_id, patientid, chief_complaint FROM patient_case")
    rows = cur.fetchall()
    print("Existing Cases:")
    for row in rows:
        print(f"Case ID: {row[0]}, Patient ID: {row[1]}, Complaint: {row[2]}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_cases()
