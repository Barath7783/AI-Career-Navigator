import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ============================================================
# AI CAREER NAVIGATOR
# ============================================================

st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API key not found. Please add GEMINI_API_KEY to your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div style="text-align:center; padding:20px 0;">

        <h1 style="
            font-size:48px;
            font-weight:800;
            margin:0;
            background:linear-gradient(90deg,#ff4b4b,#a855f7,#3b82f6);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        ">
            🚀 AI CAREER NAVIGATOR 🧭
        </h1>

        <h2 style="
            color:#00d9ff;
            font-size:28px;
            font-weight:700;
            margin:10px 0;
        ">
            REVERSE 2026
        </h2>

        <p style="
            font-size:22px;
            color:#d1d5db;
            margin-top:10px;
        ">
            Your AI-Powered Career Planning Assistant
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:16px;
        color:#b8c0cc;
        margin-bottom:25px;
    ">
        AI Career Navigator analyzes your education, skills,
        interests and career goals to create a personalized career roadmap.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎯 Career Navigator")

st.sidebar.info(
    """
    Enter your profile information and let AI create
    a personalized career plan.
    """
)

st.sidebar.markdown("### Features")

st.sidebar.markdown(
    """
    - 🎓 Education Analysis
    - 💻 Skill Analysis
    - 🤖 AI Career Recommendations
    - 📚 Learning Roadmap
    - 💼 Job Role Suggestions
    - 📈 Skill Gap Analysis
    - 🚀 Future Career Plan
    """
)

# ============================================================
# USER INPUT
# ============================================================

st.header("👤 Your Career Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Full Name",
        placeholder="Example: Barath G"
    )

    education = st.text_area(
        "Education",
        placeholder=(
            "Example:\n"
            "BCA - Artificial Intelligence & Data Science\n"
            "MCA - Generative Artificial Intelligence"
        ),
        height=120
    )

    skills = st.text_area(
        "Current Skills",
        placeholder=(
            "Example: Python, Java, SQL, Machine Learning, "
            "Deep Learning, Generative AI, Streamlit"
        ),
        height=120
    )

with col2:

    interests = st.text_area(
        "Career Interests",
        placeholder=(
            "Example: Artificial Intelligence, "
            "Generative AI, Machine Learning, Data Science"
        ),
        height=120
    )

    experience = st.text_area(
        "Projects / Internship Experience",
        placeholder=(
            "Example:\n"
            "AI Resume Scoring Web App\n"
            "Vehicle Detection using YOLO\n"
            "Python AI/ML Internship"
        ),
        height=120
    )

    career_goal = st.text_input(
        "Career Goal",
        placeholder="Example: AI Engineer"
    )

# ============================================================
# EXPERIENCE LEVEL
# ============================================================

experience_level = st.selectbox(
    "Current Career Level",
    [
        "Student",
        "Fresher",
        "Entry-Level Professional",
        "1-2 Years Experience",
        "3+ Years Experience"
    ]
)

# ============================================================
# CAREER DOMAIN
# ============================================================

career_domain = st.selectbox(
    "Preferred Career Domain",
    [
        "Artificial Intelligence",
        "Machine Learning",
        "Generative AI",
        "Data Science",
        "Data Engineering",
        "Software Development",
        "Cloud Computing",
        "Cybersecurity",
        "Computer Vision",
        "Natural Language Processing",
        "Not Sure"
    ]
)

# ============================================================
# GENERATE REPORT
# ============================================================

generate_report = st.button(
    "🚀 Generate My AI Career Plan",
    type="primary",
    use_container_width=True
)

if generate_report:

    if not education.strip():
        st.warning("⚠️ Please enter your education details.")
        st.stop()

    if not skills.strip():
        st.warning("⚠️ Please enter your current skills.")
        st.stop()

    if not career_goal.strip():
        st.warning("⚠️ Please enter your career goal.")
        st.stop()

    prompt = f"""
You are an expert AI Career Advisor and Technology Career Strategist.

Create a detailed but practical career plan based on the following candidate profile.

Candidate Name:
{name}

Education:
{education}

Current Skills:
{skills}

Interests:
{interests}

Projects / Internship Experience:
{experience}

Career Goal:
{career_goal}

Experience Level:
{experience_level}

Preferred Career Domain:
{career_domain}

Generate a professional AI Career Navigation Report.

The report must contain:

1. Career Assessment
2. Recommended Career Roles
3. Skill Gap Analysis
4. Technical Skills Roadmap
5. 6-Month Learning Roadmap
6. Project Recommendations
7. Resume Recommendations
8. Interview Preparation
9. Job Search Strategy
10. Long-Term Career Roadmap
11. Final Recommendation

Keep the advice realistic, practical and suitable for the candidate's
current experience level.

Use clear headings and bullet points.
"""

    with st.spinner("🤖 AI is analyzing your career profile..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            result = response.text

        except Exception as e:

            st.error("❌ Error while generating the career report.")
            st.exception(e)
            st.stop()

    st.divider()

    st.header("📊 Your AI Career Navigation Report")

    st.markdown(result)

    st.divider()

    st.subheader("📥 Download Your Report")

    st.download_button(
        label="📥 Download Career Report",
        data=result,
        file_name="AI_Career_Navigator_Report.txt",
        mime="text/plain"
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px 0;
        font-size:18px;
        color:white;
    ">
        © 2026 Barath. All Rights Reserved.
    </div>
    """,
    unsafe_allow_html=True
)
