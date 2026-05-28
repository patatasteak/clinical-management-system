-- ============================================================
-- CLINIC MANAGEMENT SYSTEM — SEED DATA
-- Run schema.sql first before this file
-- PatientIDs start at 1 (sequence starts at 1)
-- ============================================================
-- ============================================================
-- ADMIN USERS
-- ============================================================
INSERT INTO admin_user (name, email, password_hash, role)
VALUES (
        'Admin Staff',
        'admin@clinicms.ph',
        'changeme_hash',
        'superadmin'
    ),
    (
        'Reception Desk',
        'reception@clinicms.ph',
        'changeme_hash',
        'staff'
    );
-- ============================================================
-- DOCTORS
-- ============================================================
INSERT INTO doctor (
        first_name,
        last_name,
        sex,
        license_no,
        email,
        years_exp,
        specialization,
        contact_number,
        role,
        is_active
    )
VALUES (
        'Anna',
        'Cruz',
        'F',
        1001,
        'a.cruz@clinicms.ph',
        8,
        'Internal Medicine',
        '0917-555-0011',
        'attending',
        TRUE
    ),
    (
        'Ben',
        'Marcos',
        'M',
        1002,
        'b.marcos@clinicms.ph',
        2,
        'Cardiology',
        '0928-555-0022',
        'resident',
        TRUE
    ),
    (
        'Clara',
        'Lim',
        'F',
        1003,
        'c.lim@clinicms.ph',
        5,
        'Pediatrics',
        '0935-555-0033',
        'consultant',
        TRUE
    ),
    (
        'Dante',
        'Tan',
        'M',
        1004,
        'd.tan@clinicms.ph',
        11,
        'General Practice',
        '0945-555-0044',
        'attending',
        TRUE
    ),
    (
        'Elena',
        'Vega',
        'F',
        1005,
        'e.vega@clinicms.ph',
        3,
        'Neurology',
        '0956-555-0055',
        'resident',
        TRUE
    );
-- ============================================================
-- PATIENTS
-- PatientIDs will be 1, 2, 3, 4, 5
-- ============================================================
INSERT INTO patient (
        FirstName,
        LastName,
        Nationality,
        Sex,
        Address,
        contactNumber,
        BloodType,
        email,
        birthday,
        emergencyContact,
        password_hash
    )
VALUES (
        'Maria',
        'Reyes',
        'Filipino',
        'female',
        '123 Mango Ave, Lahug, Cebu City, 6000',
        '0917-234-5678',
        'A+',
        'maria.reyes@email.com',
        '1986-03-14',
        'Pedro Reyes - 0917-987-6543',
        'changeme_hash'
    ),
    (
        'Jose',
        'Dela Cruz',
        'Filipino',
        'male',
        '45 Osmena Blvd, Pardo, Cebu City, 6000',
        '0928-765-4321',
        'O+',
        'jdelacruz@email.com',
        '1972-06-08',
        'Rosa Dela Cruz - 0928-111-2222',
        'changeme_hash'
    ),
    (
        'Liza',
        'Santos',
        'Filipino',
        'female',
        '88 Colon St, Parian, Cebu City, 6000',
        '0935-111-9922',
        'B-',
        'liza.santos@email.com',
        '1995-11-20',
        'Nena Santos - 0935-444-5555',
        'changeme_hash'
    ),
    (
        'Roberto',
        'Mendoza',
        'Filipino',
        'male',
        '22 Leon Kilat St, Kalubihan, Cebu City, 6000',
        '0945-888-3300',
        'AB+',
        'r.mendoza@email.com',
        '1963-02-03',
        'Carmen Mendoza - 0945-777-6600',
        'changeme_hash'
    ),
    (
        'Ana',
        'Villanueva',
        'Filipino',
        'female',
        '7 Jakosalem St, Cebu City, 6000',
        '0956-432-7711',
        'O-',
        'ana.villanueva@email.com',
        '1980-08-30',
        'Marco Villanueva - 0956-333-4444',
        'changeme_hash'
    );
-- ============================================================
-- VITAL STATS
-- ============================================================
INSERT INTO vital_stats (
        weight,
        height,
        temperature,
        blood_pressure,
        pulse_rate,
        PatientID
    )
VALUES (62.5, 158.0, 36.8, '150/95', 88, 1),
    (78.0, 170.0, 36.5, '145/90', 82, 2),
    (52.0, 162.0, 37.1, '110/70', 94, 3),
    (80.5, 165.0, 36.6, '128/82', 76, 4),
    (65.0, 160.0, 36.7, '118/75', 80, 5);
-- ============================================================
-- INSURANCE
-- ============================================================
INSERT INTO insurance (provider, expiry, policy_number, PatientID)
VALUES ('PhilHealth', '2027-12-31', 'PH-123456789', 1),
    ('Maxicare', '2026-06-30', 'MX-987654321', 2),
    ('PhilHealth', '2027-12-31', 'PH-456789123', 3),
    ('Medicard', '2026-09-30', 'MD-321654987', 4),
    ('PhilHealth', '2027-12-31', 'PH-789123456', 5);
-- ============================================================
-- CLINICAL BACKGROUND
-- ============================================================
INSERT INTO clinical_background (smoking_status, alcohol_use, notes, PatientID)
VALUES (
        'non-smoker',
        'occasional',
        'Managed diabetic, hypertensive',
        1
    ),
    (
        'active smoker',
        'non-drinker',
        '10 pack-years, early COPD',
        2
    ),
    (
        'non-smoker',
        'non-drinker',
        'Bronchial asthma since childhood',
        3
    ),
    (
        'former smoker (quit 2018)',
        'occasional',
        'Post-CABG, mild hearing impairment',
        4
    ),
    (
        'non-smoker',
        'non-drinker',
        'Hypothyroid, two prior C-sections',
        5
    );
-- ============================================================
-- ALLERGIES
-- ============================================================
INSERT INTO allergy (
        clinical_id,
        allergen,
        reaction,
        severity,
        noted_date
    )
VALUES (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 1),
        'Penicillin',
        'Rash and hives',
        'moderate',
        '2015-06-01'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 1),
        'Shellfish',
        'Swelling of lips and throat',
        'severe',
        '2018-02-10'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 2),
        'Aspirin',
        'Gastric bleeding',
        'severe',
        '2020-09-15'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 3),
        'Dust mites',
        'Sneezing and asthma trigger',
        'moderate',
        '2010-03-22'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 3),
        'NSAIDs',
        'Bronchospasm',
        'severe',
        '2016-07-08'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 5),
        'Latex',
        'Contact dermatitis',
        'mild',
        '2008-11-30'
    );
-- ============================================================
-- CHRONIC CONDITIONS
-- ============================================================
INSERT INTO chronic_condition (
        clinical_id,
        condition_name,
        date_diagnosed,
        status,
        notes
    )
VALUES (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 1),
        'Type 2 Diabetes',
        '2018-05-20',
        'active',
        'On Metformin 500mg twice daily'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 1),
        'Hypertension',
        '2019-03-11',
        'active',
        'On Amlodipine 5mg OD'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 2),
        'Hypertension',
        '2015-08-04',
        'active',
        'On Losartan 50mg OD'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 2),
        'Stage 1 COPD',
        '2022-01-17',
        'active',
        'Spirometry confirmed, on SABA PRN'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 3),
        'Bronchial Asthma',
        '2005-09-12',
        'active',
        'Salbutamol inhaler PRN, ICS controller'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 4),
        'Type 2 Diabetes',
        '2016-04-29',
        'managed',
        'HbA1c stable at 6.8%, on Metformin'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 5),
        'Hypothyroidism',
        '2014-07-15',
        'active',
        'On Levothyroxine, dose under review'
    );
-- ============================================================
-- DISABILITIES
-- ============================================================
INSERT INTO disability (clinical_id, description, congenital, notes)
VALUES (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 4),
        'Mild hearing impairment (left ear)',
        FALSE,
        'Acquired, likely noise-induced'
    );
-- ============================================================
-- PAST SURGERIES
-- ============================================================
INSERT INTO past_surgery (
        clinical_id,
        procedure_name,
        date_performed,
        hospital,
        notes
    )
VALUES (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 1),
        'Appendectomy',
        '2010-07-14',
        'Cebu Doctors University Hospital',
        'Uncomplicated, full recovery'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 4),
        'Coronary Artery Bypass Grafting (CABG)',
        '2019-11-03',
        'Vicente Sotto Memorial Medical Center',
        '3-vessel CABG, stable post-op'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 4),
        'Cataract Surgery (left eye)',
        '2022-06-20',
        'Cebu Eye Center',
        'Phacoemulsification with IOL implant'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 5),
        'Cesarean Section',
        '2010-04-02',
        'Chong Hua Hospital',
        'First delivery'
    ),
    (
        (SELECT clinical_id FROM clinical_background WHERE PatientID = 5),
        'Cesarean Section',
        '2013-08-18',
        'Chong Hua Hospital',
        'Second delivery'
    );
-- ============================================================
-- LAB TEST CATALOG
-- ============================================================
INSERT INTO LabTestCatalog (catalog_id, test_name, description, price)
VALUES (
        'LT0001',
        'CBC',
        'Complete Blood Count',
        350.00
    ),
    (
        'LT0002',
        'FBS',
        'Fasting Blood Sugar',
        150.00
    ),
    (
        'LT0003',
        'HbA1c',
        'Glycated Hemoglobin',
        650.00
    ),
    (
        'LT0004',
        'BMP',
        'Basic Metabolic Panel',
        800.00
    ),
    (
        'LT0005',
        'Lipid Panel',
        'Total cholesterol, LDL, HDL, triglycerides',
        900.00
    ),
    (
        'LT0006',
        'TSH',
        'Thyroid Stimulating Hormone',
        750.00
    ),
    (
        'LT0007',
        'Free T4',
        'Free Thyroxine',
        700.00
    ),
    (
        'LT0008',
        'Urinalysis',
        'Urine examination',
        120.00
    ),
    (
        'LT0009',
        'ECG',
        'Electrocardiogram',
        500.00
    ),
    (
        'LT0010',
        'Chest X-Ray',
        'Radiograph of chest cavity',
        600.00
    ),
    (
        'LT0011',
        'Peak Flow Meter',
        'Measures maximum exhalation speed',
        200.00
    ),
    (
        'LT0012',
        'ABG',
        'Arterial Blood Gas',
        950.00
    );
-- ============================================================
-- PATIENT CASES
-- doctor_id: 1=Cruz, 2=Marcos, 3=Lim, 4=Tan, 5=Vega
-- PatientID: 1=Maria, 2=Jose, 3=Liza, 4=Roberto, 5=Ana
-- ============================================================
INSERT INTO patient_case (
        appoint_status,
        chief_Complaint,
        description,
        PatientID,
        doctor_id,
        date_opened,
        date_closed
    )
VALUES (
        'Ongoing',
        'Persistent chest pain and shortness of breath',
        'Patient reports intermittent chest tightness lasting 3-5 minutes, accompanied by mild dyspnea. BP elevated at 150/95 mmHg on admission.',
        1,
        1,
        '2026-05-20',
        NULL
    ),
    (
        'Closed',
        'Uncontrolled blood glucose levels',
        'HbA1c at 9.2% on last check. Patient admits poor dietary compliance.',
        1,
        4,
        '2026-02-03',
        '2026-03-15'
    ),
    (
        'Closed',
        'Annual physical examination',
        'Routine annual checkup. All vitals stable. BMI 27.4. No new complaints.',
        1,
        1,
        '2025-08-10',
        '2025-08-10'
    ),
    (
        'Ongoing',
        'Productive cough and fatigue for 2 weeks',
        'Chronic smoker presenting with productive cough, mild hemoptysis, fatigue. SpO2 94% on room air.',
        2,
        2,
        '2026-05-15',
        NULL
    ),
    (
        'Ongoing',
        'Recurrent asthma exacerbation',
        'Third exacerbation this year. Peak flow reading at 68% predicted. Salbutamol nebulization administered in clinic.',
        3,
        1,
        '2026-05-10',
        NULL
    ),
    (
        'Closed',
        'Routine hypertension follow-up',
        'BP 128/82 mmHg on current medication. No complaints. Stable.',
        4,
        4,
        '2025-11-05',
        '2025-11-05'
    ),
    (
        'Ongoing',
        'Fatigue and unexplained weight gain',
        'TSH elevated at 7.8 mIU/L. Patient reports fatigue, cold intolerance, 4kg weight gain over 3 months.',
        5,
        1,
        '2026-05-18',
        NULL
    );
-- ============================================================
-- MEDICINES
-- ============================================================
INSERT INTO medicine (name, description, form, strength, unit_price)
VALUES (
        'Metformin',
        'Oral anti-diabetic medication',
        'tablet',
        '500mg',
        0.25
    ),
    (
        'Amlodipine',
        'Calcium channel blocker for hypertension',
        'tablet',
        '5mg',
        0.30
    ),
    (
        'Salbutamol',
        'Short-acting bronchodilator',
        'inhaler',
        '100mcg',
        4.50
    ),
    (
        'Levothyroxine',
        'Thyroid hormone replacement',
        'tablet',
        '50mcg',
        0.45
    ),
    (
        'Atorvastatin',
        'Lipid lowering agent',
        'tablet',
        '20mg',
        0.40
    );

-- ============================================================
-- PRESCRIPTIONS
-- ============================================================
INSERT INTO prescription (case_id, prescribed_by, instructions, notes)
VALUES (
        1,
        1,
        'Take once daily after breakfast',
        'For blood pressure control and chest pain management'
    ),
    (
        2,
        4,
        'Take twice daily with meals',
        'Manage elevated blood glucose levels'
    ),
    (
        5,
        1,
        'Use two puffs every 6 hours as needed',
        'Asthma maintenance and rescue support'
    ),
    (
        7,
        1,
        'Take one tablet once daily before breakfast',
        'Hypothyroidism maintenance therapy'
    );

-- ============================================================
-- PRESCRIPTION MEDICINES
-- ============================================================
INSERT INTO "has" (prescription_id, medicine_id, quantity, dosage, frequency)
VALUES (
        1,
        1,
        1,
        '500mg',
        'once daily'
    ),
    (
        1,
        2,
        1,
        '5mg',
        'once daily'
    ),
    (
        2,
        1,
        2,
        '500mg',
        'twice daily'
    ),
    (
        3,
        3,
        2,
        '100mcg',
        'every 6 hours as needed'
    ),
    (
        4,
        4,
        1,
        '50mcg',
        'once daily'
    );

-- ============================================================
-- LAB TESTS
-- case_id 1-7 in order of inserts above
-- ============================================================
INSERT INTO lab_test (
        case_id,
        catalog_id,
        date_taken,
        findings,
        ordered_by
    )
VALUES (
        1,
        'LT0009',
        '2026-05-20',
        'Sinus rhythm, no ST-segment changes. Minor T-wave inversion in V4-V5.',
        1
    ),
    (
        1,
        'LT0001',
        '2026-05-20',
        'WBC 8.2 x10³/μL, RBC 4.5 x10⁶/μL, Hgb 13.1 g/dL — within normal limits.',
        1
    ),
    (
        2,
        'LT0003',
        '2026-02-03',
        'HbA1c 9.2% — poorly controlled. Target <7%.',
        4
    ),
    (
        2,
        'LT0002',
        '2026-02-03',
        'Fasting blood sugar 182 mg/dL — elevated.',
        4
    ),
    (
        3,
        'LT0008',
        '2025-08-10',
        'Normal, no proteinuria or glycosuria.',
        1
    ),
    (
        3,
        'LT0005',
        '2025-08-10',
        'Total cholesterol 214 mg/dL, LDL 138 mg/dL — borderline elevated.',
        1
    ),
    (
        4,
        'LT0010',
        '2026-05-15',
        'Mild hyperinflation, no infiltrates. Consistent with early COPD.',
        2
    ),
    (
        4,
        'LT0001',
        '2026-05-15',
        'WBC 10.1 x10³/μL — slightly elevated, possible infectious component.',
        2
    ),
    (
        5,
        'LT0011',
        '2026-05-10',
        '68% of predicted — moderate obstruction.',
        1
    ),
    (
        5,
        'LT0012',
        '2026-05-10',
        'pH 7.42, PaO2 88 mmHg, PaCO2 36 mmHg — mild hypoxemia.',
        1
    ),
    (
        6,
        'LT0004',
        '2025-11-05',
        'Creatinine 1.0 mg/dL, K+ 4.2 mEq/L — normal renal function.',
        4
    ),
    (
        7,
        'LT0006',
        '2026-05-18',
        'TSH 7.8 mIU/L — elevated, consistent with hypothyroidism.',
        1
    ),
    (
        7,
        'LT0007',
        '2026-05-18',
        'Free T4 0.7 ng/dL — low-normal.',
        1
    );