-- ============================================================
-- CLINIC MANAGEMENT SYSTEM — SCHEMA (v0, based on ERD draft)
-- ============================================================
-- TODO: Add the following entities in a future version:
--   - lab_test_catalog  (reference table for test types)
--   - lab_test          (individual results tied to a case)
--   - prescription      (medications issued per case/visit)
-- ============================================================
DROP TABLE IF EXISTS clinical_background CASCADE;
DROP TABLE IF EXISTS vital_stats CASCADE;
DROP TABLE IF EXISTS insurance CASCADE;
DROP TABLE IF EXISTS patient_case CASCADE;
DROP TABLE IF EXISTS doctor CASCADE;
DROP TABLE IF EXISTS patient CASCADE;
-- ============================================================
-- PATIENT
-- ============================================================
CREATE TABLE patient (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    nationality VARCHAR(50),
    sex CHAR(1) CHECK (sex IN ('M', 'F', 'O')),
    philhealth_id INT,
    email VARCHAR(50),
    blood_type VARCHAR(2) CHECK (
        blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
    ),
    emergency_contact VARCHAR(50),
    contact_num VARCHAR(50),
    birthday DATE,
    address VARCHAR(50)
);
-- ============================================================
-- DOCTOR
-- ============================================================
CREATE TABLE doctor (
    doctor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    sex VARCHAR(1) CHECK (sex IN ('M', 'F', 'O')),
    license_no INT,
    email VARCHAR(50),
    years_exp INT,
    specialization VARCHAR(50),
    contact_no VARCHAR(50) -- kept as varchar, int would break leading zeros
);
-- ============================================================
-- CASE
-- ============================================================
CREATE TABLE patient_case (
    case_id SERIAL PRIMARY KEY,
    date_opened DATE,
    date_closed DATE,
    chief_complaint TEXT,
    patient_id INT NOT NULL REFERENCES patient(patient_id) ON DELETE CASCADE,
    doctor_id INT NOT NULL REFERENCES doctor(doctor_id),
    CONSTRAINT closed_date_check CHECK (
        date_closed IS NULL
        OR date_closed >= date_opened
    )
);
-- ============================================================
-- VITAL STATS
-- weight/height typed as numeric — ERD shows 'date' which is
-- likely a tool mistake
-- ============================================================
CREATE TABLE vital_stats (
    stat_id SERIAL PRIMARY KEY,
    recorded_at DATE NOT NULL,
    weight NUMERIC(5, 2),
    -- in kg
    height NUMERIC(5, 2),
    -- in cm
    patient_id INT NOT NULL REFERENCES patient(patient_id) ON DELETE CASCADE
);
-- ============================================================
-- INSURANCE
-- ============================================================
CREATE TABLE insurance (
    insurance_id SERIAL PRIMARY KEY,
    provider VARCHAR(50),
    expiry DATE,
    policy TEXT,
    patient_id INT NOT NULL REFERENCES patient(patient_id) ON DELETE CASCADE
);
-- ============================================================
-- CLINICAL BACKGROUND
-- tied to both a patient and a specific case per your ERD
-- note: revisit with prof whether this should be per-patient
-- (single living record) or per-case (snapshot per visit)
-- ============================================================
CREATE TABLE clinical_background (
    clinical_id SERIAL PRIMARY KEY,
    allergen TEXT,
    disability TEXT,
    alcohol_use VARCHAR(50),
    smoking_status VARCHAR(50),
    notes TEXT,
    patient_id INT NOT NULL REFERENCES patient(patient_id) ON DELETE CASCADE,
    case_id INT NOT NULL REFERENCES patient_case(case_id) ON DELETE CASCADE
);