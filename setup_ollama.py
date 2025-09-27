#!/usr/bin/env python3
"""
Setup script for Ollama (local AI models)
"""

import os
import subprocess
import requests
import json
import platform

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama():
    """Install Ollama based on the operating system"""
    system = platform.system().lower()
    
    print(f"🔧 Installing Ollama for {system}...")
    
    if system == "windows":
        print("📥 Download Ollama for Windows from: https://ollama.ai/download")
        print("Run the installer and restart your terminal.")
        return False
    elif system == "darwin":  # macOS
        try:
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ Homebrew not found. Please install Homebrew first or download from https://ollama.ai/download")
            return False
    elif system == "linux":
        try:
            subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh'], check=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Ollama. Please visit https://ollama.ai/download")
            return False
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False

def start_ollama():
    """Start Ollama service"""
    try:
        # Try to start Ollama in background
        if platform.system().lower() == "windows":
            subprocess.Popen(['ollama', 'serve'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait a moment for service to start
        import time
        time.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")
        return False

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def download_model(model_name="llama2"):
    """Download a model for Ollama"""
    print(f"📥 Downloading {model_name} model (this may take a while)...")
    
    try:
        result = subprocess.run(['ollama', 'pull', model_name], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully downloaded {model_name}")
            return True
        else:
            print(f"❌ Failed to download {model_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def test_ollama():
    """Test Ollama with a simple request"""
    try:
        data = {
            "model": "llama2",
            "prompt": "Hello, this is a test.",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama is working correctly!")
            print(f"Test response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ Ollama test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

def setup_ollama():
    """Main setup function for Ollama"""
    print("🔧 Setting up Ollama (Local AI)")
    print("=" * 40)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("📦 Ollama not found. Installing...")
        if not install_ollama():
            print("❌ Failed to install Ollama. Please install manually from https://ollama.ai/download")
            return False
    else:
        print("✅ Ollama is already installed")
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("🚀 Starting Ollama service...")
        if not start_ollama():
            print("❌ Failed to start Ollama service")
            return False
    else:
        print("✅ Ollama service is running")
    
    # Download a model if needed
    print("📥 Checking for available models...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if not models:
                print("📥 No models found. Downloading llama2...")
                if not download_model("llama2"):
                    print("❌ Failed to download model")
                    return False
            else:
                print(f"✅ Found {len(models)} models: {[m['name'] for m in models]}")
    except:
        print("❌ Failed to check models")
        return False
    
    # Test Ollama
    print("🧪 Testing Ollama...")
    if test_ollama():
        print("✅ Ollama setup complete!")
        return True
    else:
        print("❌ Ollama test failed")
        return False

if __name__ == "__main__":
    print("🚀 Ollama Setup (Local AI Models)")
    print("=" * 50)
    
    print("💡 Ollama allows you to run AI models locally without API limits!")
    print("📋 Benefits:")
    print("  - No API quotas or rate limits")
    print("  - Complete privacy (data stays local)")
    print("  - Free to use")
    print("  - Works offline")
    
    success = setup_ollama()
    
    if success:
        print("\n🎉 Ollama setup complete!")
        print("Ollama will be used as a fallback AI provider.")
        print("\n📚 Available models:")
        print("  - llama2 (default)")
        print("  - codellama (for code)")
        print("  - mistral (alternative)")
        print("\nTo download more models: ollama pull <model-name>")
    else:
        print("\n❌ Ollama setup failed.")
        print("The system will use other available providers.")
    
    print("\n🔧 Manual setup:")
    print("1. Install Ollama: https://ollama.ai/download")
    print("2. Start service: ollama serve")
    print("3. Download model: ollama pull llama2")
