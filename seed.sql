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
-- DISABILITIES
-- ============================================================
INSERT INTO disability (
        clinical_id,
        description,
        congenital,
        notes
    )
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
        clinical_id,
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
-- MEDICINES
-- updated for new schema
-- ============================================================
INSERT INTO medicine (medicine_name, medicine_type)
VALUES ('Metformin', 'Anti-diabetic'),
    ('Amlodipine', 'Antihypertensive'),
    ('Salbutamol', 'Bronchodilator'),
    (
        'Levothyroxine',
        'Hormone Replacement'
    ),
    ('Atorvastatin', 'Statin');
-- ============================================================
-- PRESCRIPTIONS
-- ============================================================
INSERT INTO prescription (
        case_id,
        prescribed_by,
        instructions,
        notes
    )
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
INSERT INTO "has" (
        prescription_id,
        medicine_id,
        quantity,
        dosage,
        frequency
    )
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