import os
import re
import pyodbc
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from openai import AzureOpenAI

# --- Load environment variables ---
load_dotenv()

# --- Flask app ---
app = Flask(__name__, template_folder="templates")

# --- Azure OpenAI / Foundry setup ---
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

# Authenticate using Service Principal
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

token = credential.get_token("https://cognitiveservices.azure.com/.default")

# AzureOpenAI client
client = AzureOpenAI(
    api_key=token.token,
    azure_endpoint=ENDPOINT,
    api_version="2024-02-01"
)

# --- Azure SQL config ---
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "1433")

def get_db_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_HOST},{DB_PORT};DATABASE={DB_NAME};"
        f"UID={DB_USER};PWD={DB_PASS};Encrypt=yes;TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_str)

# --- Helper functions ---
def clean_sql(sql: str) -> str:
    """Remove markdown / code blocks"""
    sql = re.sub(r"```(?:sql)?\n?(.*?)```", r"\1", sql, flags=re.DOTALL)
    return sql.strip()

def get_db_schema() -> str:
    """Generate schema description of all tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    schema_desc = ""
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables = cursor.fetchall()
    for table_name, in tables:
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}'")
        columns = cursor.fetchall()
        cols_str = ", ".join([f"{col[0]} ({col[1]})" for col in columns])
        schema_desc += f"Table `{table_name}`: {cols_str}\n"
    conn.close()
    return schema_desc

def generate_sql(user_question: str) -> str:
    """Call Azure OpenAI to generate SQL from natural language"""
    DB_SCHEMA = get_db_schema()
    prompt = f"""
You are an expert SQL generator. Use ONLY the schema below:

{DB_SCHEMA}

Rules:
- Generate ONLY SQL
- Must run in SQL Server / Azure SQL
- Do not invent tables or columns
- Do not include Markdown
"""
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0
    )
    sql = response.choices[0].message.content
    return clean_sql(sql)

# --- Flask endpoints ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    sql = generate_sql(user_question)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return jsonify({"sql": sql, "result": result})

    except Exception as e:
        return jsonify({"error": str(e), "sql": sql}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
