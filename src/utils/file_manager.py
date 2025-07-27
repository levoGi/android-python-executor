"""
File Manager - Handles saving and loading Python code files
"""

import os
import datetime
from typing import Optional
from kivy.utils import platform

class FileManager:
    """Manages file operations for the Python code executor"""
    
    def __init__(self):
        self.base_dir = self._get_base_directory()
        self.ensure_directory_exists()
    
    def _get_base_directory(self) -> str:
        """Get the base directory for storing files"""
        if platform == 'android':
            # On Android, use the app's external storage directory
            from android.storage import primary_external_storage_path
            base_path = primary_external_storage_path()
            return os.path.join(base_path, 'PythonCodeExecutor')
        else:
            # On desktop, use a local directory
            return os.path.join(os.path.expanduser('~'), 'PythonCodeExecutor')
    
    def ensure_directory_exists(self):
        """Ensure the base directory exists"""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)
    
    def save_code(self, code: str, filename: Optional[str] = None) -> str:
        """
        Save Python code to a file
        
        Args:
            code: Python code to save
            filename: Optional filename (if not provided, auto-generate)
            
        Returns:
            The filename where the code was saved
        """
        if not filename:
            # Generate a filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"python_code_{timestamp}.py"
        
        # Ensure .py extension
        if not filename.endswith('.py'):
            filename += '.py'
        
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            return filename
        except Exception as e:
            raise Exception(f"Failed to save file: {str(e)}")
    
    def load_code(self, filename: Optional[str] = None) -> Optional[str]:
        """
        Load Python code from a file
        
        Args:
            filename: Optional filename to load (if not provided, show file picker)
            
        Returns:
            The loaded code or None if cancelled
        """
        if not filename:
            # On Android, we can use a file picker
            if platform == 'android':
                return self._load_with_picker()
            else:
                # On desktop, list available files
                return self._load_from_list()
        
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Failed to load file: {str(e)}")
    
    def _load_with_picker(self) -> Optional[str]:
        """Load file using Android file picker"""
        try:
            from plyer import filechooser
            result = filechooser.open_file(
                title="Select Python file",
                filters=[("Python files", "*.py"), ("All files", "*.*")]
            )
            
            if result:
                filepath = result[0]
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            raise Exception(f"File picker error: {str(e)}")
    
    def _load_from_list(self) -> Optional[str]:
        """Load file from a list of available files (desktop)"""
        files = self.list_files()
        if not files:
            raise Exception("No saved files found")
        
        # For now, return the most recent file
        # In a full implementation, you'd show a file selection dialog
        latest_file = max(files, key=lambda x: x['modified'])
        return self.load_code(latest_file['name'])
    
    def list_files(self) -> list:
        """
        List all saved Python files
        
        Returns:
            List of dictionaries with file information
        """
        files = []
        
        try:
            for filename in os.listdir(self.base_dir):
                if filename.endswith('.py'):
                    filepath = os.path.join(self.base_dir, filename)
                    stat = os.stat(filepath)
                    files.append({
                        'name': filename,
                        'size': stat.st_size,
                        'modified': stat.st_mtime,
                        'path': filepath
                    })
        except Exception:
            pass
        
        return sorted(files, key=lambda x: x['modified'], reverse=True)
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a saved file
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception:
            return False
    
    def get_file_info(self, filename: str) -> Optional[dict]:
        """
        Get information about a file
        
        Args:
            filename: Name of the file
            
        Returns:
            Dictionary with file information or None if not found
        """
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            if os.path.exists(filepath):
                stat = os.stat(filepath)
                return {
                    'name': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'path': filepath
                }
        except Exception:
            pass
        
        return None 