import os
import psycopg2


def get_connection():
    """Return a new psycopg2 connection using environment variables.

    Environment variables:
      DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
    """
    host = os.environ.get("DB_HOST", "localhost")
    dbname = os.environ.get("DB_NAME", "postgres")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "1234")
    port = int(os.environ.get("DB_PORT", 5432))

    return psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)