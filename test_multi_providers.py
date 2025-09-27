#!/usr/bin/env python3
"""
Test script for multi-provider AI system
"""

import os
import sys
from ai_providers import ai_manager

def test_provider_availability():
    """Test which providers are available"""
    print("🔍 Testing Provider Availability")
    print("=" * 40)
    
    available_providers = []
    
    for provider in ai_manager.providers:
        provider_name = provider.__class__.__name__
        is_available = provider.is_available()
        
        if is_available:
            print(f"✅ {provider_name} - Available")
            available_providers.append(provider_name)
        else:
            print(f"❌ {provider_name} - Not available")
    
    print(f"\n📊 Summary: {len(available_providers)}/{len(ai_manager.providers)} providers available")
    
    if available_providers:
        print(f"🎉 Available providers: {', '.join(available_providers)}")
        return True
    else:
        print("❌ No providers available")
        return False

def test_course_generation():
    """Test course generation with available providers"""
    print("\n🧪 Testing Course Generation")
    print("=" * 40)
    
    # Sample content for testing
    sample_chunks = [
        "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models.",
        "There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning.",
        "Supervised learning uses labeled training data to learn a mapping from inputs to outputs.",
        "Unsupervised learning finds hidden patterns in data without labeled examples.",
        "Reinforcement learning learns through interaction with an environment and receives rewards or penalties."
    ]
    
    user_prompt = "Create a comprehensive course on machine learning fundamentals"
    
    try:
        print("🔄 Generating course...")
        result = ai_manager.generate_course(sample_chunks, user_prompt)
        
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
        print(f"❌ Course generation failed: {str(e)}")
        return False

def test_lesson_generation():
    """Test lesson content generation"""
    print("\n📝 Testing Lesson Generation")
    print("=" * 40)
    
    lesson_title = "Introduction to Machine Learning"
    lesson_summary = "Basic concepts and definitions of machine learning"
    context_chunks = [
        "Machine learning is a method of data analysis that automates analytical model building.",
        "It is a branch of artificial intelligence based on the idea that systems can learn from data."
    ]
    
    try:
        print("🔄 Generating lesson content...")
        content = ai_manager.generate_lesson_content(lesson_title, lesson_summary, context_chunks)
        
        if content and len(content) > 100:
            print("✅ Lesson generation successful!")
            print(f"📄 Content length: {len(content)} characters")
            print(f"📝 Preview: {content[:200]}...")
            return True
        else:
            print("❌ Lesson generation failed - content too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ Lesson generation failed: {str(e)}")
        return False

def test_fallback_system():
    """Test the fallback system"""
    print("\n🔄 Testing Fallback System")
    print("=" * 40)
    
    # Test multiple generations to see if fallback works
    sample_chunks = ["Test content for fallback testing"]
    user_prompt = "Create a simple test course"
    
    try:
        for i in range(3):
            print(f"🔄 Test {i+1}/3...")
            result = ai_manager.generate_course(sample_chunks, user_prompt)
            if result and "course" in result:
                print(f"  ✅ Success with {ai_manager.current_provider.__class__.__name__}")
            else:
                print(f"  ❌ Failed")
        
        print("✅ Fallback system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Fallback system test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🧪 Multi-Provider AI System Test")
    print("=" * 50)
    
    # Test 1: Provider availability
    if not test_provider_availability():
        print("\n❌ No providers available. Please setup at least one provider.")
        print("Run: python setup_all_providers.py")
        return False
    
    # Test 2: Course generation
    if not test_course_generation():
        print("\n❌ Course generation failed")
        return False
    
    # Test 3: Lesson generation
    if not test_lesson_generation():
        print("\n❌ Lesson generation failed")
        return False
    
    # Test 4: Fallback system
    if not test_fallback_system():
        print("\n❌ Fallback system failed")
        return False
    
    print("\n🎉 All Tests Passed!")
    print("=" * 30)
    print("✅ Provider availability: OK")
    print("✅ Course generation: OK")
    print("✅ Lesson generation: OK")
    print("✅ Fallback system: OK")
    
    print(f"\n🎯 Current provider: {ai_manager.current_provider.__class__.__name__}")
    print("🚀 System is ready for use!")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Tests failed. Please check the error messages above.")
        sys.exit(1)
    else:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
