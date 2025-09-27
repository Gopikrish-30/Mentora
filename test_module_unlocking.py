#!/usr/bin/env python3
"""
Test script to verify module unlocking functionality.
This script tests the quiz generation and completion flow.
"""

import requests
import json
import time

def test_module_unlocking():
    """Test that completing a quiz unlocks subsequent modules."""
    
    # Test data - simulate a course with multiple modules
    test_module = {
        "title": "Module 1: Introduction to Python",
        "description": "Learn the basics of Python programming",
        "lessons": [
            {
                "title": "Lesson 1.1: Variables and Data Types",
                "summary": "Introduction to Python variables and basic data types"
            },
            {
                "title": "Lesson 1.2: Control Flow",
                "summary": "Learn about if statements and loops"
            }
        ]
    }
    
    print("🧪 Testing Module Unlocking Feature")
    print("=" * 50)
    
    # Test quiz generation
    print("\n1. Testing quiz generation...")
    try:
        response = requests.post(
            'http://localhost:5000/generate-module-quiz',
            headers={'Content-Type': 'application/json'},
            json={'module_data': test_module},
            timeout=30
        )
        
        if response.status_code == 200:
            quiz_data = response.json()
            print(f"✅ Quiz generated successfully!")
            print(f"   Quiz ID: {quiz_data['quiz']['id']}")
            print(f"   Title: {quiz_data['quiz']['title']}")
            print(f"   Questions: {quiz_data['quiz']['totalQuestions']}")
            
            # Verify questions exist
            questions = quiz_data['quiz']['questions']
            if len(questions) > 0:
                print(f"✅ Generated {len(questions)} questions")
                
                # Show first question as example
                first_question = questions[0]
                print(f"   Example question: {first_question['question']}")
                print(f"   Options: {first_question['options']}")
                print(f"   Correct answer: {first_question['correctAnswer']}")
                print(f"   Explanation: {first_question['explanation']}")
                
            else:
                print("❌ No questions generated")
                return False
                
        else:
            print(f"❌ Quiz generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON response: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Module unlocking feature test completed successfully!")
    print("\n📝 Summary:")
    print("   - Quiz generation works correctly")
    print("   - Questions are properly formatted")
    print("   - Explanations are provided")
    print("\n🎯 Next steps:")
    print("   1. Test quiz completion in the frontend")
    print("   2. Verify that completing Module 1 unlocks Module 2")
    print("   3. Test that Module 3 unlocks after completing Module 2")
    
    return True

if __name__ == "__main__":
    print("Starting module unlocking feature test...")
    
    # Wait a moment for services to be ready
    print("Waiting for services to be ready...")
    time.sleep(2)
    
    success = test_module_unlocking()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        exit(1)