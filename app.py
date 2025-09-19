import json
import os
import sys

# Simple in-memory data store
todos = [
    {"id": 1, "task": "Learn AWS Lambda", "completed": False},
    {"id": 2, "task": "Deploy Flask app", "completed": False}
]

def lambda_handler(event, context):
    """
    AWS Lambda handler function for API Gateway events
    """
    global todos  # Declare global at the beginning of the function
    
    try:
        # Get HTTP method and path
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Parse request body if present
        body = {}
        if event.get('body'):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
        
        # Route handling
        if path == '/' and http_method == 'GET':
            response_body = {
                "message": "Welcome to Simple Flask API!",
                "version": "1.0.0",
                "endpoints": [
                    "GET /",
                    "GET /todos", 
                    "POST /todos",
                    "PUT /todos/<id>",
                    "DELETE /todos/<id>"
                ]
            }
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response_body)
            }
            
        elif path == '/health' and http_method == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"status": "healthy", "service": "flask-api"})
            }
            
        elif path == '/todos' and http_method == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"todos": todos})
            }
            
        elif path == '/todos' and http_method == 'POST':
            if not body or 'task' not in body:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Task is required"})
                }
            
            new_todo = {
                "id": len(todos) + 1,
                "task": body['task'],
                "completed": body.get('completed', False)
            }
            todos.append(new_todo)
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"todo": new_todo})
            }
            
        elif path.startswith('/todos/') and http_method == 'PUT':
            # Extract todo ID from path
            try:
                todo_id = int(path.split('/')[-1])
            except ValueError:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Invalid todo ID"})
                }
            
            todo = next((t for t in todos if t['id'] == todo_id), None)
            if not todo:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Todo not found"})
                }
            
            if 'task' in body:
                todo['task'] = body['task']
            if 'completed' in body:
                todo['completed'] = body['completed']
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"todo": todo})
            }
            
        elif path.startswith('/todos/') and http_method == 'DELETE':
            # Extract todo ID from path
            try:
                todo_id = int(path.split('/')[-1])
            except ValueError:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Invalid todo ID"})
                }
            
            # Remove the duplicate global declaration that was causing the error
            original_length = len(todos)
            todos = [t for t in todos if t['id'] != todo_id]
            
            if len(todos) == original_length:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Todo not found"})
                }
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"message": "Todo deleted"})
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "Not found"})
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Internal server error"})
        }

# For local testing
if __name__ == '__main__':
    # Test event
    test_event = {
        'httpMethod': 'GET',
        'path': '/',
        'body': None
    }
    test_context = {}
    
    result = lambda_handler(test_event, test_context)
    print(json.dumps(result, indent=2))