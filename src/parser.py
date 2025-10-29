import os
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        text = extract_pdf_text(file_path)
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        full_text = [p.text for p in doc.paragraphs]
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_resume_text(file_path):
    """Detect file type and extract resume text."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return ""

if __name__ == "__main__":
    # Example usage
    sample_path = "D:/projects/AI Resume parser/data/sample_resumes/sample.pdf"# change if needed
    text = extract_resume_text(sample_path)
    print(text[:1000])  # print first 1000 chars for check
