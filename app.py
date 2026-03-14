import streamlit as st
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
    <style>
        .score-box {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin: 10px 0;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid;
            margin-bottom: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.07);
        }
        .green  { border-color: #28a745; }
        .red    { border-color: #dc3545; }
        .yellow { border-color: #ffc107; }
    </style>
""", unsafe_allow_html=True)


def extract_text(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def analyze_resume(text: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are an expert career coach and recruiter with 15 years of experience.
Analyze the resume below and respond in EXACTLY this format:

SCORE: [number from 1 to 10]

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

WEAKNESSES:
- [weakness 1]
- [weakness 2]
- [weakness 3]

SUGGESTIONS:
- [suggestion 1]
- [suggestion 2]
- [suggestion 3]
- [suggestion 4]

SUMMARY:
[2-3 sentence overall assessment]

Resume:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return parse(response.choices[0].message.content)


def parse(raw: str) -> dict:
    result = {
        "score": "N/A",
        "strengths": [],
        "weaknesses": [],
        "suggestions": [],
        "summary": ""
    }

    section = None

    for line in raw.strip().split("\n"):
        line = line.strip()

        if line.startswith("SCORE:"):
            result["score"] = line.replace("SCORE:", "").strip()
        elif line == "STRENGTHS:":
            section = "strengths"
        elif line == "WEAKNESSES:":
            section = "weaknesses"
        elif line == "SUGGESTIONS:":
            section = "suggestions"
        elif line == "SUMMARY:":
            section = "summary"
        elif line.startswith("- ") and section in ("strengths", "weaknesses", "suggestions"):
            result[section].append(line[2:])
        elif section == "summary" and line:
            result["summary"] += line + " "

    result["summary"] = result["summary"].strip()
    return result


st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and get instant AI feedback — score, strengths, weaknesses, and tips.")
st.divider()

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading your resume..."):
        resume_text = extract_text(uploaded_file)

    if not resume_text:
        st.error("⚠️ Could not extract text. Make sure this isn't a scanned/image PDF.")
    else:
        st.success(f"✅ Resume loaded — {len(resume_text)} characters extracted.")

        with st.expander("Preview extracted text"):
            st.text(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))

        st.divider()

        if st.button("🚀 Analyze My Resume", use_container_width=True):
            with st.spinner("AI is analyzing your resume..."):
                result = analyze_resume(resume_text)

            st.markdown("### 🎯 Overall Score")
            st.markdown(f'<div class="score-box">{result["score"]} / 10</div>', unsafe_allow_html=True)

            if result["summary"]:
                st.markdown("### 📝 Summary")
                st.info(result["summary"])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Strengths")
                st.markdown('<div class="card green">', unsafe_allow_html=True)
                for item in result["strengths"]:
                    st.markdown(f"✔️ {item}")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("### ❌ Weaknesses")
                st.markdown('<div class="card red">', unsafe_allow_html=True)
                for item in result["weaknesses"]:
                    st.markdown(f"⚠️ {item}")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### 💡 Improvement Suggestions")
            st.markdown('<div class="card yellow">', unsafe_allow_html=True)
            for item in result["suggestions"]:
                st.markdown(f"➡️ {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
            st.caption("Powered by Groq AI · Built with Streamlit")