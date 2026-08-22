import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Check API key
if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

# Gemini
client = genai.Client(api_key=api_key)

# Page settings
st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 AI Career Navigator")
st.subheader("Navigate Your Career. Build Your Future.")

st.write(
    "AI-powered career guidance, skill-gap analysis "
    "and personalized career roadmap."
)

st.divider()

# Sidebar
st.sidebar.header("👤 Your Profile")

name = st.sidebar.text_input(
    "Your Name"
)

education = st.sidebar.text_input(
    "Education",
    placeholder="Example: MCA Generative AI"
)

skills = st.sidebar.text_area(
    "Your Skills",
    placeholder="Python, SQL, Machine Learning"
)

interests = st.sidebar.text_area(
    "Your Interests",
    placeholder="Generative AI, NLP, Computer Vision"
)

target_role = st.sidebar.text_input(
    "Target Job",
    placeholder="Example: AI Engineer"
)

experience = st.sidebar.selectbox(
    "Experience",
    [
        "Student",
        "Fresher",
        "0-2 Years",
        "2-5 Years"
    ]
)

# Button
analyze = st.sidebar.button(
    "🚀 Analyze My Career"
)

# Home screen
if not analyze:

    st.info(
        "👈 Enter your details on the left and "
        "click **Analyze My Career**."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎯 Career",
            "AI Powered"
        )

    with col2:
        st.metric(
            "🧠 Skill Analysis",
            "Gemini"
        )

    with col3:
        st.metric(
            "🗺️ Roadmap",
            "Personalized"
        )

# Analyze
else:

    if not name or not education or not skills or not target_role:

        st.warning(
            "Please enter Name, Education, Skills "
            "and Target Job."
        )

        st.stop()

    # Prompt for Gemini
    prompt = f"""
You are an expert AI career advisor.

Candidate information:

Name: {name}

Education:
{education}

Experience:
{experience}

Current Skills:
{skills}

Interests:
{interests}

Target Job:
{target_role}

Create a personalized career plan.

Give the answer using these sections:

1. Career Assessment
2. Career Match Percentage
3. Current Strengths
4. Skill Gaps
5. Skills to Learn
6. 6-Month Career Roadmap
7. Recommended Projects
8. Certifications
9. Interview Preparation
10. Job Application Strategy
11. Suitable Job Roles
12. Final Career Advice

Give practical and specific advice.
"""

    # Gemini response
    with st.spinner("🤖 Gemini is analyzing your career..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            result = response.text

        except Exception as e:

            st.error(f"Gemini Error: {e}")
            st.stop()

    # Results
    st.success("✅ Career analysis completed!")

    st.divider()

    st.header("🎯 Your Career Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Target Job",
            target_role
        )

    with col2:
        st.metric(
            "Experience",
            experience
        )

    with col3:
        st.metric(
            "AI Engine",
            "Gemini"
        )

    st.divider()

    st.header("🧠 AI Career Analysis")

    st.markdown(result)

    # Download
    st.download_button(
        label="📥 Download Career Report",
        data=result,
        file_name="AI_Career_Navigator_Report.txt",
        mime="text/plain"
    )