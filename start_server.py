#!/usr/bin/env python3
"""
Simple script to start the Flask server with proper environment setup
"""
import os
import sys

# Check if GROQ_API_KEY is set in environment
if 'GROQ_API_KEY' not in os.environ:
    print("Error: GROQ_API_KEY environment variable not set")
    print("Please set it in your .env file or environment variables")
    sys.exit(1)

print("Environment variables set:")
print(f"GROQ_API_KEY: {os.environ.get('GROQ_API_KEY', 'NOT SET')}")

try:
    print("Importing Flask app...")
    from app import app
    print("Flask app imported successfully!")
    
    print("Starting Flask server on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    
    # Start the server
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=False  # Disable reloader to avoid issues
    )
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
