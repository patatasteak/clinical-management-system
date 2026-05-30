
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
        
        # 4. Add missing columns to medicine table
        print("Adding columns to medicine table...")
        cur.execute("""
            ALTER TABLE medicine ADD COLUMN IF NOT EXISTS description TEXT
        """)
        cur.execute("""
            ALTER TABLE medicine ADD COLUMN IF NOT EXISTS form VARCHAR(100)
        """)
        cur.execute("""
            ALTER TABLE medicine ADD COLUMN IF NOT EXISTS strength VARCHAR(100)
        """)
        cur.execute("""
            ALTER TABLE medicine ADD COLUMN IF NOT EXISTS unit_price DECIMAL(10, 2)
        """)
        
        # 5. Fix "has" table med_id to medicine_id if needed
        print("Checking 'has' table columns...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'has' AND column_name = 'med_id'
        """)
        if cur.fetchone():
            print("Renaming med_id to medicine_id in has table...")
            cur.execute("""
                ALTER TABLE has RENAME COLUMN med_id TO medicine_id
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
            
        # Verify medicine columns
        print("\nMedicine columns:")
        medicine_cols = ['description', 'form', 'strength', 'unit_price']
        for col in medicine_cols:
            cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'medicine' AND column_name = '{col}'
            """)
            if cur.fetchone():
                print(f" - {col} column exists")
        
    except Exception as e:
        print(f"Error applying migration: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    apply_migration()

