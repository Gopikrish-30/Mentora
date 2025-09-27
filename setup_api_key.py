#!/usr/bin/env python3
"""
Setup script to configure the Gemini API key
"""

import os
import sys

def setup_api_key():
    """Setup the Gemini API key"""
    
    api_key = "AIzaSyDuyFkAkIZtYvxZddZ560m9QIuqSp6FocY"
    
    # Set the environment variable for the current session
    os.environ["GOOGLE_API_KEY"] = api_key
    
    print("✅ Gemini API key configured successfully!")
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # Test the setup
    try:
        from llm_processor import model
        print("✅ Gemini model initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing Gemini model: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up Gemini API Key")
    print("=" * 40)
    
    success = setup_api_key()
    
    if success:
        print("\n🎉 Setup complete! You can now run the application.")
        print("\nTo make this permanent, add this to your shell profile:")
        print("export GOOGLE_API_KEY='AIzaSyDuyFkAkIZtYvxZddZ560m9QIuqSp6FocY'")
    else:
        print("\n💥 Setup failed. Please check the error messages above.")
        sys.exit(1)
