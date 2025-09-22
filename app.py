from flask import Flask, request, jsonify
import serverless_wsgi

app = Flask(__name__)

# In-memory store
todos = [
    {"id": 1, "task": "Learn AWS Lambda", "completed": False},
    {"id": 2, "task": "Deploy Flask app", "completed": False},
    {"id":3,"task":"testing deployment","completed":False}
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Simple Flask API!, deployment check",
        "version": "1.0.0",
        "endpoints": [
            "GET /",
            "GET /todos",
            "POST /todos",
            "PUT /todos/<id>",
            "DELETE /todos/<id>"
        ]
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "flask-api"})

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify({"todos": todos})

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Task is required"}), 400
    
    new_todo = {
        "id": len(todos) + 1,
        "task": data["task"],
        "completed": data.get("completed", False)
    }
    todos.append(new_todo)
    return jsonify({"todo": new_todo}), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    if "task" in data:
        todo["task"] = data["task"]
    if "completed" in data:
        todo["completed"] = data["completed"]
    
    return jsonify({"todo": todo})

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    original_length = len(todos)
    todos = [t for t in todos if t["id"] != todo_id]
    
    if len(todos) == original_length:
        return jsonify({"error": "Todo not found"}), 404
    
    return jsonify({"message": "Todo deleted"})

# ✅ Lambda entry point (serverless-wsgi handles event -> Flask)
def lambda_handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

# Local run (normal Flask server)
if __name__ == "__main__":
    app.run(debug=True)
