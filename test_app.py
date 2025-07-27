#!/usr/bin/env python3
"""
Test script for Python Code Executor app
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_code_executor():
    """Test the code executor functionality"""
    from src.utils.code_executor import CodeExecutor
    
    executor = CodeExecutor()
    
    # Test simple code
    code = 'print("Hello, World!")'
    result = executor.execute(code)
    print("Test 1 - Simple print:")
    print(result)
    print("-" * 50)
    
    # Test calculation
    code = '''
x = 10
y = 20
result = x + y
print(f"{x} + {y} = {result}")
'''
    result = executor.execute(code)
    print("Test 2 - Calculation:")
    print(result)
    print("-" * 50)
    
    # Test function
    code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
'''
    result = executor.execute(code)
    print("Test 3 - Function:")
    print(result)
    print("-" * 50)
    
    # Test input detection - should be blocked
    code = '''
name = input("Enter your name: ")
print(f"Hello, {name}!")
'''
    result = executor.execute(code)
    print("Test 4 - Input detection (should be blocked):")
    print(result)
    print("-" * 50)
    
    # Test import detection - should be blocked
    code = '''
import tkinter
root = tkinter.Tk()
root.title("Test")
'''
    result = executor.execute(code)
    print("Test 5 - Import detection (should be blocked):")
    print(result)
    print("-" * 50)
    
    # Test safe alternative to input
    code = '''
# Safe alternative to input()
name = "John"  # Instead of name = input("Enter name: ")
age = 25       # Instead of age = int(input("Enter age: "))
print(f"Hello, {name}! You are {age} years old.")
'''
    result = executor.execute(code)
    print("Test 6 - Safe alternative to input:")
    print(result)
    print("-" * 50)

def test_file_manager():
    """Test the file manager functionality"""
    from src.utils.file_manager import FileManager
    
    file_manager = FileManager()
    
    # Test saving code
    test_code = 'print("This is a test file")'
    try:
        filename = file_manager.save_code(test_code, "test_file.py")
        print(f"Test 7 - File saved: {filename}")
    except Exception as e:
        print(f"Test 7 - File save error: {e}")
    
    # Test listing files
    try:
        files = file_manager.list_files()
        print(f"Test 8 - Found {len(files)} files")
        for file in files[:3]:  # Show first 3 files
            print(f"  - {file['name']}")
    except Exception as e:
        print(f"Test 8 - File list error: {e}")

if __name__ == '__main__':
    print("Testing Python Code Executor Components")
    print("=" * 50)
    
    test_code_executor()
    test_file_manager()
    
    print("\nAll tests completed!") 