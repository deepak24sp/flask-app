#!/usr/bin/env python3
"""
Simple test script to verify your Flask app works locally
Run: python test_local.py
"""

import requests
import json
import time
import subprocess
import signal
import sys
from multiprocessing import Process

def start_flask_app():
    """Start Flask app in background"""
    import app
    app.app.run(host='0.0.0.0', port=8000, debug=False)

def test_api():
    """Test all API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Flask API locally...\n")
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        # Test 1: Home endpoint
        print("1️⃣ Testing GET /")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()['message']}")
        assert response.status_code == 200
        print("   ✅ PASS\n")
        
        # Test 2: Health check
        print("2️⃣ Testing GET /health")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ PASS\n")
        
        # Test 3: Get todos
        print("3️⃣ Testing GET /todos")
        response = requests.get(f"{base_url}/todos")
        print(f"   Status: {response.status_code}")
        todos = response.json()['todos']
        print(f"   Found {len(todos)} todos")
        assert response.status_code == 200
        print("   ✅ PASS\n")
        
        # Test 4: Add new todo
        print("4️⃣ Testing POST /todos")
        new_todo = {"task": "Test API deployment", "completed": False}
        response = requests.post(f"{base_url}/todos", json=new_todo)
        print(f"   Status: {response.status_code}")
        created_todo = response.json()['todo']
        print(f"   Created: {created_todo['task']}")
        assert response.status_code == 201
        print("   ✅ PASS\n")
        
        # Test 5: Update todo
        print("5️⃣ Testing PUT /todos/1")
        update_data = {"task": "Learn AWS Lambda - Updated!", "completed": True}
        response = requests.put(f"{base_url}/todos/1", json=update_data)
        print(f"   Status: {response.status_code}")
        updated_todo = response.json()['todo']
        print(f"   Updated: {updated_todo['task']}")
        print(f"   Completed: {updated_todo['completed']}")
        assert response.status_code == 200
        print("   ✅ PASS\n")
        
        # Test 6: Delete todo
        print("6️⃣ Testing DELETE /todos/2")
        response = requests.delete(f"{base_url}/todos/2")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()['message']}")
        assert response.status_code == 200
        print("   ✅ PASS\n")
        
        print("🎉 All tests passed! Your Flask app is working correctly.")
        print("\n📋 Summary:")
        print("   ✅ Home endpoint working")
        print("   ✅ Health check working")
        print("   ✅ GET todos working")
        print("   ✅ POST todos working")
        print("   ✅ PUT todos working")
        print("   ✅ DELETE todos working")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def main():
    print("🚀 Starting Flask app for testing...")
    
    # Start Flask app in background process
    flask_process = Process(target=start_flask_app)
    flask_process.start()
    
    try:
        # Run tests
        success = test_api()
        
        if success:
            print("\n✅ Ready for deployment!")
            print("\n🚀 Next steps:")
            print("   1. Run ./setup.sh to create AWS infrastructure")
            print("   2. Set up GitHub secrets")
            print("   3. Push to main branch")
        else:
            print("\n❌ Tests failed. Fix issues before deploying.")
            
    finally:
        # Cleanup: terminate Flask process
        flask_process.terminate()
        flask_process.join()
        print("\n🛑 Test server stopped.")

if __name__ == "__main__":
    main()