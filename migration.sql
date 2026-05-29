-- Add missing password_hash column to doctor table
ALTER TABLE doctor ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);

-- Create doctor_id_seq if it doesn't exist and set default for doctor_id
CREATE SEQUENCE IF NOT EXISTS doctor_id_seq START 100000;
ALTER TABLE doctor ALTER COLUMN doctor_id SET DEFAULT nextval('doctor_id_seq');

-- Add feedback column to patient_case table
ALTER TABLE patient_case ADD COLUMN IF NOT EXISTS feedback TEXT;
