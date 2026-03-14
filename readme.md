# 📄 AI Resume Analyzer for Job Seekers

An AI-powered resume analyzer built with Python and Streamlit.  
Upload your PDF resume and get instant feedback — score, strengths, weaknesses, and actionable improvement tips.

---

## 🚀 Live Demo

> Run locally by following the steps below.

---

## 🖼️ Screenshot

![AI Resume Analyzer Screenshot](screenshot.png)

---

## ✨ Features

- 📤 Upload any PDF resume
- 🔍 Automatic text extraction using PyPDF
- 🤖 AI-powered analysis via Groq (Llama 3.3 70B)
- 📊 Outputs:
  - Overall score out of 10
  - Written summary
  - Top strengths
  - Key weaknesses
  - Improvement suggestions

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| PyPDF | PDF text extraction |
| Groq API | Free AI inference (Llama 3.3 70B) |
| python-dotenv | API key management |

---

## ⚙️ How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/LuisSebastianDelRosario/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure
```
ai-resume-analyzer/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── .env                # API key (never committed)
├── .gitignore          # Ignored files
└── README.md           # You are here
```

---

## 🔒 Security Note

Your `.env` file is listed in `.gitignore` and will never be pushed to GitHub.  
Never share your API key publicly.

---

## 👤 Author

**Luis Sebastian Del Rosario**  
[GitHub](https://github.com/LuisSebastianDelRosario)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).