"""
Editor Screen - Main interface for writing and executing Python code
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from ..utils.code_executor import CodeExecutor
from ..utils.file_manager import FileManager

class EditorScreen(Screen):
    """Main editor screen for writing Python code"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code_executor = CodeExecutor()
        self.file_manager = FileManager()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        title_label = Label(
            text='Python Code Editor',
            font_size=dp(18),
            bold=True,
            size_hint_x=0.6
        )
        
        run_button = Button(
            text='Run',
            size_hint_x=0.2,
            background_color=(0.2, 0.8, 0.2, 1),
            on_press=self.run_code
        )
        
        save_button = Button(
            text='Save',
            size_hint_x=0.2,
            background_color=(0.2, 0.6, 0.8, 1),
            on_press=self.save_code
        )
        
        header.add_widget(title_label)
        header.add_widget(run_button)
        header.add_widget(save_button)
        
        # Code editor area
        editor_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        editor_label = Label(
            text='Write your Python code here:',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(14)
        )
        
        # Code editor
        self.code_editor = TextInput(
            hint_text='# Write your Python code here\n\nprint("Hello, World!")\n\n# Example: Calculate fibonacci\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)\n\nprint(fib(10))\n\n# Example: Safe alternatives to input()\n# Instead of: name = input("Enter name: ")\nname = "John"\nage = 25\nprint(f"Hello, {name}! You are {age} years old.")\n\n# Note: input(), tkinter, and other user input functions are not allowed',
            font_size=dp(14),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            cursor_color=(0.2, 0.6, 0.8, 1),
            multiline=True,
            size_hint_y=None,
            height=dp(300)
        )
        
        editor_layout.add_widget(editor_label)
        editor_layout.add_widget(self.code_editor)
        
        # File operations
        file_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        
        load_button = Button(
            text='Load File',
            size_hint_x=0.5,
            background_color=(0.8, 0.6, 0.2, 1),
            on_press=self.load_file
        )
        
        clear_button = Button(
            text='Clear',
            size_hint_x=0.5,
            background_color=(0.8, 0.2, 0.2, 1),
            on_press=self.clear_code
        )
        
        file_layout.add_widget(load_button)
        file_layout.add_widget(clear_button)
        
        # Add all widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(editor_layout)
        main_layout.add_widget(file_layout)
        
        self.add_widget(main_layout)
    
    def run_code(self, instance=None):
        """Execute the Python code"""
        code = self.code_editor.text
        if not code.strip():
            return
        
        try:
            # Execute the code and get results
            result = self.code_executor.execute(code)
            
            # Switch to output screen to show results
            app = self.manager.get_screen('output')
            app.display_output(result)
            self.manager.current = 'output'
            
        except Exception as e:
            # Show error in output screen
            app = self.manager.get_screen('output')
            app.display_output(f"Error: {str(e)}")
            self.manager.current = 'output'
    
    def save_code(self, instance=None):
        """Save the current code to a file"""
        code = self.code_editor.text
        if code.strip():
            try:
                filename = self.file_manager.save_code(code)
                # Show success message
                app = self.manager.get_screen('output')
                app.display_output(f"Code saved successfully to: {filename}")
                self.manager.current = 'output'
            except Exception as e:
                app = self.manager.get_screen('output')
                app.display_output(f"Error saving file: {str(e)}")
                self.manager.current = 'output'
    
    def load_file(self, instance=None):
        """Load code from a file"""
        try:
            code = self.file_manager.load_code()
            if code:
                self.code_editor.text = code
        except Exception as e:
            app = self.manager.get_screen('output')
            app.display_output(f"Error loading file: {str(e)}")
            self.manager.current = 'output'
    
    def clear_code(self, instance=None):
        """Clear the code editor"""
        self.code_editor.text = "" 