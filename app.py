from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table
conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT,
    class TEXT,
    section TEXT
)
""")
conn.commit()
conn.close()

# ---------- ROUTES ----------
@app.route("/")
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    roll = request.form["roll"]
    name = request.form["name"]
    clas = request.form["class"]
    section = request.form["section"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO students (roll, name, class, section) VALUES (?, ?, ?, ?)",
        (roll, name, clas, section),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:roll>")
def delete(roll):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE roll = ?", (roll,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
