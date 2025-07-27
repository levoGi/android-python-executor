#!/usr/bin/env python3
"""
Python Code Executor - Android App
Main entry point for the Kivy application
"""

import os
import sys
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.resources import resource_add_path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import PythonCodeExecutorApp

if __name__ == '__main__':
    # Set window size for desktop testing (will be fullscreen on mobile)
    Window.size = (400, 700)
    
    # Add resource paths
    resource_add_path(os.path.join(os.path.dirname(__file__), 'assets'))
    
    # Run the application
    PythonCodeExecutorApp().run() 