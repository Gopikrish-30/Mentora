# Introduction to Python Programming

## Course Overview
Python is a high-level, interpreted programming language that emphasizes code readability with its notable use of significant whitespace. It is widely used in web development, data science, artificial intelligence, and automation.

## Chapter 1: Getting Started
### Basic Syntax
Python syntax is designed to be clear and readable. Unlike many other programming languages, Python uses indentation to indicate code blocks.

Example:
```python
if True:
    print("Hello, World!")
    if x > 0:
        print("Positive number")
```

### Variables and Data Types
- Integers: Whole numbers (e.g., 5, -17, 1000)
- Floats: Decimal numbers (e.g., 3.14, -0.001, 2.0)
- Strings: Text data ("Hello", 'Python')
- Booleans: True or False
- Lists: Ordered collections [1, 2, 3]
- Dictionaries: Key-value pairs {"name": "John", "age": 30}

## Chapter 2: Control Flow
### Conditional Statements
Use if, elif, and else for decision making:
```python
age = 18
if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
else:
    print("Adult")
```

### Loops
Two main types of loops:
1. For loops - iterate over sequences
2. While loops - repeat while condition is true

## Chapter 3: Functions
Functions are reusable blocks of code:
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
```