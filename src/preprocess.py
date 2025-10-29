import re
import nltk
from nltk.tokenize import word_tokenize

# Download required tokenizer data (only once)
nltk.download('punkt', quiet=True)

def clean_text(text):
    """
    Cleans and normalizes resume text.
    Removes unwanted characters, extra spaces, etc.
    """
    # Remove multiple newlines, tabs, etc.
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)

    # Remove weird unicode characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove unwanted punctuation (optional)
    text = re.sub(r'[{}<>]', ' ', text)

    return text.strip()

def extract_email(text):
    """Extracts the first valid email address found."""
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    """Extracts the first valid phone number found."""
    phone_pattern = r'(\+?\d{1,3}[\s-]?)?(\d{10})'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None

def tokenize_text(text):
    """Tokenizes text into individual words."""
    return word_tokenize(text)

if __name__ == "__main__":
    # Example test
    sample_text = """
    John Doe
    Email: johndoe@gmail.com
    Phone: +91 9876543210
    Data Scientist with experience in Python, NLP, and AI.
    """
    
    cleaned = clean_text(sample_text)
    email = extract_email(cleaned)
    phone = extract_phone(cleaned)
    tokens = tokenize_text(cleaned)

    print("Cleaned Text:", cleaned)
    print("Email:", email)
    print("Phone:", phone)
    print("Tokens:", tokens[:15])  # show first 15
