import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url, sslmode="require")

    # fallback to individual vars for local dev
    host = os.environ.get("DB_HOST", "localhost")
    dbname = os.environ.get("DB_NAME", "postgres")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "1234")
    port = int(os.environ.get("DB_PORT", 5432))

    return psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)