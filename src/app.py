"""
Main application class for Python Code Executor
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform

from .screens.editor_screen import EditorScreen
from .screens.output_screen import OutputScreen

class PythonCodeExecutorApp(App):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Python Code Executor"
        self.screen_manager = None
        
    def build(self):
        """Build the application UI"""
        # Set up the screen manager
        self.screen_manager = ScreenManager()
        
        # Add screens
        self.screen_manager.add_widget(EditorScreen(name='editor'))
        self.screen_manager.add_widget(OutputScreen(name='output'))
        
        # Set mobile-specific configurations
        if platform == 'android':
            self.setup_android()
        
        return self.screen_manager
    
    def setup_android(self):
        """Configure Android-specific settings"""
        # Request necessary permissions
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])
        
        # Set fullscreen mode
        Window.fullscreen = 'auto'
    
    def on_pause(self):
        """Handle app pause (Android)"""
        return True
    
    def on_resume(self):
        """Handle app resume (Android)"""
        pass
    
    def get_screen(self, name):
        """Get a screen by name"""
        return self.screen_manager.get_screen(name)
    
    def switch_screen(self, screen_name):
        """Switch to a different screen"""
        self.screen_manager.current = screen_name 