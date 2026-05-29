-- ============================================================
-- CLINIC MANAGEMENT SYSTEM — SCHEMA
-- ============================================================
DROP TABLE IF EXISTS lab_test CASCADE;
DROP TABLE IF EXISTS "has" CASCADE;
DROP TABLE IF EXISTS prescription CASCADE;
DROP TABLE IF EXISTS medicine CASCADE;
DROP TABLE IF EXISTS LabTestCatalog CASCADE;
DROP TABLE IF EXISTS past_surgery CASCADE;
DROP TABLE IF EXISTS disability CASCADE;
DROP TABLE IF EXISTS allergy CASCADE;
DROP TABLE IF EXISTS clinical_background CASCADE;
DROP TABLE IF EXISTS vital_stats CASCADE;
DROP TABLE IF EXISTS patient_case CASCADE;
DROP TABLE IF EXISTS doctor CASCADE;
DROP TABLE IF EXISTS patient CASCADE;
DROP TABLE IF EXISTS admin_user CASCADE;
DROP SEQUENCE IF EXISTS patient_id_seq;
-- ============================================================
-- ADMIN USERS
-- ============================================================
CREATE TABLE admin_user (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('superadmin', 'staff'))
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
    email VARCHAR(100),
    years_exp INT,
    specialization VARCHAR(100),
    contact_number VARCHAR(50),
    role VARCHAR(20) DEFAULT 'resident',
    is_active BOOLEAN DEFAULT TRUE
);
-- ============================================================
-- PATIENT
-- ============================================================
CREATE SEQUENCE patient_id_seq START 1;
CREATE TABLE patient (
    PatientID INT PRIMARY KEY DEFAULT nextval('patient_id_seq'),
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Nationality VARCHAR(50),
    Sex VARCHAR(10) CHECK (Sex IN ('male', 'female', 'other')),
    Address TEXT,
    contactNumber VARCHAR(50),
    BloodType VARCHAR(3) CHECK (
        BloodType IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
    ),
    email VARCHAR(100) UNIQUE NOT NULL,
    birthday DATE,
    emergencyContact VARCHAR(50),
    password_hash VARCHAR(255) NOT NULL
);
-- ============================================================
-- CASE
-- ============================================================
CREATE TABLE patient_case (
    case_id SERIAL PRIMARY KEY,
    appoint_status VARCHAR(20) DEFAULT 'Pending' CHECK (
        appoint_status IN ('Pending', 'Ongoing', 'Closed')
    ),
    chief_Complaint TEXT NOT NULL,
    -- Case Name
    description TEXT,
    PatientID INT NOT NULL REFERENCES patient(PatientID) ON DELETE CASCADE,
    doctor_id INT NOT NULL REFERENCES doctor(doctor_id),
    date_opened TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_closed TIMESTAMP
);
-- ============================================================
-- VITAL STATS
-- ============================================================
CREATE TABLE vital_stats (
    stat_id SERIAL PRIMARY KEY,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    weight NUMERIC(5, 2),
    -- in kg
    height NUMERIC(5, 2),
    -- in cm
    temperature NUMERIC(4, 1),
    blood_pressure VARCHAR(20),
    pulse_rate INT,
    PatientID INT NOT NULL REFERENCES patient(PatientID) ON DELETE CASCADE
);
-- ============================================================
-- CLINICAL BACKGROUND
-- ============================================================
CREATE TABLE clinical_background (
    clinical_id SERIAL PRIMARY KEY,
    case_id INT NOT NULL REFERENCES patient_case(case_id) ON DELETE CASCADE,
    smoking_status VARCHAR(50),
    alcohol_use VARCHAR(50),
    notes TEXT
);
-- ============================================================
-- ALLERGY
-- ============================================================
CREATE TABLE allergy (
    allergy_id SERIAL PRIMARY KEY,
    clinical_id INT NOT NULL REFERENCES clinical_background(clinical_id) ON DELETE CASCADE,
    allergen VARCHAR(100) NOT NULL,
    reaction TEXT,
    severity VARCHAR(20) CHECK (severity IN ('mild', 'moderate', 'severe')),
    noted_date DATE
);
-- ============================================================
-- DISABILITY
-- ============================================================
CREATE TABLE disability (
    disability_id SERIAL PRIMARY KEY,
    clinical_id INT NOT NULL REFERENCES clinical_background(clinical_id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    congenital BOOLEAN DEFAULT FALSE,
    notes TEXT
);
-- ============================================================
-- PAST SURGERY
-- ============================================================
CREATE TABLE past_surgery (
    surgery_id SERIAL PRIMARY KEY,
    clinical_id INT NOT NULL REFERENCES clinical_background(clinical_id) ON DELETE CASCADE,
    procedure_name VARCHAR(100) NOT NULL,
    date_performed DATE,
    hospital VARCHAR(255),
    notes TEXT
);
-- ============================================================
-- LAB TEST CATALOG
-- ============================================================
CREATE TABLE LabTestCatalog (
    catalog_id VARCHAR(10) PRIMARY KEY,
    -- e.g. LT0001
    test_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);
-- ============================================================
-- LAB TEST
-- ============================================================
CREATE TABLE lab_test (
    test_id SERIAL PRIMARY KEY,
    case_id INT NOT NULL REFERENCES patient_case(case_id) ON DELETE CASCADE,
    catalog_id VARCHAR(10) NOT NULL REFERENCES LabTestCatalog(catalog_id),
    date_taken DATE NOT NULL,
    findings TEXT,
    ordered_by INT REFERENCES doctor(doctor_id)
);
-- todo make labtest results
-- ============================================================
-- PRESCRIPTIONS / MEDICINES
-- ============================================================
CREATE TABLE medicine (
    medicine_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    form VARCHAR(50),
    strength VARCHAR(50),
    unit_price DECIMAL(10, 2)
);
CREATE TABLE prescription (
    prescription_id SERIAL PRIMARY KEY,
    case_id INT NOT NULL REFERENCES patient_case(case_id) ON DELETE CASCADE,
    prescribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    instructions TEXT,
    prescribed_by INT NOT NULL REFERENCES doctor(doctor_id),
    notes TEXT
);
CREATE TABLE "has" (
    prescription_id INT NOT NULL REFERENCES prescription(prescription_id) ON DELETE CASCADE,
    medicine_id INT NOT NULL REFERENCES medicine(medicine_id),
    quantity INT NOT NULL DEFAULT 1,
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    PRIMARY KEY (prescription_id, medicine_id)
);