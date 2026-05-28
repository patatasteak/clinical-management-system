-- ============================================================
-- CLINIC MANAGEMENT SYSTEM — SEED DATA
-- Run schema.sql first before this file
-- ============================================================

-- ============================================================
-- MEDICINES
-- ============================================================
INSERT INTO Medicine (med_id, medicinename, medicine_type, description)
VALUES 
    ('00000001', 'Paracetamol (Acetaminophen)', 'Analgesic (Pain reliever) and Antipyretic (Fever reducer)', 'Used to treat mild-to-moderate pain (like headaches or muscle aches) and to reduce fever. It is gentle on the stomach compared to other pain relievers.'),
    ('00000002', 'Ibuprofen', 'NSAID (Non-Steroidal Anti-Inflammatory Drug)', 'Relieves pain, reduces fever, and targets inflammation. Commonly used for arthritis, menstrual cramps, toothaches, and backaches.'),
    ('00000003', 'Cetirizine', 'Antihistamine (Second-generation)', 'Provides 24-hour relief from allergy symptoms like sneezing, runny nose, itchy eyes, and hives without causing significant drowsiness.'),
    ('00000004', 'Loratadine', 'Antihistamine (Non-drowsy)', 'Another effective daily allergy medication that treats hay fever and skin allergies without causing sleepiness.'),
    ('00000005', 'Omeprazole', 'Proton Pump Inhibitor (PPI)', 'Reduces the amount of acid produced in the stomach. Used to treat heartburn, acid reflux, and GERD.'),
    ('00000006', 'Ranitidine / Famotidine', 'H2 Blocker (Antacid)', 'Quickly relieves and prevents heartburn and acid indigestion by blocking histamine receptors in the stomach.'),
    ('00000007', 'Loperamide', 'Anti-diarrheal', 'Slows down gut movement to help control and relieve sudden, short-term diarrhea.'),
    ('00000008', 'Oral Rehydration Salts (ORS)', 'Electrolyte Replenisher', 'A balanced mixture of glucose and salts used to prevent or treat dehydration caused by severe diarrhea or vomiting.'),
    ('00000009', 'Metoclopramide', 'Antiemetic (Anti-nausea)', 'Used to treat and prevent nausea and vomiting, often associated with migraines, surgery, or chemotherapy.'),
    ('00000010', 'Amoxicillin', 'Antibiotic (Penicillin class)', 'A broad-spectrum antibiotic used to treat a wide variety of bacterial infections, such as middle ear infections, strep throat, and pneumonia. (Requires a prescription).'),
    ('00000011', 'Azithromycin', 'Antibiotic (Macrolide class)', 'A commonly prescribed antibiotic used for respiratory infections, skin infections, and certain sexually transmitted infections. (Requires a prescription).'),
    ('00000012', 'Metformin', 'Antidiabetic (Biguanide)', 'The first-line medication for the treatment of type 2 diabetes, helping to lower blood sugar levels and improve insulin sensitivity. (Requires a prescription).'),
    ('00000013', 'Amlodipine', 'Calcium Channel Blocker (Antihypertensive)', 'Relaxes blood vessels to lower high blood pressure and prevent chest pain (angina). (Requires a prescription).'),
    ('00000014', 'Atorvastatin', 'Statin (Cholesterol-lowering drug)', 'Lowers "bad" cholesterol (LDL) and triglycerides while raising "good" cholesterol (HDL) to reduce the risk of heart disease and stroke. (Requires a prescription).'),
    ('00000015', 'Salbutamol (Albuterol)', 'Bronchodilator (Beta-2 agonist)', 'A rescue inhaler used to quickly open up the airways during asthma attacks or for chronic obstructive pulmonary disease (COPD). (Requires a prescription).'),
    ('00000016', 'Hydrocortisone Cream', 'Topical Corticosteroid', 'A mild steroid cream used applied to the skin to reduce swelling, itching, and redness caused by eczema, insect bites, or rashes.'),
    ('00000017', 'Clotrimazole', 'Topical Antifungal', 'Used to treat fungal skin infections such as athlete''s foot, jock itch, ringworm, and vaginal yeast infections.'),
    ('00000018', 'Dextromethorphan', 'Antitussive (Cough suppressant)', 'Used to provide temporary relief from a dry, hacking cough by affecting the signals in the brain that trigger the cough reflex.'),
    ('00000019', 'Guaifenesin', 'Expectorant', 'Thins and loosens mucus in the chest and airways, making it easier to cough up phlegm during a wet cough.'),
    ('00000020', 'Aspirin (Low-Dose)', 'Antiplatelet / NSAID', 'In low doses, it acts as a blood thinner to help prevent blood clots, reducing the risk of a heart attack or stroke in high-risk individuals. (Should be taken under medical supervision).');

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
        '123 Mango Ave, Cebu City',
        '0917-234-5678',
        'A+',
        'maria.reyes@email.com',
        '1986-03-14',
        '0917-987-6543',
        'password123'
    ),
    (
        'Jose',
        'Dela Cruz',
        'Filipino',
        'male',
        '45 Osmena Blvd, Cebu City',
        '0928-765-4321',
        'O+',
        'jdelacruz@email.com',
        '1972-06-08',
        '0928-111-2222',
        'password123'
    );

-- ============================================================
-- CLINICAL BACKGROUND
-- ============================================================
INSERT INTO clinical_background (patient_id, smoking_status, alcohol_use)
VALUES (0, 'non-smoker', 'occasional'),
    (1, 'active smoker', 'non-drinker');

-- ============================================================
-- VITAL STATS (My Stats)
-- ============================================================
INSERT INTO vitalStats (recorded_at, weight, height, patient_id)
VALUES 
    ('2005-04-15 10:00:00', 45.0, 150.0, 0),
    ('2010-05-20 14:30:00', 55.5, 165.0, 0),
    ('2026-05-28 09:00:00', 60.2, 165.0, 0);

-- ============================================================
-- CASES
-- ============================================================
INSERT INTO patient_case (chief_Complaint, description, patient_id, doctor_id, appoint_status)
VALUES (
        'Persistent chest pain',
        'Intermittent chest tightness lasting 3-5 minutes',
        0,
        1,
        'Ongoing'
    ),
    (
        'Annual physical examination',
        'Routine annual checkup',
        0,
        4,
        'Closed'
    );

-- ============================================================
-- LAB TEST CATALOG
-- ============================================================
INSERT INTO LabTestCatalog (catalog_id, test_name, description, price)
VALUES 
    ('LT0001', 'Complete Blood Count (CBC)', 'A routine blood test used to evaluate your overall health.', 280.00),
    ('LT0002', 'Urinalysis', 'Analysis of urine used to detect track tract infections.', 110.00),
    ('LT0003', 'Fecalysis', 'A stool test used to check for parasites.', 100.00);
