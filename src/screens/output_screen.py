"""
Output Screen - Displays code execution results and error messages
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

class OutputScreen(Screen):
    """Screen for displaying code execution output"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        title_label = Label(
            text='Code Execution Output',
            font_size=dp(18),
            bold=True,
            size_hint_x=0.7
        )
        
        back_button = Button(
            text='Back to Editor',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.8, 1),
            on_press=self.go_back
        )
        
        header.add_widget(title_label)
        header.add_widget(back_button)
        
        # Output display area
        output_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        output_label = Label(
            text='Execution Results:',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(14)
        )
        
        # Output display
        self.output_display = TextInput(
            readonly=True,
            font_size=dp(14),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0.9, 0.9, 0.9, 1),
            cursor_color=(0.2, 0.6, 0.8, 1),
            multiline=True,
            size_hint_y=None,
            height=dp(400)
        )
        
        output_layout.add_widget(output_label)
        output_layout.add_widget(self.output_display)
        
        # Action buttons
        button_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        
        copy_button = Button(
            text='Copy Output',
            size_hint_x=0.5,
            background_color=(0.6, 0.6, 0.6, 1),
            on_press=self.copy_output
        )
        
        clear_button = Button(
            text='Clear Output',
            size_hint_x=0.5,
            background_color=(0.8, 0.2, 0.2, 1),
            on_press=self.clear_output
        )
        
        button_layout.add_widget(copy_button)
        button_layout.add_widget(clear_button)
        
        # Add all widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(output_layout)
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def display_output(self, output):
        """Display the execution output"""
        self.output_display.text = str(output)
    
    def go_back(self, instance=None):
        """Return to the editor screen"""
        self.manager.current = 'editor'
    
    def copy_output(self, instance=None):
        """Copy the output to clipboard"""
        try:
            from kivy.core.clipboard import Clipboard
            output_text = self.output_display.text
            Clipboard.put(output_text)
            
            # Show success message
            self.output_display.text += "\n\n[Output copied to clipboard]"
        except Exception as e:
            self.output_display.text += f"\n\n[Error copying to clipboard: {str(e)}]"
    
    def clear_output(self, instance=None):
        """Clear the output display"""
        self.output_display.text = ""