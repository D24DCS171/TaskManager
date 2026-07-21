from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__)
CORS(app)

# -----------------------------
# MySQL Connection (Retry Logic)
# -----------------------------
db = None

for i in range(10):
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="Drashti@0406",
            database="taskdb"
        )
        print("✅ Connected to MySQL!")
        break
    except Exception as e:
        print(f"❌ MySQL not ready... Retrying ({i+1}/10)")
        time.sleep(5)

if db is None:
    raise Exception("Could not connect to MySQL")

cursor = db.cursor(dictionary=True)

# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return "Welcome to Task Manager API (MySQL + Docker)"

# -----------------------------
# GET All Tasks
# -----------------------------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return jsonify(tasks)

# -----------------------------
# Add Task
# -----------------------------
@app.route("/tasks", methods=["POST"])
def add_task():

    data = request.get_json()

    sql = "INSERT INTO tasks(title, status) VALUES(%s,%s)"
    values = (
        data["title"],
        "Pending"
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({
        "message": "Task Added Successfully"
    }), 201

# -----------------------------
# Update Task
# -----------------------------
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    data = request.get_json()

    sql = """
    UPDATE tasks
    SET title=%s, status=%s
    WHERE id=%s
    """

    values = (
        data["title"],
        data["status"],
        id
    )

    cursor.execute(sql, values)
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({
            "message": "Task Not Found"
        }), 404

    return jsonify({
        "message": "Task Updated Successfully"
    })

# -----------------------------
# Delete Task
# -----------------------------
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        return jsonify({
            "message": "Task Not Found"
        }), 404

    return jsonify({
        "message": "Task Deleted Successfully"
    })

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)