import requests
import json

# Test data for quiz generation
test_module = {
    "title": "Introduction to Python Programming",
    "description": "Learn the basics of Python programming including variables, data types, and control structures",
    "lessons": [
        {
            "title": "Variables and Data Types",
            "summary": "In Python, variables are used to store data values. Python has several data types including integers, floats, strings, and booleans. Variables are created when you assign a value to them. For example: x = 5 creates an integer variable. Strings are text values enclosed in quotes. Booleans can be True or False."
        },
        {
            "title": "Control Structures",
            "summary": "Python uses if statements for conditional execution. The if statement checks a condition and executes code if the condition is true. Loops are used to repeat code. The for loop iterates over a sequence, while the while loop repeats as long as a condition is true. Break and continue statements control loop execution."
        },
        {
            "title": "Functions and Modules",
            "summary": "Functions are reusable blocks of code that perform specific tasks. You define a function using the def keyword. Functions can accept parameters and return values. Modules are Python files that contain functions, classes, and variables that can be imported into other programs."
        },
        {
            "title": "Data Structures",
            "summary": "Python provides built-in data structures like lists, tuples, dictionaries, and sets. Lists are ordered, mutable collections. Tuples are ordered, immutable collections. Dictionaries store key-value pairs. Sets are unordered collections of unique elements."
        }
    ]
}

def test_quiz_generation():
    print("Testing quiz generation endpoint...")
    
    try:
        response = requests.post(
            'http://localhost:5000/generate-module-quiz',
            headers={'Content-Type': 'application/json'},
            json={'module_data': test_module}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Quiz generated successfully!")
            print(f"Quiz Title: {data['quiz']['title']}")
            print(f"Number of Questions: {data['quiz']['totalQuestions']}")
            print("\nQuestions:")
            for i, question in enumerate(data['quiz']['questions'], 1):
                print(f"{i}. {question['question']}")
                print(f"   Options: {question['options']}")
                print(f"   Correct Answer: {question['correctAnswer']}")
                print(f"   Explanation: {question['explanation']}")
                print()
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    test_quiz_generation()