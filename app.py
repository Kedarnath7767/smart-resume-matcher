# app.py - Main Application File

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

# Import our utility modules
from utils.pdf_extractor import extract_text_from_pdf, extract_sections
from utils.skill_extractor import (
    extract_skills_with_spacy,
    categorize_skills,
    get_skill_frequency
)
from utils.matcher import (
    calculate_similarity_score,
    get_matched_skills,
    get_missing_skills,
    get_extra_skills,
    calculate_skill_match_percentage,
    get_semantic_skill_matches,
    get_overall_grade
)
from utils.suggester import (
    generate_improvement_suggestions,
    get_learning_roadmap
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #0e1117;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }

    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }

    /* Skill badges */
    .skill-badge-green {
        background-color: #00C851;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
        display: inline-block;
    }

    .skill-badge-red {
        background-color: #FF4444;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
        display: inline-block;
    }

    .skill-badge-blue {
        background-color: #33B5E5;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
        display: inline-block;
    }

    /* Suggestion cards */
.suggestion-card {
    background-color: #ffffff;
    color: #000000;
    border-left: 5px solid #667eea;
    padding: 1.2rem;
    border-radius: 10px;
    margin: 0.8rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.suggestion-card strong {
    color: #333333;
}

.suggestion-card small {
    color: #444444;
}

    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #667eea;
        margin: 1.5rem 0 0.5rem 0;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.3rem;
    }

    /* Metric boxes */
    .metric-box {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #333;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS FOR UI
# ============================================================

def render_skill_badges(skills: list, badge_class: str):
    """Render skills as colored badges."""
    if not skills:
        st.write("None found")
        return

    badges_html = ""
    for skill in skills:
        badges_html += f'<span class="{badge_class}">{skill.title()}</span> '

    st.markdown(badges_html, unsafe_allow_html=True)


def create_gauge_chart(score: float, title: str):
    """Create a gauge chart for score visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'color': 'white'}},
        number={'font': {'size': 36, 'color': 'white'}, 'suffix': '%'},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "white",
                'tickfont': {'color': 'white'}
            },
            'bar': {'color': get_gauge_color(score)},
            'bgcolor': "#1a1a2e",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 35], 'color': '#2d0a0a'},
                {'range': [35, 50], 'color': '#2d1a0a'},
                {'range': [50, 65], 'color': '#2d2a0a'},
                {'range': [65, 80], 'color': '#0a2d1a'},
                {'range': [80, 100], 'color': '#0a1a2d'},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="#0e1117",
        font={'color': 'white'},
        height=280,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


def get_gauge_color(score: float) -> str:
    """Return color based on score."""
    if score >= 80:
        return "#00C851"
    elif score >= 65:
        return "#33B5E5"
    elif score >= 50:
        return "#FFBB33"
    elif score >= 35:
        return "#FF8800"
    else:
        return "#FF4444"


def create_skills_bar_chart(
    matched: list,
    missing: list,
    extra: list
):
    """Create a bar chart showing skill breakdown."""
    categories = ['Matched Skills ✅', 'Missing Skills ❌', 'Bonus Skills 💡']
    values = [len(matched), len(missing), len(extra)]
    colors = ['#00C851', '#FF4444', '#33B5E5']

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto',
            textfont={'size': 16, 'color': 'white'}
        )
    ])

    fig.update_layout(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#1a1a2e",
        font={'color': 'white'},
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis={'gridcolor': '#333'},
        yaxis={'gridcolor': '#333', 'title': 'Number of Skills'}
    )

    return fig


def create_skill_pie_chart(matched: list, missing: list, extra: list):
    """Create pie chart for skill distribution."""
    labels = ['Matched', 'Missing', 'Bonus']
    values = [len(matched), len(missing), len(extra)]
    colors = ['#00C851', '#FF4444', '#33B5E5']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textfont={'size': 14, 'color': 'white'}
    )])

    fig.update_layout(
        paper_bgcolor="#0e1117",
        font={'color': 'white'},
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        legend={'font': {'color': 'white'}}
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🎯 AI Resume Matcher")
    st.markdown("---")

    st.markdown("""
    ### How to Use:
    1. 📄 Upload your resume PDF
    2. 📋 Paste the job description
    3. 🚀 Click Analyze
    4. 📊 Review your results
    5. 💡 Apply suggestions

    ---
    ### What We Analyze:
    - ✅ Skill matching
    - 📊 Semantic similarity
    - 🎯 ATS compatibility
    - 💡 Improvement areas
    - 📚 Learning roadmap

    ---
    ### Tech Stack:
    - 🐍 Python
    - 🤗 Sentence Transformers
    - 🔬 spaCy NLP
    - 📈 Scikit-learn
    - 🎨 Streamlit + Plotly

    ---
    """)

    st.markdown("### ⚙️ Settings")
    show_raw_text = st.checkbox("Show extracted text", value=False)
    show_semantic = st.checkbox("Show semantic matches", value=True)
    min_similarity = st.slider(
        "Min semantic match threshold",
        min_value=50,
        max_value=90,
        value=60,
        step=5
    )


# ============================================================
# MAIN HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🎯 AI Resume & Job Description Matcher</h1>
    <p style="font-size: 1.1rem; opacity: 0.9;">
        Analyze your resume against any job description using AI.
        Get your ATS score, skill gaps, and personalized improvement tips.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT SECTION
# ============================================================
st.markdown('<div class="section-header">📥 Input Your Data</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📄 Upload Your Resume")
    uploaded_resume = st.file_uploader(
        label="Upload Resume PDF",
        type=["pdf"],
        help="Upload your resume in PDF format",
        label_visibility="collapsed"
    )

    if uploaded_resume:
        st.success(f"✅ Resume uploaded: **{uploaded_resume.name}**")
        file_size = len(uploaded_resume.getvalue()) / 1024
        st.caption(f"File size: {file_size:.1f} KB")

with col2:
    st.markdown("### 📋 Paste Job Description")
    job_description = st.text_area(
        label="Job Description",
        height=200,
        placeholder="""Paste the full job description here...

Example:
We are looking for a Machine Learning Engineer 
with experience in Python, TensorFlow, and NLP.
The candidate should have knowledge of RAG, 
LangChain, and vector databases like FAISS.
Strong SQL and data analysis skills required.
Experience with Docker and AWS is a plus.""",
        label_visibility="collapsed"
    )

    if job_description:
        word_count = len(job_description.split())
        st.caption(f"Word count: {word_count} words")

# ============================================================
# ANALYZE BUTTON
# ============================================================
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    analyze_button = st.button(
        "🚀 Analyze My Resume",
        type="primary",
        use_container_width=True
    )

st.markdown("---")


# ============================================================
# MAIN ANALYSIS LOGIC
# ============================================================
if analyze_button:

    # ---- Validation ----
    if not uploaded_resume:
        st.error("❌ Please upload your resume PDF first!")
        st.stop()

    if not job_description or len(job_description.strip()) < 50:
        st.error("❌ Please paste a job description (at least 50 characters)!")
        st.stop()

    # ---- Progress Bar ----
    progress_bar = st.progress(0)
    status_text = st.empty()

    # ---- Step 1: Extract Text ----
    status_text.text("📖 Step 1/5: Extracting text from your resume...")
    progress_bar.progress(10)
    time.sleep(0.3)

    resume_text = extract_text_from_pdf(uploaded_resume)

    if resume_text.startswith("ERROR"):
        st.error(f"❌ {resume_text}")
        st.stop()

    if len(resume_text) < 100:
        st.error("❌ Could not extract enough text from your PDF. "
                 "Make sure it's not a scanned image PDF.")
        st.stop()

    progress_bar.progress(25)

    # ---- Step 2: Extract Skills ----
    status_text.text("🔍 Step 2/5: Extracting skills using NLP...")
    time.sleep(0.3)

    resume_skills = extract_skills_with_spacy(resume_text)
    jd_skills = extract_skills_with_spacy(job_description)

    progress_bar.progress(45)

    # ---- Step 3: Calculate Scores ----
    status_text.text("🧮 Step 3/5: Calculating similarity scores with AI...")
    time.sleep(0.3)

    similarity_score = calculate_similarity_score(resume_text, job_description)
    skill_match_pct = calculate_skill_match_percentage(resume_skills, jd_skills)
    matched_skills = get_matched_skills(resume_skills, jd_skills)
    missing_skills = get_missing_skills(resume_skills, jd_skills)
    extra_skills = get_extra_skills(resume_skills, jd_skills)

    # Combined ATS score (weighted average)
    ats_score = (similarity_score * 0.4) + (skill_match_pct * 0.6)
    ats_score = round(ats_score, 2)

    progress_bar.progress(65)

    # ---- Step 4: Semantic Matches ----
    status_text.text("🤖 Step 4/5: Finding semantic skill relationships...")
    time.sleep(0.3)

    semantic_matches = get_semantic_skill_matches(resume_skills, jd_skills)

    progress_bar.progress(80)

    # ---- Step 5: Generate Suggestions ----
    status_text.text("💡 Step 5/5: Generating improvement suggestions...")
    time.sleep(0.3)

    suggestions = generate_improvement_suggestions(
        resume_text, job_description,
        matched_skills, missing_skills,
        similarity_score
    )
    learning_roadmap = get_learning_roadmap(missing_skills)

    progress_bar.progress(100)
    status_text.text("✅ Analysis Complete!")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

    # ============================================================
    # RESULTS SECTION
    # ============================================================
    st.success("🎉 Analysis Complete! Here are your results:")
    st.markdown("---")

    # ---- SCORE OVERVIEW ----
    st.markdown('<div class="section-header">📊 Your Scores</div>',
                unsafe_allow_html=True)

    grade, grade_desc, grade_color = get_overall_grade(ats_score)

    # Grade Banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {grade_color}22, {grade_color}44);
        border: 2px solid {grade_color};
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    ">
        <h1 style="color: {grade_color}; font-size: 3rem; margin: 0;">
            Grade: {grade}
        </h1>
        <h3 style="color: white; margin: 0.5rem 0;">{grade_desc}</h3>
        <p style="color: #aaa; margin: 0;">
            Overall ATS Score: <strong style="color: {grade_color};">
            {ats_score}%</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Gauge Charts
    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1:
        st.plotly_chart(
            create_gauge_chart(ats_score, "🎯 ATS Score"),
            use_container_width=True
        )
        st.caption("Combined score (60% skills + 40% semantic)")

    with col_g2:
        st.plotly_chart(
            create_gauge_chart(skill_match_pct, "🔧 Skill Match"),
            use_container_width=True
        )
        st.caption("% of required skills found in resume")

    with col_g3:
        st.plotly_chart(
            create_gauge_chart(similarity_score, "🧠 Semantic Score"),
            use_container_width=True
        )
        st.caption("AI-based content similarity score")

    # Metrics Row
    st.markdown("---")
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric("Total Resume Skills", len(resume_skills))
    with m2:
        st.metric("Total JD Skills", len(jd_skills))
    with m3:
        st.metric("✅ Matched", len(matched_skills), delta=f"+{len(matched_skills)}")
    with m4:
        st.metric("❌ Missing", len(missing_skills), delta=f"-{len(missing_skills)}",
                  delta_color="inverse")
    with m5:
        st.metric("💡 Bonus Skills", len(extra_skills))

    # Charts Row
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.plotly_chart(
            create_skills_bar_chart(matched_skills, missing_skills, extra_skills),
            use_container_width=True
        )

    with col_c2:
        st.plotly_chart(
            create_skill_pie_chart(matched_skills, missing_skills, extra_skills),
            use_container_width=True
        )

    # ---- SKILL ANALYSIS ----
    st.markdown("---")
    st.markdown('<div class="section-header">🔧 Skill Analysis</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "✅ Matched Skills",
        "❌ Missing Skills",
        "💡 Bonus Skills",
        "🤝 Semantic Matches"
    ])

    with tab1:
        st.markdown(f"### ✅ Skills Found in Both Resume & JD ({len(matched_skills)})")
        st.caption("These are your strengths for this role. Highlight them prominently.")
        if matched_skills:
            render_skill_badges(matched_skills, "skill-badge-green")

            # Show as table too
            st.markdown("---")
            matched_df = pd.DataFrame({
                "Skill": [s.title() for s in matched_skills],
                "Status": ["✅ Matched"] * len(matched_skills)
            })
            st.dataframe(matched_df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No exact skill matches found. "
                       "Consider adding more relevant skills.")

    with tab2:
        st.markdown(f"### ❌ Skills Required by JD But Missing in Resume ({len(missing_skills)})")
        st.caption("Focus on learning or adding these skills to improve your match score.")

        if missing_skills:
            render_skill_badges(missing_skills, "skill-badge-red")

            st.markdown("---")
            st.markdown("### 📚 Learning Roadmap for Missing Skills")

            if learning_roadmap:
                for skill, resource in learning_roadmap.items():
                    st.markdown(f"""
                     <div class="suggestion-card">
                     <strong style="color: #1a1a1a;">🎓 {skill.title()}</strong><br>
                        <small style="color: #333333;">{resource}</small>
                     </div>
    """, unsafe_allow_html=True)
            else:
                st.info("Add learning resources for your missing skills.")
        else:
            st.success("🎉 Amazing! You have all the required skills!")

    with tab3:
        st.markdown(f"### 💡 Your Bonus Skills Not in JD ({len(extra_skills)})")
        st.caption(
            "These are additional strengths. "
            "Mention them if relevant but don't let them distract."
        )

        if extra_skills:
            render_skill_badges(extra_skills, "skill-badge-blue")
        else:
            st.info("No additional skills beyond what's required.")

    with tab4:
        st.markdown("### 🤖 Semantically Similar Skills")
        st.caption(
            "Even without exact matches, these skills are conceptually related "
            "to what the JD requires."
        )

        if show_semantic and semantic_matches:
            sem_data = []
            for jd_skill, match_info in semantic_matches.items():
                if match_info["similarity"] >= min_similarity:
                    sem_data.append({
                        "JD Requires": jd_skill.title(),
                        "Your Similar Skill": match_info["similar_skill"].title(),
                        "Similarity": f"{match_info['similarity']}%"
                    })

            if sem_data:
                sem_df = pd.DataFrame(sem_data)
                st.dataframe(sem_df, use_container_width=True, hide_index=True)
            else:
                st.info(f"No semantic matches above {min_similarity}% threshold.")
        else:
            st.info("Enable 'Show semantic matches' in sidebar settings.")

    # ---- IMPROVEMENT SUGGESTIONS ----
    st.markdown("---")
    st.markdown('<div class="section-header">💡 Personalized Improvement Suggestions</div>',
                unsafe_allow_html=True)

    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
         st.markdown(f"""
        <div class="suggestion-card">
            <strong style="color: #1a1a1a; font-size: 1rem;">Tip #{i}</strong><br>
            <span style="color: #000000; font-size: 0.95rem;">{suggestion}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Your resume looks great for this role!")

    # ---- RESUME CATEGORIES ----
    st.markdown("---")
    st.markdown('<div class="section-header">📂 Your Skills by Category</div>',
                unsafe_allow_html=True)

    resume_categorized = categorize_skills(resume_skills)

    if resume_categorized:
        cat_col1, cat_col2 = st.columns(2)
        categories = list(resume_categorized.items())
        mid = len(categories) // 2

        for i, (category, skills) in enumerate(categories):
            col = cat_col1 if i < mid else cat_col2
            with col:
                with st.expander(f"📁 {category} ({len(skills)} skills)"):
                    render_skill_badges(skills, "skill-badge-blue")

    # ---- RAW TEXT (Optional) ----
    if show_raw_text:
        st.markdown("---")
        st.markdown('<div class="section-header">📝 Extracted Resume Text</div>',
                    unsafe_allow_html=True)

        with st.expander("View Extracted Resume Text"):
            st.text_area(
                "Resume Text",
                value=resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""),
                height=200,
                disabled=True,
                label_visibility="collapsed"
            )

    # ---- DOWNLOAD REPORT ----
    st.markdown("---")
    st.markdown('<div class="section-header">📥 Download Report</div>',
                unsafe_allow_html=True)

    report_content = f"""
AI RESUME MATCHER - ANALYSIS REPORT
=====================================
Generated by: AI Resume Matcher Tool

SCORES:
-------
Overall ATS Score    : {ats_score}%
Skill Match Score    : {skill_match_pct}%
Semantic Score       : {similarity_score}%
Grade                : {grade} - {grade_desc}

SKILL COUNTS:
-------------
Resume Skills Found  : {len(resume_skills)}
JD Skills Required   : {len(jd_skills)}
Matched Skills       : {len(matched_skills)}
Missing Skills       : {len(missing_skills)}
Bonus Skills         : {len(extra_skills)}

MATCHED SKILLS:
---------------
{', '.join([s.title() for s in matched_skills]) if matched_skills else 'None'}

MISSING SKILLS (Add These!):
-----------------------------
{', '.join([s.title() for s in missing_skills]) if missing_skills else 'None'}

IMPROVEMENT SUGGESTIONS:
------------------------
{chr(10).join([f'{i+1}. {s}' for i, s in enumerate(suggestions)])}

LEARNING ROADMAP:
-----------------
{chr(10).join([f'- {skill.title()}: {resource}' for skill, resource in learning_roadmap.items()])}
"""

    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        st.download_button(
            label="📥 Download Full Report (.txt)",
            data=report_content,
            file_name="resume_match_report.txt",
            mime="text/plain",
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎯 AI Resume Matcher | Built with Python, Streamlit, spaCy & Sentence Transformers</p>
    <p>🔒 100% Local Processing | No API Keys | No Data Stored | Privacy First</p>
</div>
""", unsafe_allow_html=True)