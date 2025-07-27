# Python Code Executor - Android App

A mobile application built with Kivy that allows users to write and execute Python code directly on their Android device.

## Features

- **Code Editor**: Write Python code with syntax highlighting
- **Code Execution**: Execute Python scripts with a single button press
- **Output Display**: View execution results and error messages
- **File Management**: Save and load code files
- **Mobile Optimized**: Touch-friendly interface designed for mobile devices

## Technology Stack

- **Kivy**: Cross-platform Python framework for mobile development
- **KivyMD**: Material Design components for Kivy
- **Python**: Core programming language
- **Buildozer**: Tool for packaging Kivy apps for Android

## Setup Instructions

### Prerequisites

1. Python 3.7+ installed
2. Android SDK and NDK (for building APK)
3. Buildozer (for Android packaging)

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app locally:
   ```bash
   python main.py
   ```

### Building for Android

1. Install Buildozer:
   ```bash
   pip install buildozer
   ```

2. Initialize Buildozer:
   ```bash
   buildozer init
   ```

3. Build the APK:
   ```bash
   buildozer android debug
   ```

## Project Structure

```
android-python-executor/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── buildozer.spec         # Buildozer configuration
├── assets/                # Static assets (icons, images)
├── src/                   # Source code
│   ├── __init__.py
│   ├── app.py            # Main app class
│   ├── screens/          # Kivy screen definitions
│   │   ├── __init__.py
│   │   ├── editor_screen.py
│   │   └── output_screen.py
│   ├── widgets/          # Custom widgets
│   │   ├── __init__.py
│   │   ├── code_editor.py
│   │   └── output_display.py
│   └── utils/            # Utility functions
│       ├── __init__.py
│       ├── code_executor.py
│       └── file_manager.py
└── README.md
```

## Usage

1. Launch the app
2. Write Python code in the editor
3. Tap the "Run" button to execute the code
4. View results in the output panel
5. Save your code for later use

## License

MIT License 