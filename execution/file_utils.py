import os

def read_file(file_path):
    """Reads content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def save_file(file_path, content):
    """Saves content to a file, creating directories if needed."""
    try:
        dirname = os.path.dirname(file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file {file_path}: {str(e)}")
        return False

def list_files(directory, extension=None):
    """Lists files in a directory, optionally filtered by extension."""
    try:
        files = os.listdir(directory)
        if extension:
            return [f for f in files if f.endswith(extension)]
        return files
    except Exception as e:
        return f"Error listing files in {directory}: {str(e)}"

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file using pypdf."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path, strict=False)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except ImportError:
        return "Error: pypdf library not installed. Run 'pip install pypdf'."
    except Exception as e:
        return f"Error reading PDF {file_path}: {str(e)}"
