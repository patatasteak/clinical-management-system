
-- Add missing password_hash column to doctor table
ALTER TABLE doctor ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);

-- Create doctor_id_seq if it doesn't exist and set default for doctor_id
CREATE SEQUENCE IF NOT EXISTS doctor_id_seq START 100000;
ALTER TABLE doctor ALTER COLUMN doctor_id SET DEFAULT nextval('doctor_id_seq');

-- Add feedback column to patient_case table
ALTER TABLE patient_case ADD COLUMN IF NOT EXISTS feedback TEXT;

-- Add missing columns to medicine table
ALTER TABLE medicine ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE medicine ADD COLUMN IF NOT EXISTS form VARCHAR(100);
ALTER TABLE medicine ADD COLUMN IF NOT EXISTS strength VARCHAR(100);
ALTER TABLE medicine ADD COLUMN IF NOT EXISTS unit_price DECIMAL(10, 2);

-- Fix "has" table columns if they use med_id
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'has' AND column_name = 'med_id') THEN
        ALTER TABLE has RENAME COLUMN med_id TO medicine_id;
    END IF;
END $$;

