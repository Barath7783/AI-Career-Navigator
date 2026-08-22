import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ============================================================
# AI CAREER NAVIGATOR
# ============================================================

# Page configuration
st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🧭",
    layout="wide"
)

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "❌ Gemini API key not found. "
        "Please add GEMINI_API_KEY to your .env file."
    )
    st.stop()

# Initialize Gemini
client = genai.Client(api_key=api_key)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<h1 style='text-align: center;'>🧭 AI Career Navigator</h1>",
    unsafe_allow_html=True
)

st.subheader("Navigate Your Career. Build Your Future.")


st.markdown(
    """
    **AI Career Navigator** analyzes your education, skills, interests
    and career goals to create a personalized career roadmap.
    """
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
# PREFERRED CAREER DOMAIN
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
# GENERATE CAREER REPORT
# ============================================================

generate_report = st.button(
    "🧭 Generate My AI Career Plan",
    type="primary",
    use_container_width=True
)


if generate_report:

    # Validate inputs
    if not education.strip():
        st.warning("⚠️ Please enter your education details.")
        st.stop()

    if not skills.strip():
        st.warning("⚠️ Please enter your current skills.")
        st.stop()

    if not career_goal.strip():
        st.warning("⚠️ Please enter your career goal.")
        st.stop()

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are an expert AI Career Advisor and Technology Career Strategist.

Create a detailed but practical career plan based on the following
candidate profile.

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

The report must contain the following sections:

1. Career Assessment
   - Current profile
   - Career readiness
   - Strengths

2. Recommended Career Roles
   - Recommend 5 suitable job roles
   - Explain why each role is suitable
   - Give an approximate difficulty level

3. Skill Gap Analysis
   - Existing skills
   - Missing skills
   - Priority of each missing skill

4. Technical Skills Roadmap
   - Programming
   - AI/ML
   - Generative AI
   - Frameworks
   - Databases
   - Cloud
   - Deployment
   - Git/GitHub

5. 6-Month Learning Roadmap
   Month 1
   Month 2
   Month 3
   Month 4
   Month 5
   Month 6

6. Project Recommendations
   - Beginner project
   - Intermediate project
   - Advanced project
   - One strong portfolio project

7. Resume Recommendations
   - Skills to highlight
   - Projects to highlight
   - Certifications
   - ATS recommendations

8. Interview Preparation
   - Technical topics
   - Coding topics
   - AI/ML questions
   - HR questions

9. Job Search Strategy
   - Suitable job titles
   - Types of companies
   - LinkedIn strategy
   - GitHub strategy
   - Portfolio strategy

10. Long-Term Career Roadmap
   - 1 year
   - 3 years
   - 5 years

11. Final Recommendation
   Give a clear conclusion about the candidate's best career direction.

Keep the advice realistic, practical and suitable for the candidate's
current experience level.

Use clear headings and bullet points.
"""


    # ========================================================
    # CALL GEMINI
    # ========================================================

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


    # ========================================================
    # DISPLAY REPORT
    # ========================================================

    st.divider()

    st.header("📊 Your AI Career Navigation Report")

    st.markdown(result)


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

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

st.caption(
    "🧭 AI Career Navigator | Built with Python, Streamlit and Google Gemini"
)
st.markdown(
    "<p style='text-align:center;'>© 2026 Barath. All Rights Reserved.</p>",
    unsafe_allow_html=True
)
