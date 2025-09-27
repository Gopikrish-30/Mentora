#!/usr/bin/env python3
"""
Setup script for DeepSeek API
"""

import os
import requests
import json

def setup_deepseek():
    """Setup DeepSeek API"""
    
    print("🔧 Setting up DeepSeek API")
    print("=" * 40)
    
    # DeepSeek API key (you can get this from https://platform.deepseek.com/)
    api_key = input("Enter your DeepSeek API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  Skipping DeepSeek setup. You can set it later with:")
        print("export DEEPSEEK_API_KEY='your-api-key'")
        return False
    
    # Set environment variable
    os.environ["DEEPSEEK_API_KEY"] = api_key
    
    # Test the API
    print("🧪 Testing DeepSeek API...")
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": "Hello, this is a test message."}
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ DeepSeek API is working correctly!")
            print(f"🔑 API Key: {api_key[:10]}...")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing DeepSeek API: {str(e)}")
        return False

def get_deepseek_api_key():
    """Instructions for getting DeepSeek API key"""
    print("\n📋 How to get DeepSeek API Key:")
    print("1. Visit: https://platform.deepseek.com/")
    print("2. Sign up for an account")
    print("3. Go to API section")
    print("4. Create a new API key")
    print("5. Copy the key and use it in this setup")
    print("\n💡 DeepSeek offers generous free tier with good performance!")

if __name__ == "__main__":
    print("🚀 DeepSeek API Setup")
    print("=" * 50)
    
    get_deepseek_api_key()
    
    success = setup_deepseek()
    
    if success:
        print("\n🎉 DeepSeek setup complete!")
        print("DeepSeek will be used as the primary AI provider.")
    else:
        print("\n⚠️  DeepSeek setup incomplete.")
        print("The system will fall back to other available providers.")
    
    print("\nTo make this permanent, add to your shell profile:")
    print("export DEEPSEEK_API_KEY='your-api-key'")
