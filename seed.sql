-- ============================================================
-- CLINIC MANAGEMENT SYSTEM — SEED DATA
-- Run schema.sql first before this file
-- ============================================================
-- ============================================================
-- ADMIN USERS
-- passwords are placeholder hashes — replace before going live
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
        specialization,
        role,
        contact_number,
        email,
        is_active
    )
VALUES (
        'Anna',
        'Cruz',
        'Internal Medicine',
        'attending',
        '0917-555-0011',
        'a.cruz@clinicms.ph',
        TRUE
    ),
    (
        'Ben',
        'Marcos',
        'Cardiology',
        'resident',
        '0928-555-0022',
        'b.marcos@clinicms.ph',
        TRUE
    ),
    (
        'Clara',
        'Lim',
        'Pediatrics',
        'consultant',
        '0935-555-0033',
        'c.lim@clinicms.ph',
        TRUE
    ),
    (
        'Dante',
        'Tan',
        'General Practice',
        'attending',
        '0945-555-0044',
        'd.tan@clinicms.ph',
        TRUE
    ),
    (
        'Elena',
        'Vega',
        'Neurology',
        'resident',
        '0956-555-0055',
        'e.vega@clinicms.ph',
        TRUE
    );
-- ============================================================
-- PATIENTS
-- ============================================================
INSERT INTO patient (
        first_name,
        last_name,
        date_of_birth,
        sex,
        blood_type,
        contact_number,
        email,
        street_address,
        barangay,
        city,
        province,
        zip_code,
        emergency_contact_name,
        emergency_contact_number
    )
VALUES (
        'Maria',
        'Reyes',
        '1986-03-14',
        'female',
        'A+',
        '0917-234-5678',
        'maria.reyes@email.com',
        '123 Mango Ave',
        'Lahug',
        'Cebu City',
        'Cebu',
        '6000',
        'Pedro Reyes',
        '0917-987-6543'
    ),
    (
        'Jose',
        'Dela Cruz',
        '1972-06-08',
        'male',
        'O+',
        '0928-765-4321',
        'jdelacruz@email.com',
        '45 Osmena Blvd',
        'Pardo',
        'Cebu City',
        'Cebu',
        '6000',
        'Rosa Dela Cruz',
        '0928-111-2222'
    ),
    (
        'Liza',
        'Santos',
        '1995-11-20',
        'female',
        'B-',
        '0935-111-9922',
        'liza.santos@email.com',
        '88 Colon St',
        'Parian',
        'Cebu City',
        'Cebu',
        '6000',
        'Nena Santos',
        '0935-444-5555'
    ),
    (
        'Roberto',
        'Mendoza',
        '1963-02-03',
        'male',
        'AB+',
        '0945-888-3300',
        'r.mendoza@email.com',
        '22 Leon Kilat St',
        'Kalubihan',
        'Cebu City',
        'Cebu',
        '6000',
        'Carmen Mendoza',
        '0945-777-6600'
    ),
    (
        'Ana',
        'Villanueva',
        '1980-08-30',
        'female',
        'O-',
        '0956-432-7711',
        'ana.villanueva@email.com',
        '7 Jakosalem St',
        'Cebu City',
        'Cebu City',
        'Cebu',
        '6000',
        'Marco Villanueva',
        '0956-333-4444'
    );
-- ============================================================
-- CLINICAL BACKGROUND
-- one row per patient
-- ============================================================
INSERT INTO clinical_background (patient_id, smoking_status, alcohol_use)
VALUES (1, 'non-smoker', 'occasional'),
    (2, 'active smoker', 'non-drinker'),
    (3, 'non-smoker', 'non-drinker'),
    (4, 'former smoker (quit 2018)', 'occasional'),
    (5, 'non-smoker', 'non-drinker');
-- ============================================================
-- ALLERGIES
-- ============================================================
INSERT INTO allergy (
        patient_id,
        allergen,
        reaction,
        severity,
        noted_date
    )
VALUES (
        1,
        'Penicillin',
        'Rash and hives',
        'moderate',
        '2015-06-01'
    ),
    (
        1,
        'Shellfish',
        'Swelling of lips and throat',
        'severe',
        '2018-02-10'
    ),
    (
        2,
        'Aspirin',
        'Gastric bleeding',
        'severe',
        '2020-09-15'
    ),
    (
        3,
        'Dust mites',
        'Sneezing and asthma trigger',
        'moderate',
        '2010-03-22'
    ),
    (
        3,
        'NSAIDs',
        'Bronchospasm',
        'severe',
        '2016-07-08'
    ),
    (
        5,
        'Latex',
        'Contact dermatitis',
        'mild',
        '2008-11-30'
    );
-- ============================================================
-- CHRONIC CONDITIONS
-- ============================================================
INSERT INTO chronic_condition (
        patient_id,
        condition_name,
        date_diagnosed,
        status,
        notes
    )
VALUES (
        1,
        'Type 2 Diabetes',
        '2018-05-20',
        'active',
        'On Metformin 500mg twice daily'
    ),
    (
        1,
        'Hypertension',
        '2019-03-11',
        'active',
        'On Amlodipine 5mg OD'
    ),
    (
        2,
        'Hypertension',
        '2015-08-04',
        'active',
        'On Losartan 50mg OD'
    ),
    (
        2,
        'Stage 1 COPD',
        '2022-01-17',
        'active',
        'Spirometry confirmed, on SABA PRN'
    ),
    (
        3,
        'Bronchial Asthma',
        '2005-09-12',
        'active',
        'Salbutamol inhaler PRN, ICS controller'
    ),
    (
        4,
        'Type 2 Diabetes',
        '2016-04-29',
        'managed',
        'HbA1c stable at 6.8%, on Metformin'
    ),
    (
        5,
        'Hypothyroidism',
        '2014-07-15',
        'active',
        'On Levothyroxine, dose under review'
    );
-- ============================================================
-- DISABILITIES
-- ============================================================
INSERT INTO disability (patient_id, description, congenital, notes)
VALUES (
        4,
        'Mild hearing impairment (left ear)',
        FALSE,
        'Acquired, likely noise-induced'
    );
-- ============================================================
-- PAST SURGERIES
-- ============================================================
INSERT INTO past_surgery (
        patient_id,
        procedure_name,
        date_performed,
        hospital,
        notes
    )
VALUES (
        1,
        'Appendectomy',
        '2010-07-14',
        'Cebu Doctors University Hospital',
        'Uncomplicated, full recovery'
    ),
    (
        4,
        'Coronary Artery Bypass Grafting (CABG)',
        '2019-11-03',
        'Vicente Sotto Memorial Medical Center',
        '3-vessel CABG, stable post-op'
    ),
    (
        4,
        'Cataract Surgery (left eye)',
        '2022-06-20',
        'Cebu Eye Center',
        'Phacoemulsification with IOL implant'
    ),
    (
        5,
        'Cesarean Section',
        '2010-04-02',
        'Chong Hua Hospital',
        'First delivery'
    ),
    (
        5,
        'Cesarean Section',
        '2013-08-18',
        'Chong Hua Hospital',
        'Second delivery'
    );
-- ============================================================
-- LAB TEST CATALOG
-- ============================================================
INSERT INTO lab_test_catalog (test_name, category, description)
VALUES (
        'CBC',
        'Hematology',
        'Complete Blood Count — evaluates overall blood health'
    ),
    (
        'FBS',
        'Chemistry',
        'Fasting Blood Sugar — screens for diabetes'
    ),
    (
        'HbA1c',
        'Chemistry',
        'Glycated hemoglobin — 3-month average blood glucose'
    ),
    (
        'BMP',
        'Chemistry',
        'Basic Metabolic Panel — kidney function, electrolytes'
    ),
    (
        'Lipid Panel',
        'Chemistry',
        'Total cholesterol, LDL, HDL, triglycerides'
    ),
    (
        'TSH',
        'Endocrinology',
        'Thyroid Stimulating Hormone'
    ),
    (
        'Free T4',
        'Endocrinology',
        'Free Thyroxine — thyroid function'
    ),
    (
        'Urinalysis',
        'Microbiology',
        'Urine examination for infection, kidney issues'
    ),
    (
        'ECG',
        'Cardiology',
        'Electrocardiogram — heart rhythm and electrical activity'
    ),
    (
        'Chest X-Ray',
        'Imaging',
        'Radiograph of chest cavity'
    ),
    (
        'Peak Flow Meter',
        'Pulmonology',
        'Measures maximum exhalation speed, used in asthma'
    ),
    (
        'ABG',
        'Pulmonology',
        'Arterial Blood Gas — oxygen and CO2 levels'
    );
-- ============================================================
-- PATIENT CASES
-- doctor_id references: 1=Cruz, 2=Marcos, 3=Lim, 4=Tan, 5=Vega
-- ============================================================
INSERT INTO patient_case (
        patient_id,
        doctor_id,
        case_code,
        chief_complaint,
        diagnosis,
        treatment_plan,
        clinical_notes,
        status,
        date_opened,
        date_closed
    )
VALUES -- Maria Reyes cases
    (
        1,
        1,
        'C-2026-031',
        'Persistent chest pain and shortness of breath',
        'Hypertensive urgency with possible angina',
        'Adjust antihypertensives, refer to cardiology, monitor ECG',
        'Patient reports intermittent chest tightness lasting 3-5 minutes, accompanied by mild dyspnea. BP elevated at 150/95 mmHg on admission.',
        'open',
        '2026-05-20',
        NULL
    ),
    (
        1,
        4,
        'C-2026-018',
        'Uncontrolled blood glucose levels',
        'Poorly controlled Type 2 Diabetes Mellitus',
        'Adjust Metformin dosage, refer to nutritionist, lifestyle counseling',
        'HbA1c at 9.2% on last check. Patient admits poor dietary compliance.',
        'closed',
        '2026-02-03',
        '2026-03-15'
    ),
    (
        1,
        1,
        'C-2025-045',
        'Annual physical examination',
        'Stable hypertension, controlled diabetes',
        'Continue current medications, repeat labs in 6 months',
        'Routine annual checkup. All vitals stable. BMI 27.4. No new complaints.',
        'closed',
        '2025-08-10',
        '2025-08-10'
    ),
    -- Jose Dela Cruz cases
    (
        2,
        2,
        'C-2026-029',
        'Productive cough and fatigue for 2 weeks',
        'COPD exacerbation, rule out pulmonary infection',
        'Bronchodilator nebulization, sputum culture, refer to pulmonology',
        'Chronic smoker presenting with productive cough, mild hemoptysis, fatigue. SpO2 94% on room air.',
        'open',
        '2026-05-15',
        NULL
    ),
    -- Liza Santos cases
    (
        3,
        1,
        'C-2026-027',
        'Recurrent asthma exacerbation',
        'Moderate persistent bronchial asthma',
        'Step up controller therapy, review trigger avoidance, pulmonology referral',
        'Third exacerbation this year. Peak flow reading at 68% predicted. Salbutamol nebulization administered in clinic.',
        'open',
        '2026-05-10',
        NULL
    ),
    -- Roberto Mendoza cases
    (
        4,
        4,
        'C-2025-058',
        'Routine hypertension follow-up',
        'Hypertension — well controlled',
        'Continue Amlodipine 5mg OD, repeat BMP in 3 months',
        'BP 128/82 mmHg on current medication. No complaints. Stable.',
        'closed',
        '2025-11-05',
        '2025-11-05'
    ),
    -- Ana Villanueva cases
    (
        5,
        1,
        'C-2026-030',
        'Fatigue and unexplained weight gain',
        'Hypothyroidism — inadequate replacement dose',
        'Increase Levothyroxine dose pending confirmatory labs, recheck TSH in 6 weeks',
        'TSH elevated at 7.8 mIU/L. Patient reports fatigue, cold intolerance, 4kg weight gain over 3 months.',
        'open',
        '2026-05-18',
        NULL
    );
-- ============================================================
-- LAB TESTS
-- case_id references the order above (1-7)
-- catalog_id references lab_test_catalog (1-12)
-- ============================================================
INSERT INTO lab_test (
        case_id,
        catalog_id,
        date_taken,
        findings,
        ordered_by
    )
VALUES -- Case 1: Maria Reyes — chest pain
    (
        1,
        9,
        '2026-05-20',
        'Sinus rhythm, no ST-segment changes. Minor T-wave inversion in V4-V5.',
        1
    ),
    (
        1,
        1,
        '2026-05-20',
        'WBC 8.2 x10³/μL, RBC 4.5 x10⁶/μL, Hgb 13.1 g/dL — within normal limits.',
        1
    ),
    -- Case 2: Maria Reyes — blood glucose
    (
        2,
        3,
        '2026-02-03',
        'HbA1c 9.2% — poorly controlled. Target <7%.',
        4
    ),
    (
        2,
        2,
        '2026-02-03',
        'Fasting blood sugar 182 mg/dL — elevated.',
        4
    ),
    -- Case 3: Maria Reyes — annual PE
    (
        3,
        8,
        '2025-08-10',
        'Normal, no proteinuria or glycosuria.',
        1
    ),
    (
        3,
        5,
        '2025-08-10',
        'Total cholesterol 214 mg/dL, LDL 138 mg/dL — borderline elevated.',
        1
    ),
    -- Case 4: Jose Dela Cruz — cough
    (
        4,
        10,
        '2026-05-15',
        'Mild hyperinflation, no infiltrates or consolidation. Consistent with early COPD.',
        2
    ),
    (
        4,
        1,
        '2026-05-15',
        'WBC 10.1 x10³/μL — slightly elevated, possible infectious component.',
        2
    ),
    -- Case 5: Liza Santos — asthma
    (
        5,
        11,
        '2026-05-10',
        '68% of predicted — moderate obstruction.',
        1
    ),
    (
        5,
        12,
        '2026-05-10',
        'pH 7.42, PaO2 88 mmHg, PaCO2 36 mmHg — mild hypoxemia.',
        1
    ),
    -- Case 6: Roberto Mendoza — hypertension follow-up
    (
        6,
        4,
        '2025-11-05',
        'Creatinine 1.0 mg/dL, K+ 4.2 mEq/L — normal renal function.',
        4
    ),
    -- Case 7: Ana Villanueva — fatigue
    (
        7,
        6,
        '2026-05-18',
        'TSH 7.8 mIU/L — elevated, consistent with hypothyroidism.',
        1
    ),
    (
        7,
        7,
        '2026-05-18',
        'Free T4 0.7 ng/dL — low-normal.',
        1
    );