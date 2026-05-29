from database import get_connection

def apply_migration():
    print("Applying migration...")
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # 1. Add password_hash column to doctor table
        print("Adding password_hash column...")
        cur.execute("""
            ALTER TABLE doctor ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)
        """)
        
        # 2. Create doctor_id_seq sequence if not exists and set default
        print("Creating/updating doctor_id_seq...")
        cur.execute("""
            CREATE SEQUENCE IF NOT EXISTS doctor_id_seq START 100000
        """)
        
        cur.execute("""
            ALTER TABLE doctor ALTER COLUMN doctor_id SET DEFAULT nextval('doctor_id_seq')
        """)
        
        # 3. Add feedback column to patient_case table
        print("Adding feedback column to patient_case...")
        cur.execute("""
            ALTER TABLE patient_case ADD COLUMN IF NOT EXISTS feedback TEXT
        """)
        
        conn.commit()
        print("Migration applied successfully!")
        
        # Verify columns exist
        print("\nVerifying columns exist:")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'doctor' AND column_name = 'password_hash'
        """)
        if cur.fetchone():
            print(" - password_hash column exists")
        
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'patient_case' AND column_name = 'feedback'
        """)
        if cur.fetchone():
            print(" - feedback column exists")
        
    except Exception as e:
        print(f"Error applying migration: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    apply_migration()
