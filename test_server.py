#!/usr/bin/env python3
"""
Test script to debug Flask server startup
"""
import os
import sys

print("Checking environment variables...")
if 'GROQ_API_KEY' not in os.environ:
    print("Error: GROQ_API_KEY environment variable not set")
    print("Please set it in your .env file or environment variables")
    sys.exit(1)

print("Testing imports...")
try:
    from ai_providers import ai_manager
    print("✅ AI Manager imported successfully")
except Exception as e:
    print(f"❌ AI Manager import failed: {e}")
    sys.exit(1)

try:
    from app import app
    print("✅ Flask app imported successfully")
except Exception as e:
    print(f"❌ Flask app import failed: {e}")
    sys.exit(1)

print("Testing Flask app...")
try:
    with app.test_client() as client:
        response = client.get('/')
        print(f"✅ Flask app test successful: {response.status_code}")
except Exception as e:
    print(f"❌ Flask app test failed: {e}")

print("Starting Flask server...")
try:
    app.run(host='127.0.0.1', port=5000, debug=False)
except Exception as e:
    print(f"❌ Flask server failed to start: {e}")
    import traceback
    traceback.print_exc()
