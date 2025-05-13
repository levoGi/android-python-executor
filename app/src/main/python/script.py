import sys
import io

def run_code(code):
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        exec(code, {})
        output = mystdout.getvalue()
    except Exception as e:
        output = "Error: " + str(e)
    finally:
        sys.stdout = old_stdout

    return output
