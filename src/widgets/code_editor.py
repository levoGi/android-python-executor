"""
Custom Code Editor Widget with syntax highlighting
"""

from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import Label
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder

class CodeEditor(TextInput):
    """Enhanced text input for code editing"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_editor()
    
    def setup_editor(self):
        """Set up the editor with code-friendly settings"""
        # Set monospace font for better code readability
        self.font_name = 'RobotoMono-Regular'  # Fallback to default if not available
        
        # Set colors for better code visibility
        self.background_color = (0.95, 0.95, 0.95, 1)  # Light gray background
        self.foreground_color = (0.1, 0.1, 0.1, 1)     # Dark text
        self.cursor_color = (0.2, 0.6, 0.8, 1)         # Blue cursor
        
        # Enable multiline and other code-friendly features
        self.multiline = True
        self.tab_width = 4  # 4 spaces for indentation
        
        # Set padding for better text visibility
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
    
    def insert_text(self, substring, from_undo=False):
        """Override to handle tab key for indentation"""
        if substring == '\t':
            substring = '    '  # Replace tab with 4 spaces
        return super().insert_text(substring, from_undo)
    
    def on_text_validate(self):
        """Handle Enter key for auto-indentation"""
        # Get current line
        current_line = self.text.split('\n')[self.cursor_index_to_cursor_pos(self.cursor_index())[1]]
        
        # Calculate indentation
        indent = len(current_line) - len(current_line.lstrip())
        
        # If line ends with ':', add extra indentation
        if current_line.strip().endswith(':'):
            indent += 4
        
        # Insert newline with proper indentation
        spaces = ' ' * indent
        self.insert_text(f'\n{spaces}')
        return True

class CodeEditorWidget(BoxLayout):
    """Container widget for the code editor with line numbers"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        
        # Create line numbers widget
        self.line_numbers = LineNumbersWidget()
        
        # Create code editor
        self.code_editor = CodeEditor()
        self.code_editor.bind(text=self.on_text_change)
        
        # Add widgets to layout
        self.add_widget(self.line_numbers)
        self.add_widget(self.code_editor)
    
    def on_text_change(self, instance, value):
        """Update line numbers when text changes"""
        lines = value.split('\n')
        self.line_numbers.update_lines(len(lines))

class LineNumbersWidget(TextInput):
    """Widget to display line numbers"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_line_numbers()
    
    def setup_line_numbers(self):
        """Set up the line numbers widget"""
        self.readonly = True
        self.size_hint_x = None
        self.width = dp(50)
        self.background_color = (0.9, 0.9, 0.9, 1)
        self.foreground_color = (0.5, 0.5, 0.5, 1)
        self.font_size = dp(12)
        self.padding = [dp(5), dp(10), dp(5), dp(10)]
        self.multiline = True
    
    def update_lines(self, line_count):
        """Update the line numbers display"""
        numbers = '\n'.join(str(i + 1) for i in range(line_count))
        self.text = numbers 