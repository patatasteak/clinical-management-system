-- Add missing password_hash column to doctor table
ALTER TABLE doctor ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);

-- Create doctor_id_seq if it doesn't exist and set default for doctor_id
CREATE SEQUENCE IF NOT EXISTS doctor_id_seq START 100000;
ALTER TABLE doctor ALTER COLUMN doctor_id SET DEFAULT nextval('doctor_id_seq');

-- Add feedback column to patient_case table
ALTER TABLE patient_case ADD COLUMN IF NOT EXISTS feedback TEXT;

CREATE TABLE IF NOT EXISTS prescription (
  prescription_id INT PRIMARY KEY AUTO_INCREMENT,
  dosage         DATE        NOT NULL,
  frequency      TEXT        NOT NULL,
  case_id        INT,
  date_start     DATE        NOT NULL,
  date_end       DATE,
  FOREIGN KEY (case_id) REFERENCES Case(case_id)
);

CREATE TABLE IF NOT EXISTS Has (
  med_id          INT NOT NULL,
  prescription_id INT NOT NULL,
  PRIMARY KEY (med_id, prescription_id),
  FOREIGN KEY (med_id)          REFERENCES Medicine(med_id),
  FOREIGN KEY (prescription_id) REFERENCES prescription(prescription_id)
);