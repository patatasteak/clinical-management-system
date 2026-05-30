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