import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "1433")

def get_db_connection(db_name, db_user, db_password, db_host, db_port):
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={db_host},{db_port};DATABASE={db_name};"
        f"UID={db_user};PWD={db_password};Encrypt=yes;TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_str)

class DatabaseService:

    def execute_query(self, query):
        conn = get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return result