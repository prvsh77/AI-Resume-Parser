import spacy
import re

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# --- Helper lists (can be expanded later) ---
EDUCATION_KEYWORDS = ["B.Tech", "B.E", "M.Tech", "B.Sc", "M.Sc", "MBA", "PhD", "Bachelor", "Master", "Degree"]
SKILL_KEYWORDS = [
    "Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning", "NLP",
    "TensorFlow", "PyTorch", "Data Science", "AI", "Cloud", "AWS", "Azure", "Docker", "Kubernetes"
]

def extract_name(text):
    """Extract candidate name using Named Entity Recognition (NER)."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_education(text):
    """Extract education qualifications using keywords."""
    matches = []
    for keyword in EDUCATION_KEYWORDS:
        if re.search(keyword, text, re.IGNORECASE):
            matches.append(keyword)
    return list(set(matches))

def extract_skills(text):
    """Extract technical skills from resume text."""
    found_skills = []
    for skill in SKILL_KEYWORDS:
        if re.search(rf"\b{skill}\b", text, re.IGNORECASE):
            found_skills.append(skill)
    return list(set(found_skills))

def extract_experience(text):
    """Extract years of experience (e.g., '5 years of experience')."""
    match = re.search(r'(\d+)\s+(?:years?|yrs?)\s+of\s+experience', text, re.IGNORECASE)
    return match.group(0) if match else None

if __name__ == "__main__":
    # Example text
    sample_text = """
    John Doe is a Machine Learning Engineer with 3 years of experience.
    Skilled in Python, TensorFlow, and Cloud (AWS, Azure).
    He holds a B.Tech in Computer Science from IIT Delhi.
    """
    name = extract_name(sample_text)
    education = extract_education(sample_text)
    skills = extract_skills(sample_text)
    experience = extract_experience(sample_text)

    print("Name:", name)
    print("Education:", education)
    print("Skills:", skills)
    print("Experience:", experience)
