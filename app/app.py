import streamlit as st
import json
import re
import spacy
from pdfminer.high_level import extract_text

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ---------- Helper function ----------
def extract_info(text):
    doc = nlp(text)

    # Extract name
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

    # Education & Skills
    education_keywords = ["B.Tech", "B.E", "M.Tech", "MSc", "B.Sc", "Bachelor", "Master", "PhD"]
    skills_list = ["Python", "Java", "C++", "Machine Learning", "Deep Learning", "SQL", "TensorFlow", "NLP"]

    education = [e for e in education_keywords if e.lower() in text.lower()]
    skills_found = [s for s in skills_list if s.lower() in text.lower()]

    # Experience
    experience = re.findall(r"(\d+)\s*(?:years|yrs)\s*(?:of)?\s*experience", text, re.IGNORECASE)
    experience = experience[0] + " years" if experience else None

    return {
        "Name": name or "Not Found",
        "Email": email or "Not Found",
        "Phone": phone or "Not Found",
        "Skills": skills_found or ["Not Found"],
        "Education": education or ["Not Found"],
        "Experience": experience or "Not Found"
    }

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AI Resume Parser", page_icon="🤖", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f7f9fc;
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        color: #003366;
        margin-bottom: 1rem;
    }
    .subtext {
        text-align: center;
        color: #444;
        margin-bottom: 2rem;
    }
    .info-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .info-card h4 {
        color: #003366;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Resume Parser</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Upload your resume to extract details using NLP and AI</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Upload a Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")
    text = extract_text("temp_resume.pdf")
    info = extract_info(text)

    st.markdown("---")
    st.markdown("### 🧠 Extracted Resume Details")

    # Display results in elegant cards
    for key, value in info.items():
        with st.container():
            st.markdown(f"""
            <div class="info-card">
                <h4>{key}</h4>
                <p>{', '.join(value) if isinstance(value, list) else value}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    json_data = json.dumps(info, indent=4)
    st.download_button(
        label="⬇️ Download Extracted Data (JSON)",
        data=json_data,
        file_name="parsed_resume.json",
        mime="application/json"
    )
