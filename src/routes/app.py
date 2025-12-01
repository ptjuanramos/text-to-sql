import re

from flask import Blueprint, request, jsonify, render_template
from dotenv import load_dotenv

from src.services.database.database_service import DatabaseService
from src.services.rag.rag_engine import RagEngine

# --- Load environment variables ---
load_dotenv()

# --- Flask app ---
app = Blueprint("main", __name__)

# --- Flask endpoints ---
@app.route("/")
def home():
    return render_template("index.html")

def clean_sql(sql: str) -> str:
    """Remove markdown / code blocks"""
    sql = re.sub(r"```(?:sql)?\n?(.*?)```", r"\1", sql, flags=re.DOTALL)
    return sql.strip()

@app.route("/query", methods=["POST"])
def query():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    rag_engine = RagEngine()
    query = rag_engine.get_query(user_question)

    try:
        database_service = DatabaseService()
        result = database_service.execute_query(query)
        return jsonify({"sql": query, "result": result})

    except Exception as e:
        return jsonify({"error": str(e), "sql": query}), 400