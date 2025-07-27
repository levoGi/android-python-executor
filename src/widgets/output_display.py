"""
Custom Output Display Widget for code execution results
"""

from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.lang import Builder

class OutputDisplay(TextInput):
    """Enhanced text input for displaying code execution output"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_output_display()
    
    def setup_output_display(self):
        """Set up the output display with appropriate styling"""
        # Make it read-only
        self.readonly = True
        
        # Set colors for output display
        self.background_color = (0.1, 0.1, 0.1, 1)  # Dark background
        self.foreground_color = (0.9, 0.9, 0.9, 1)  # Light text
        self.cursor_color = (0.2, 0.6, 0.8, 1)      # Blue cursor
        
        # Set font and size
        self.font_size = dp(14)
        self.font_name = 'RobotoMono-Regular'  # Monospace font
        
        # Enable multiline and scrolling
        self.multiline = True
        self.scroll_type = ['bars']
        self.bar_width = dp(10)
        
        # Set padding
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
    
    def append_text(self, text):
        """Append text to the current output"""
        current_text = self.text
        if current_text:
            self.text = current_text + '\n' + text
        else:
            self.text = text
        
        # Scroll to bottom
        self.cursor = (0, len(self.text))
    
    def clear_output(self):
        """Clear the output display"""
        self.text = ""
    
    def set_output(self, text):
        """Set the output text"""
        self.text = str(text)

class OutputDisplayWidget(BoxLayout):
    """Container widget for the output display with controls"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(5)
        
        # Create header
        self.header = self.create_header()
        
        # Create output display
        self.output_display = OutputDisplay()
        
        # Create control buttons
        self.controls = self.create_controls()
        
        # Add widgets to layout
        self.add_widget(self.header)
        self.add_widget(self.output_display)
        self.add_widget(self.controls)
    
    def create_header(self):
        """Create the header section"""
        header = BoxLayout(size_hint_y=None, height=dp(30))
        
        label = Label(
            text='Execution Output',
            font_size=dp(16),
            bold=True,
            size_hint_x=0.7
        )
        
        header.add_widget(label)
        return header
    
    def create_controls(self):
        """Create the control buttons"""
        controls = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        
        copy_btn = Button(
            text='Copy',
            size_hint_x=0.5,
            background_color=(0.6, 0.6, 0.6, 1),
            on_press=self.copy_output
        )
        
        clear_btn = Button(
            text='Clear',
            size_hint_x=0.5,
            background_color=(0.8, 0.2, 0.2, 1),
            on_press=self.clear_output
        )
        
        controls.add_widget(copy_btn)
        controls.add_widget(clear_btn)
        return controls
    
    def display_output(self, text):
        """Display output text"""
        self.output_display.set_output(text)
    
    def append_output(self, text):
        """Append text to output"""
        self.output_display.append_text(text)
    
    def clear_output(self, instance=None):
        """Clear the output"""
        self.output_display.clear_output()
    
    def copy_output(self, instance=None):
        """Copy output to clipboard"""
        try:
            from kivy.core.clipboard import Clipboard
            output_text = self.output_display.text
            Clipboard.put(output_text)
            
            # Show success message
            self.append_output("\n[Output copied to clipboard]")
        except Exception as e:
            self.append_output(f"\n[Error copying to clipboard: {str(e)}]")
    
    def get_output_text(self):
        """Get the current output text"""
        return self.output_display.text 