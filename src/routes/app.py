import os
import re
import pyodbc
from flask import Flask, Blueprint, request, jsonify, render_template
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from openai import AzureOpenAI

from src.services.rag.rag_engine import RagEngine

# --- Load environment variables ---
load_dotenv()

# --- Flask app ---
app = Blueprint("main", __name__)

# --- Flask endpoints ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    rag_engine = RagEngine()
    sql = rag_engine.get_query(user_question)

    try:
        # conn = get_db_connection()
        # cursor = conn.cursor()
        # cursor.execute(sql)
        # rows = cursor.fetchall()
        # columns = [column[0] for column in cursor.description]
        # result = [dict(zip(columns, row)) for row in rows]
        # conn.close()
        result = []
        return jsonify({"sql": sql, "result": result})

    except Exception as e:
        return jsonify({"error": str(e), "sql": sql}), 400