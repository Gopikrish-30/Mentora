#!/usr/bin/env python3
"""
Test script to verify Gemini API integration
"""

import os
import sys
from llm_processor import generate_course_from_text

def test_gemini_api():
    """Test the Gemini API with a simple course generation"""
    
    # Check if API key is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        print("Please set it with: export GOOGLE_API_KEY='your-api-key'")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test with sample content
    sample_chunks = [
        "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models.",
        "There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning.",
        "Supervised learning uses labeled training data to learn a mapping from inputs to outputs.",
        "Unsupervised learning finds hidden patterns in data without labeled examples.",
        "Reinforcement learning learns through interaction with an environment and receives rewards or penalties."
    ]
    
    user_prompt = "Create a comprehensive course on machine learning fundamentals"
    
    try:
        print("🔄 Generating course content...")
        result = generate_course_from_text(sample_chunks, user_prompt)
        
        if result and "course" in result:
            print("✅ Course generation successful!")
            print(f"📚 Course Title: {result['course']}")
            print(f"📖 Number of modules: {len(result['modules'])}")
            
            for i, module in enumerate(result['modules']):
                print(f"  Module {i+1}: {module['title']}")
                print(f"    Lessons: {len(module['lessons'])}")
                for j, lesson in enumerate(module['lessons']):
                    print(f"      {j+1}. {lesson['title']}")
                    print(f"         Summary: {lesson['summary'][:100]}...")
                    print(f"         Detail length: {len(lesson['detail'])} characters")
            
            return True
        else:
            print("❌ Course generation failed - invalid response format")
            return False
            
    except Exception as e:
        print(f"❌ Error during course generation: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini API Integration")
    print("=" * 50)
    
    success = test_gemini_api()
    
    if success:
        print("\n🎉 All tests passed! Gemini API is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Tests failed. Please check your API key and configuration.")
        sys.exit(1)
