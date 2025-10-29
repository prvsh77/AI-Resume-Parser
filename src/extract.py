import json
import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Read preprocessed resume text
with open("data/processed/cleaned_sample.txt", "r", encoding="utf-8") as f:
    text = f.read()

doc = nlp(text)

# --------- Extraction logic ----------

# Extract name (first PERSON entity)
name = None
for ent in doc.ents:
    if ent.label_ == "PERSON":
        name = ent.text
        break

# Extract email
email = re.findall(r"[\w\.-]+@[\w\.-]+", text)
email = email[0] if email else None

# Extract phone number
phone = re.findall(r"\+?\d[\d -]{8,12}\d", text)
phone = phone[0] if phone else None

# Extract education-related entities
education_keywords = ["B.Tech", "B.E", "M.Tech", "MSc", "B.Sc", "Bachelor", "Master", "PhD"]
education = [word for word in education_keywords if word.lower() in text.lower()]

# Extract skills
skills_list = ["Python", "Java", "C++", "Machine Learning", "Deep Learning", "SQL", "TensorFlow", "NLP"]
skills_found = [skill for skill in skills_list if skill.lower() in text.lower()]

# Extract experience
experience = re.findall(r"(\d+)\s*(?:years|yrs)\s*(?:of)?\s*experience", text, re.IGNORECASE)
experience = experience[0] + " years" if experience else None

# --------- Save structured output ----------
parsed_data = {
    "Name": name or "Not Found",
    "Email": email or "Not Found",
    "Phone": phone or "Not Found",
    "Skills": skills_found or ["Not Found"],
    "Education": education or ["Not Found"],
    "Experience": experience or "Not Found",
}

with open("data/output/extracted_info.json", "w", encoding="utf-8") as out:
    json.dump(parsed_data, out, indent=4)

print("✅ Information extraction completed successfully!")
print(json.dumps(parsed_data, indent=4))
