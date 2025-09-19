from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Simple in-memory data store
todos = [
    {"id": 1, "task": "Learn AWS Lambda", "completed": False},
    {"id": 2, "task": "Deploy Flask app", "completed": False}
]

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Simple Flask API!",
        "version": "1.0.0",
        "endpoints": [
            "GET /",
            "GET /todos",
            "POST /todos",
            "PUT /todos/<id>",
            "DELETE /todos/<id>"
        ]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "flask-api"})

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify({"todos": todos})

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Task is required"}), 400
    
    new_todo = {
        "id": len(todos) + 1,
        "task": data['task'],
        "completed": data.get('completed', False)
    }
    todos.append(new_todo)
    return jsonify({"todo": new_todo}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    if 'task' in data:
        todo['task'] = data['task']
    if 'completed' in data:
        todo['completed'] = data['completed']
    
    return jsonify({"todo": todo})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({"message": "Todo deleted "})

# Lambda handler function
def lambda_handler(event, context):
    try:
        from serverless_wsgi import handle_request
        return handle_request(app, event, context)
    except ImportError:
        # Fallback for local testing
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'serverless_wsgi not available'})
        }

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=8000)