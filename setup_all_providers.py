#!/usr/bin/env python3
"""
Comprehensive setup script for all AI providers
"""

import os
import sys
import subprocess
import importlib

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    packages = [
        'flask',
        'flask_cors',
        'requests',
        'chromadb',
        'transformers',
        'torch'
    ]
    
    failed_imports = []
    
    for package in packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All packages imported successfully")
    return True

def setup_providers():
    """Setup all AI providers"""
    print("\n🔧 Setting up AI Providers")
    print("=" * 50)
    
    # Test the AI provider system
    try:
        from ai_providers import ai_manager
        print("✅ AI Provider system loaded successfully")
        
        # Check which providers are available
        available_providers = []
        for provider in ai_manager.providers:
            if provider.is_available():
                available_providers.append(provider.__class__.__name__)
                print(f"  ✅ {provider.__class__.__name__} - Available")
            else:
                print(f"  ❌ {provider.__class__.__name__} - Not available")
        
        if available_providers:
            print(f"\n🎉 {len(available_providers)} provider(s) available: {', '.join(available_providers)}")
            return True
        else:
            print("\n❌ No AI providers are available")
            return False
            
    except Exception as e:
        print(f"❌ Error loading AI providers: {e}")
        return False

def test_course_generation():
    """Test course generation with available providers"""
    print("\n🧪 Testing Course Generation")
    print("=" * 40)
    
    try:
        from ai_providers import ai_manager
        
        # Test with sample content
        sample_chunks = [
            "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models.",
            "There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning.",
            "Supervised learning uses labeled training data to learn a mapping from inputs to outputs."
        ]
        
        user_prompt = "Create a basic course on machine learning fundamentals"
        
        print("🔄 Generating test course...")
        result = ai_manager.generate_course(sample_chunks, user_prompt)
        
        if result and "course" in result:
            print("✅ Course generation successful!")
            print(f"📚 Course: {result['course']}")
            print(f"📖 Modules: {len(result['modules'])}")
            return True
        else:
            print("❌ Course generation failed - invalid response")
            return False
            
    except Exception as e:
        print(f"❌ Course generation test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AI Course Creator - Complete Setup")
    print("=" * 60)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return False
    
    # Step 2: Test imports
    if not test_imports():
        print("❌ Setup failed at import testing")
        return False
    
    # Step 3: Setup providers
    if not setup_providers():
        print("❌ Setup failed at provider setup")
        return False
    
    # Step 4: Test course generation
    if not test_course_generation():
        print("❌ Setup failed at course generation test")
        return False
    
    print("\n🎉 Setup Complete!")
    print("=" * 30)
    print("✅ All requirements installed")
    print("✅ AI providers configured")
    print("✅ Course generation tested")
    
    print("\n🚀 Next Steps:")
    print("1. Start the backend: python app.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Open http://localhost:3000 in your browser")
    
    print("\n💡 Provider Setup:")
    print("- DeepSeek: python setup_deepseek.py")
    print("- Ollama: python setup_ollama.py")
    print("- Gemini: export GOOGLE_API_KEY='your-key'")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    else:
        print("\n🎉 Setup completed successfully!")
        sys.exit(0)
