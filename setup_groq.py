#!/usr/bin/env python3
"""
Setup script for Groq AI provider
"""

import os
import sys

def setup_groq():
    """Setup Groq API key"""
    print("🚀 Setting up Groq AI Provider")
    print("=" * 40)
    
    print("\n📝 Groq Setup Instructions:")
    print("1. Go to https://console.groq.com/")
    print("2. Sign up or log in to your account")
    print("3. Navigate to API Keys section")
    print("4. Create a new API key")
    print("5. Copy the API key")
    
    print("\n🔑 Enter your Groq API Key:")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return False
    
    # Set environment variable
    os.environ["GROQ_API_KEY"] = api_key
    
    # Test the API key
    print("\n🧪 Testing Groq API connection...")
    try:
        from ai_providers import GroqProvider
        
        provider = GroqProvider()
        if provider.is_available():
            print("✅ Groq API key is valid!")
            
            # Test a simple request
            try:
                test_messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Hello from Groq!'"}
                ]
                
                response = provider._make_request(test_messages, max_tokens=50)
                print(f"✅ Test response: {response}")
                
                # Save API key to environment file
                save_api_key_to_file(api_key)
                
                print("\n🎉 Groq setup completed successfully!")
                print("✅ API key is working")
                print("✅ Provider is ready to use")
                
                return True
                
            except Exception as e:
                print(f"❌ API test failed: {e}")
                return False
        else:
            print("❌ Groq provider is not available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Groq: {e}")
        return False

def save_api_key_to_file(api_key):
    """Save API key to a .env file"""
    env_file = ".env"
    
    # Read existing .env file if it exists
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    
    # Update or add GROQ_API_KEY
    env_vars["GROQ_API_KEY"] = api_key
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.write("# AI Provider API Keys\n")
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ API key saved to {env_file}")

def load_env_file():
    """Load environment variables from .env file"""
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def main():
    """Main setup function"""
    # Load existing environment variables
    load_env_file()
    
    # Check if API key is already set
    if os.environ.get("GROQ_API_KEY"):
        print("🔑 Groq API key already configured!")
        print("🧪 Testing existing API key...")
        
        try:
            from ai_providers import GroqProvider
            provider = GroqProvider()
            
            if provider.is_available():
                print("✅ Existing Groq API key is working!")
                return True
            else:
                print("❌ Existing API key is not working. Please reconfigure.")
        except Exception as e:
            print(f"❌ Error testing existing API key: {e}")
    
    # Setup new API key
    return setup_groq()

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Groq setup failed. Please check the error messages above.")
        sys.exit(1)
    else:
        print("\n🎉 Groq setup completed successfully!")
        print("\n🚀 Next Steps:")
        print("1. Start the backend: python app.py")
        print("2. Groq will be used as the primary AI provider")
        sys.exit(0)
