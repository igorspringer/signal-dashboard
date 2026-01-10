from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            value REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/signals", methods=["GET"])
def get_signals():
    try:
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM data ORDER BY id DESC LIMIT 50"
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/signals", methods=["POST"])
def add_signal():
    data = request.json or {}

    title = str(data.get("title", "")).strip()
    value = data.get("value")

    if not title or not isinstance(value, (int, float)):
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO data (title, value, created_at) VALUES (?, ?, ?)",
        (title, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
