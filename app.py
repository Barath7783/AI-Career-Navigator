import os
import re
import sqlite3
import hashlib
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai

# ============================================================
# AI CAREER NAVIGATOR - STARTUP MVP
# ============================================================

st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🧭",
    layout="wide"
)

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=API_KEY)

DB_NAME = "career_navigator.db"

# ============================================================
# DATABASE
# ============================================================

def init_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            education TEXT,
            skills TEXT,
            interests TEXT,
            experience TEXT,
            career_goal TEXT,
            career_level TEXT,
            career_domain TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            report TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            skill TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


init_database()

# ============================================================
# PASSWORD
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================================
# USER ACCOUNT
# ============================================================

def create_user(name, email, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                hash_password(password),
                datetime.now().isoformat()
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(email, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM users
        WHERE email = ? AND password = ?
        """,
        (
            email,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# SAVE PROFILE
# ============================================================

def save_profile(
    user_id,
    education,
    skills,
    interests,
    experience,
    career_goal,
    career_level,
    career_domain
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM profiles WHERE user_id = ?",
        (user_id,)
    )

    cursor.execute(
        """
        INSERT INTO profiles
        (
            user_id,
            education,
            skills,
            interests,
            experience,
            career_goal,
            career_level,
            career_domain
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            education,
            skills,
            interests,
            experience,
            career_goal,
            career_level,
            career_domain
        )
    )

    conn.commit()
    conn.close()


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(user_id, report):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports
        (user_id, report, created_at)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            report,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
        background: linear-gradient(
            90deg,
            #ff4b4b,
            #a855f7,
            #3b82f6
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        color: #00d9ff;
    }

    .description {
        text-align: center;
        font-size: 19px;
        color: #d1d5db;
        margin-bottom: 30px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 15px;
        background: #171923;
        border: 1px solid #30323d;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        padding: 30px;
        font-size: 17px;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# ============================================================
# 👥 GUEST ACCOUNT
# ============================================================

if "guest_mode" not in st.session_state:
    st.session_state.guest_mode = False

if st.sidebar.button("👥 Guest Account", use_container_width=True):
    st.session_state.guest_mode = True
    st.session_state.user_name = "Guest User"
    st.session_state.user_email = "guest@aicareernavigator.app"
    st.rerun()

if st.session_state.guest_mode:

    st.sidebar.success("👥 Guest Account")

    st.sidebar.write("Welcome, Guest User")

    st.sidebar.caption(
        "Guest mode allows you to explore AI Career Navigator "
        "without creating an account."
    )

    if st.sidebar.button("🚪 Exit Guest Account", use_container_width=True):
        st.session_state.guest_mode = False
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.rerun()

# ============================================================
# LOGIN / SIGNUP
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">AI CAREER NAVIGATOR</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">'
        'Your AI-Powered Career Planning Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with tab1:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.user_name = user[1]

                st.success("✅ Login successful!")

                st.rerun()

            else:

                st.error(
                    "❌ Invalid email or password."
                )

    # --------------------------------------------------------
    # SIGN UP
    # --------------------------------------------------------

    with tab2:

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
            "🚀 Create Account",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill all fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                created = create_user(
                    name,
                    email,
                    password
                )

                if created:

                    st.success(
                        "✅ Account created. Please login."
                    )

                else:

                    st.error(
                        "❌ Email already exists."
                    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("AI Career Navigator")

st.sidebar.success(
    f"Welcome, {st.session_state.user_name}"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Career Profile",
        "🤖 AI Career Assessment",
        "📄 Resume & ATS",
        "💼 Job Matching",
        "📚 Learning Roadmap",
        "🎤 Interview Preparation",
        "📈 Progress Tracking",
        "💳 Subscription"
    ]
)
st.sidebar.divider()

st.sidebar.markdown("### 🔗 Connect with Me")

st.sidebar.markdown(
    """
    <a href="https://www.linkedin.com/in/barath2005/"
       target="_blank"
       style="
       text-decoration:none;
       font-size:18px;
       font-weight:600;
       ">
       💼 LinkedIn
    </a>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = ""

    st.rerun()




# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">AI CAREER NAVIGATOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">'
    'Navigate Your Career. Build Your Future.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header("🚀 Career Dashboard")

    st.write(
        f"Welcome **{st.session_state.user_name}**."
    )

    st.markdown(
        """
        <div class="feature-card">

        ### 🎯 AI Career Assessment

        Analyze your education, skills, experience
        and career goals.

        </div>

        <div class="feature-card">

        ### 📄 Resume + ATS Analysis

        Upload your resume and analyze its
        compatibility with a target job.

        </div>

        <div class="feature-card">

        ### 💼 Job Matching

        Match your skills with suitable
        technology career roles.

        </div>

        <div class="feature-card">

        ### 📚 Personalized Learning

        Generate a learning roadmap based
        on your skill gaps.

        </div>

        <div class="feature-card">

        ### 🎤 Interview Preparation

        Generate technical and HR interview
        questions for your target role.

        </div>

        <div class="feature-card">

        ### 📈 Career Progress

        Track your skills and learning progress.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CAREER PROFILE
# ============================================================

elif page == "👤 Career Profile":

    st.header("👤 Your Career Profile")

    col1, col2 = st.columns(2)

    with col1:

        education = st.text_area(
            "Education",
            placeholder="""BCA - AI & Data Science
MCA - Generative AI"""
        )

        skills = st.text_area(
            "Current Skills",
            placeholder="""Python
SQL
Machine Learning
Generative AI
Streamlit"""
        )

        interests = st.text_area(
            "Career Interests",
            placeholder="Artificial Intelligence, GenAI"
        )

    with col2:

        experience = st.text_area(
            "Projects / Internship",
            placeholder="""AI Resume Scoring Web App
Vehicle Detection using YOLO
AI/ML Internship"""
        )

        career_goal = st.text_input(
            "Career Goal",
            placeholder="AI Engineer"
        )

        career_level = st.selectbox(
            "Career Level",
            [
                "Student",
                "Fresher",
                "Entry-Level Professional",
                "1-2 Years Experience",
                "3+ Years Experience"
            ]
        )

        career_domain = st.selectbox(
            "Preferred Domain",
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
                "Natural Language Processing"
            ]
        )

    if st.button(
        "💾 Save Career Profile",
        type="primary",
        use_container_width=True
    ):

        save_profile(
            st.session_state.user_id,
            education,
            skills,
            interests,
            experience,
            career_goal,
            career_level,
            career_domain
        )

        st.success(
            "✅ Career profile saved successfully."
        )


# ============================================================
# AI CAREER ASSESSMENT
# ============================================================

elif page == "🤖 AI Career Assessment":

    st.header("🤖 AI Career Assessment")

    education = st.text_area(
        "Education"
    )

    skills = st.text_area(
        "Current Skills"
    )

    interests = st.text_area(
        "Interests"
    )

    experience = st.text_area(
        "Projects / Experience"
    )

    career_goal = st.text_input(
        "Career Goal"
    )

    if st.button(
        "🚀 Generate AI Career Plan",
        type="primary",
        use_container_width=True
    ):

        if not education or not skills or not career_goal:

            st.warning(
                "Please enter education, skills and career goal."
            )

            st.stop()

        prompt = f"""
You are an expert AI Career Advisor.

Candidate:
{st.session_state.user_name}

Education:
{education}

Skills:
{skills}

Interests:
{interests}

Experience:
{experience}

Career Goal:
{career_goal}

Create a professional career assessment.

Include:

1. Career readiness
2. Strengths
3. Recommended career roles
4. Skill gap analysis
5. Technical roadmap
6. 6-month roadmap
7. Project recommendations
8. Resume recommendations
9. Interview preparation
10. Job search strategy
11. 1-year roadmap
12. 3-year roadmap
13. 5-year roadmap
14. Final recommendation

Make the advice practical and realistic.
"""

        with st.spinner(
            "🤖 AI is creating your career plan..."
        ):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                result = response.text

                save_report(
                    st.session_state.user_id,
                    result
                )

                st.success(
                    "✅ Career report generated!"
                )

                st.markdown(result)

                st.download_button(
                    "📥 Download Career Report",
                    result,
                    "AI_Career_Navigator_Report.txt",
                    "text/plain"
                )

            except Exception as e:

                st.error(
                    "❌ Error generating report."
                )

                st.exception(e)


# ============================================================
# RESUME ATS
# ============================================================

elif page == "📄 Resume & ATS":

    st.header("📄 Resume Upload + ATS Analysis")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "txt", "docx"]
    )

    target_job = st.text_input(
        "Target Job Role",
        placeholder="Example: AI Engineer"
    )

    if uploaded_file:

        st.success(
            f"✅ Resume uploaded: {uploaded_file.name}"
        )

    if st.button(
        "📊 Analyze Resume",
        type="primary",
        use_container_width=True
    ):

        if not uploaded_file:

            st.warning(
                "Please upload your resume."
            )

            st.stop()

        resume_text = ""

        # TXT
        if uploaded_file.name.endswith(".txt"):

            resume_text = (
                uploaded_file
                .read()
                .decode("utf-8", errors="ignore")
            )

        # PDF
        elif uploaded_file.name.endswith(".pdf"):

            try:

                from PyPDF2 import PdfReader

                reader = PdfReader(
                    uploaded_file
                )

                for page_pdf in reader.pages:

                    text = page_pdf.extract_text()

                    if text:
                        resume_text += text

            except Exception:

                st.error(
                    "Install PyPDF2 to read PDF files."
                )

                st.stop()

        # DOCX
        elif uploaded_file.name.endswith(".docx"):

            try:

                from docx import Document

                document = Document(
                    uploaded_file
                )

                resume_text = "\n".join(
                    paragraph.text
                    for paragraph in document.paragraphs
                )

            except Exception:

                st.error(
                    "Install python-docx to read DOCX files."
                )

                st.stop()

        prompt = f"""
You are an ATS Resume Expert.

Target Job:
{target_job}

Resume:
{resume_text}

Analyze the resume.

Give:

1. ATS Score out of 100
2. Technical skills found
3. Missing skills
4. Keyword recommendations
5. Project improvements
6. Experience improvements
7. Education improvements
8. Formatting recommendations
9. Resume summary recommendation
10. Final ATS improvement plan
"""

        with st.spinner(
            "📄 Analyzing resume..."
        ):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            ats_result = response.text

        st.markdown(ats_result)


# ============================================================
# JOB MATCHING
# ============================================================

elif page == "💼 Job Matching":

    st.header("💼 AI Job Matching")

    skills = st.text_input(
        "Your Skills",
        placeholder="Python, SQL, Machine Learning, GenAI"
    )

    job_role = st.text_input(
        "Target Role",
        placeholder="AI Engineer"
    )

    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here..."
    )

    if st.button(
        "🎯 Match My Profile",
        type="primary",
        use_container_width=True
    ):

        prompt = f"""
You are an AI recruitment specialist.

Candidate skills:
{skills}

Target role:
{job_role}

Job description:
{job_description}

Analyze the match.

Return:

1. Match percentage
2. Matching skills
3. Missing skills
4. Recommended skills
5. Resume keywords
6. Interview preparation
7. Overall recommendation
"""

        with st.spinner(
            "💼 Matching your profile..."
        ):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            st.markdown(
                response.text
            )


# ============================================================
# LEARNING ROADMAP
# ============================================================

elif page == "📚 Learning Roadmap":

    st.header("📚 Personalized Learning Roadmap")

    target_role = st.text_input(
        "Target Career",
        placeholder="AI Engineer"
    )

    current_skills = st.text_area(
        "Current Skills",
        placeholder="Python, SQL, ML"
    )

    if st.button(
        "📚 Generate Learning Roadmap",
        type="primary",
        use_container_width=True
    ):

        prompt = f"""
Create a personalized learning roadmap.

Target career:
{target_role}

Current skills:
{current_skills}

Create:

Month 1:
Month 2:
Month 3:
Month 4:
Month 5:
Month 6:

For every month include:

- Topics
- Technologies
- Practice
- Project
- Expected outcome
"""

        with st.spinner(
            "📚 Creating roadmap..."
        ):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            st.markdown(
                response.text
            )


# ============================================================
# INTERVIEW PREPARATION
# ============================================================

elif page == "🎤 Interview Preparation":

    st.header("🎤 AI Interview Preparation")

    role = st.text_input(
        "Target Job Role",
        placeholder="AI Engineer"
    )

    level = st.selectbox(
        "Interview Level",
        [
            "Fresher",
            "Entry Level",
            "Intermediate",
            "Experienced"
        ]
    )

    if st.button(
        "🎤 Generate Interview Questions",
        type="primary",
        use_container_width=True
    ):

        prompt = f"""
You are an expert technical interviewer.

Job Role:
{role}

Level:
{level}

Generate:

1. 10 technical questions
2. 10 Python/coding questions
3. 10 AI/ML questions
4. 10 Generative AI questions
5. 5 project questions
6. 5 HR questions
7. Model answers and preparation tips
"""

        with st.spinner(
            "🎤 Preparing interview questions..."
        ):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            st.markdown(
                response.text
            )


# ============================================================
# PROGRESS TRACKING
# ============================================================

elif page == "📈 Progress Tracking":

    st.header("📈 Career Progress Tracking")

    skill = st.text_input(
        "Skill",
        placeholder="Python"
    )

    status = st.selectbox(
        "Status",
        [
            "Not Started",
            "Learning",
            "Practicing",
            "Completed"
        ]
    )

    if st.button(
        "➕ Add Skill"
    ):

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO progress
            (user_id, skill, status)
            VALUES (?, ?, ?)
            """,
            (
                st.session_state.user_id,
                skill,
                status
            )
        )

        conn.commit()
        conn.close()

        st.success(
            "✅ Skill added."
        )

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill, status
        FROM progress
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    progress_data = cursor.fetchall()

    conn.close()

    if progress_data:

        st.subheader("Your Skills")

        for skill_name, skill_status in progress_data:

            if skill_status == "Completed":

                st.success(
                    f"✅ {skill_name} — {skill_status}"
                )

            elif skill_status == "Learning":

                st.info(
                    f"📚 {skill_name} — {skill_status}"
                )

            else:

                st.write(
                    f"🔹 {skill_name} — {skill_status}"
                )


# ============================================================
# SUBSCRIPTION
# ============================================================

elif page == "💳 Subscription":

    st.header("💳 AI Career Navigator Plans")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("🆓 Free")

        st.write("₹0 / month")

        st.write("✓ Basic Career Assessment")
        st.write("✓ Basic Roadmap")
        st.write("✓ Basic Skill Analysis")

        st.button(
            "Current Plan",
            key="free_plan"
        )

    with col2:

        st.subheader("⭐ Pro")

        st.write("₹199 / month")

        st.write("✓ Advanced AI Assessment")
        st.write("✓ Resume ATS Analysis")
        st.write("✓ Job Matching")
        st.write("✓ Interview Preparation")
        st.write("✓ Personalized Roadmap")
        st.write("✓ Progress Tracking")

        st.button(
            "Choose Pro",
            key="pro_plan"
        )

    with col3:

        st.subheader("🏢 College")

        st.write("Contact for pricing")

        st.write("✓ Student Dashboard")
        st.write("✓ Placement Analytics")
        st.write("✓ Career Assessment")
        st.write("✓ Resume Analysis")
        st.write("✓ Interview Preparation")
        st.write("✓ Admin Dashboard")

        st.button(
            "Contact Us",
            key="college_plan"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        © 2026 Barath. All Rights Reserved.
    </div>
    """,
    unsafe_allow_html=True
)
