"""
Code Executor - Safely executes Python code and captures output
"""

import sys
import io
import traceback
import ast
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, Optional

class CodeExecutor:
    """Handles safe execution of Python code"""
    
    def __init__(self):
        self.global_vars = {}
        self.local_vars = {}
        self.output_buffer = io.StringIO()
        self.error_buffer = io.StringIO()
        
        # Functions that require user input
        self.input_functions = {
            'input': 'input() function requires user interaction',
            'raw_input': 'raw_input() function requires user interaction (Python 2)',
            'getpass': 'getpass module requires user interaction',
            'readline': 'readline module requires user interaction',
            'msvcrt': 'msvcrt module requires user interaction (Windows)',
            'tty': 'tty module requires user interaction (Unix)',
            'termios': 'termios module requires user interaction (Unix)',
            'select': 'select module can be used for user input',
            'keyboard': 'keyboard module requires user interaction',
            'pynput': 'pynput module requires user interaction',
            'pyautogui': 'pyautogui module requires user interaction',
            'tkinter': 'tkinter can be used for user input dialogs',
            'PyQt5': 'PyQt5 can be used for user input dialogs',
            'PySide2': 'PySide2 can be used for user input dialogs',
            'wx': 'wxPython can be used for user input dialogs'
        }
    
    def check_for_input_functions(self, code: str) -> list:
        """
        Check if the code contains functions that require user input
        
        Args:
            code: Python code to analyze
            
        Returns:
            List of detected input functions
        """
        detected_functions = []
        
        try:
            # Parse the code to analyze it
            tree = ast.parse(code)
            
            # Check for function calls and imports
            for node in ast.walk(tree):
                # Check for function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        if func_name in self.input_functions:
                            detected_functions.append(func_name)
                
                # Check for imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in self.input_functions:
                            detected_functions.append(alias.name)
                
                # Check for from imports
                elif isinstance(node, ast.ImportFrom):
                    if node.module in self.input_functions:
                        detected_functions.append(node.module)
                    for alias in node.names:
                        if alias.name in self.input_functions:
                            detected_functions.append(alias.name)
        
        except SyntaxError:
            # If the code has syntax errors, we'll let the normal execution handle it
            pass
        
        return list(set(detected_functions))  # Remove duplicates
    
    def execute(self, code: str) -> str:
        """
        Execute Python code safely and return the output
        
        Args:
            code: Python code to execute
            
        Returns:
            String containing the execution output and any errors
        """
        # Check for input functions first
        input_functions = self.check_for_input_functions(code)
        if input_functions:
            error_msg = "❌ Code execution blocked!\n\n"
            error_msg += "The following functions require user input and are not allowed:\n"
            for func in input_functions:
                error_msg += f"• {func}: {self.input_functions.get(func, 'Requires user interaction')}\n"
            error_msg += "\n💡 Suggestions:\n"
            error_msg += "• Use hardcoded values instead of input()\n"
            error_msg += "• Define variables with your test data\n"
            error_msg += "• Use random values for testing\n"
            error_msg += "• Example: name = 'John' instead of name = input('Enter name: ')\n"
            return error_msg
        
        # Clear previous output
        self.output_buffer = io.StringIO()
        self.error_buffer = io.StringIO()
        
        try:
            # Capture stdout and stderr
            with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
                # Execute the code
                exec(code, self.global_vars, self.local_vars)
            
            # Get captured output
            stdout_output = self.output_buffer.getvalue()
            stderr_output = self.error_buffer.getvalue()
            
            # Combine outputs
            result = ""
            if stdout_output:
                result += f"✅ Output:\n{stdout_output}\n"
            if stderr_output:
                result += f"⚠️  Warnings:\n{stderr_output}\n"
            
            if not result.strip():
                result = "✅ Code executed successfully (no output)"
            
            return result
            
        except Exception as e:
            # Get the full traceback
            error_traceback = traceback.format_exc()
            return f"❌ Execution Error:\n{error_traceback}"
        
        finally:
            # Clean up
            self.output_buffer.close()
            self.error_buffer.close()
    
    def execute_with_timeout(self, code: str, timeout: float = 5.0) -> str:
        """
        Execute code with a timeout limit
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            String containing the execution output
        """
        import signal
        import threading
        import time
        
        result = [None]
        exception = [None]
        
        def target():
            try:
                result[0] = self.execute(code)
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            return f"⏰ Execution timed out after {timeout} seconds"
        
        if exception[0]:
            return f"❌ Execution Error: {str(exception[0])}"
        
        return result[0]
    
    def reset_environment(self):
        """Reset the execution environment"""
        self.global_vars = {}
        self.local_vars = {}
    
    def get_variables(self) -> Dict[str, Any]:
        """Get current variables in the execution environment"""
        return self.local_vars.copy()
    
    def set_variable(self, name: str, value: Any):
        """Set a variable in the execution environment"""
        self.local_vars[name] = value 