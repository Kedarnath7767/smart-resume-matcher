# 🎯 AI Resume Matcher – ATS Resume Analyzer using AI

<p align="center">
  <b>Analyze your resume against any job description using AI.</b><br>
  Get ATS score, skill gap analysis, semantic similarity insights, and personalized improvement suggestions.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-WebApp-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/NLP-spaCy-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-SentenceTransformers-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Visualization-Plotly-purple?style=for-the-badge" />
</p>

---

## 📌 Overview

AI Resume Matcher is an intelligent ATS resume analysis platform that compares a candidate’s resume with a target job description using Natural Language Processing (NLP), semantic similarity analysis, and AI-powered skill matching.

The system helps job seekers, students, and professionals optimize resumes for ATS (Applicant Tracking Systems) by identifying matching skills, missing skills, semantic relevance, and actionable improvement suggestions.

Unlike traditional keyword-based resume checkers, this project combines exact skill matching with semantic understanding to produce smarter evaluation results.

---

## ✨ Key Features

### 📄 Resume Upload & Parsing
- Upload resumes in PDF format
- Automatic text extraction using PDF parsing
- Resume preprocessing and content cleaning

### 🧠 AI Skill Extraction
- NLP-based technical skill detection
- Extracts AI/ML, NLP, programming, databases, frameworks, tools, and cloud skills
- Intelligent job description skill extraction

### 📊 ATS Resume Scoring
Calculates:
- ATS Compatibility Score
- Skill Match Percentage
- Semantic Similarity Score
- Overall Resume Grade

### 🔍 Skill Gap Analysis
Identifies:
- Matched skills
- Missing required skills
- Bonus skills beyond JD
- Semantic skill relationships

### 💡 Personalized Suggestions
Provides AI-driven recommendations like:
- Resume keyword optimization
- ATS improvement suggestions
- Better project descriptions
- Resume summary alignment tips

### 📚 Learning Roadmap
Suggests improvement paths for missing skills.

### 📈 Interactive Dashboard
Includes:
- Gauge charts
- Skill comparison graphs
- Pie chart analytics
- Skill analysis tables
- Improvement recommendation panels

---

## 🖼️ Project Screenshots

### Home Dashboard
<img width="100%" src="screenshots/home.png">

### ATS Score Analysis
<img width="100%" src="screenshots/score_dashboard.png">

### Skill Analytics
<img width="100%" src="screenshots/skill_analysis.png">

### Matched Skills View
<img width="100%" src="screenshots/matched_skills.png">

### Personalized Suggestions
<img width="100%" src="screenshots/suggestions.png">

---

## ⚙️ How It Works

```text
Upload Resume PDF
        ↓
Extract Resume Text
        ↓
Extract Skills using NLP
        ↓
Extract Job Description Skills
        ↓
Compute Semantic Similarity
        ↓
Match Skills
        ↓
Generate ATS Score
        ↓
Provide Suggestions
        ↓
Display Interactive Dashboard
```

---

## 🏗️ Tech Stack

| Technology | Purpose |
|----------|---------|
| Python | Core backend logic |
| Streamlit | Interactive web UI |
| spaCy | NLP processing |
| Sentence Transformers | Semantic similarity |
| Scikit-learn | Cosine similarity scoring |
| Plotly | Interactive visualizations |
| pdfplumber | PDF text extraction |
| Pandas | Data manipulation |
| NumPy | Numerical operations |

## ▶️ Run Application

```bash
streamlit run app.py
```


---

## 🧠 AI Models Used

Used for:
- Semantic similarity matching
- Context-aware resume analysis
- AI skill comparison

---

### spaCy NLP
Model:
```bash
en_core_web_sm
```

Used for:
- Text preprocessing
- Skill extraction
- NLP entity analysis

---

## 🎯 Use Cases

Perfect for:

- Students preparing internship resumes
- Freshers applying for jobs
- Professionals optimizing ATS compatibility
- AI-powered HR screening demos
- Resume improvement platforms

---

## 🔒 Privacy & Security

✅ No external APIs used  
✅ No API keys required  
✅ 100% local execution  
✅ No resume data stored  
✅ Secure offline processing  

---

## 🚀 Future Improvements

Planned upgrades:

- Multi-resume comparison
- Resume rewriting with LLMs
- LinkedIn profile analysis
- Cover letter generation
- Job recommendation engine
- PDF export reports
- OCR support for scanned resumes
- Cloud deployment

---

## 👨‍💻 Author

### Boya Kedarnath
---

## 🌟 Support

If you found this project useful:

⭐ Star this repository  
🍴 Fork the project  
📢 Share with others  

---

## 📜 License

This project is open-source under the MIT License.