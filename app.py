import os
import sqlite3
import hashlib
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# SESSION STATE INITIALIZATION
# IMPORTANT: THIS MUST COME BEFORE logged_in IS USED
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ============================================================
# DATABASE
# ============================================================

DB_FILE = "career_navigator.db"


def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
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
            career_level TEXT
        )
    """)

    conn.commit()
    conn.close()


init_database()

# ============================================================
# PASSWORD HASH
# ============================================================


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# CREATE USER
# ============================================================


def create_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hash_password(password)
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ============================================================
# LOGIN USER
# ============================================================


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE email = ?
        AND password = ?
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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 5px;
        background: linear-gradient(
            90deg,
            #ff4b91,
            #8b5cf6,
            #3b82f6
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }

    .footer {
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        color: #888888;
        border-top: 1px solid #333333;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================


def show_header():

    st.markdown(
        """
        <div class="main-title">
            🚀 AI CAREER NAVIGATOR
        </div>

        <div class="subtitle">
            Your AI-Powered Career Planning Assistant
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOGIN / CREATE ACCOUNT PAGE
# ============================================================


def authentication_page():

    show_header()

    st.markdown("---")

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account"
        ]
    )

    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.subheader("🔐 Login to Your Account")

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

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            else:

                user = login_user(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.session_state.user_email = user[2]

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid email or password."
                    )

    # ========================================================
    # CREATE ACCOUNT
    # ========================================================

    with register_tab:

        st.subheader("📝 Create Your Account")

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm"
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill in all fields."
                )

            elif password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "❌ Password must contain at least 6 characters."
                )

            else:

                created = create_user(
                    name,
                    email,
                    password
                )

                if created:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "Please go to the Login tab and login."
                    )

                else:

                    st.error(
                        "❌ This email is already registered."
                    )


# ============================================================
# SIDEBAR
# ============================================================


def show_sidebar():

    st.sidebar.title("🎯 Career Navigator")

    st.sidebar.success(
        f"👋 {st.session_state.user_name}"
    )

    st.sidebar.caption(
        st.session_state.user_email
    )

    st.sidebar.divider()

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
            "📊 Progress Tracking",
            "💳 Subscription"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.session_state.user_email = ""

        st.rerun()

    return page


# ============================================================
# DASHBOARD
# ============================================================


def dashboard():

    st.header("🚀 Career Dashboard")

    st.success(
        f"Welcome, {st.session_state.user_name}!"
    )

    st.write(
        "Build your career with personalized AI guidance."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎯 AI Career Assessment")

        st.write(
            "Analyze your skills, education, interests "
            "and career goals."
        )

    with col2:

        st.subheader("📄 Resume + ATS")

        st.write(
            "Improve your resume for your target job."
        )

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("💼 Job Matching")

        st.write(
            "Find suitable job roles based on your profile."
        )

    with col4:

        st.subheader("📚 Learning Roadmap")

        st.write(
            "Get a personalized learning path."
        )


# ============================================================
# CAREER PROFILE
# ============================================================


def career_profile():

    st.header("👤 Your Career Profile")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Full Name",
            value=st.session_state.user_name
        )

        education = st.text_area(
            "Education",
            placeholder=(
                "Example:\n"
                "BCA - Artificial Intelligence & Data Science\n"
                "MCA - Generative Artificial Intelligence"
            )
        )

        skills = st.text_area(
            "Current Skills",
            placeholder=(
                "Python, Java, SQL, Machine Learning, "
                "Deep Learning, Generative AI"
            )
        )

    with col2:

        interests = st.text_area(
            "Career Interests",
            placeholder=(
                "Artificial Intelligence, "
                "Machine Learning, Generative AI"
            )
        )

        experience = st.text_area(
            "Projects / Internship Experience",
            placeholder=(
                "AI Resume Scoring Web App\n"
                "Vehicle Detection using YOLO\n"
                "AI/ML Internship"
            )
        )

        career_goal = st.text_input(
            "Career Goal",
            placeholder="Example: AI Engineer"
        )

    career_level = st.selectbox(
        "Current Career Level",
        [
            "Student",
            "Fresher",
            "Entry-Level Professional",
            "1-2 Years Experience",
            "3+ Years Experience"
        ]
    )

    if st.button(
        "💾 Save Career Profile",
        use_container_width=True
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM profiles
            WHERE user_id = ?
            """,
            (st.session_state.user_id,)
        )

        cursor.execute(
            """
            INSERT INTO profiles(
                user_id,
                education,
                skills,
                interests,
                experience,
                career_goal,
                career_level
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                st.session_state.user_id,
                education,
                skills,
                interests,
                experience,
                career_goal,
                career_level
            )
        )

        conn.commit()
        conn.close()

        st.success(
            "✅ Career profile saved successfully!"
        )


# ============================================================
# AI CAREER ASSESSMENT
# ============================================================


def ai_career_assessment():

    st.header("🤖 AI Career Assessment")

    education = st.text_area(
        "Education",
        placeholder="Enter your education"
    )

    skills = st.text_area(
        "Current Skills",
        placeholder="Python, SQL, AI, ML..."
    )

    interests = st.text_area(
        "Career Interests",
        placeholder="AI, ML, GenAI..."
    )

    experience = st.text_area(
        "Projects / Internship",
        placeholder="Enter your experience"
    )

    career_goal = st.text_input(
        "Career Goal",
        placeholder="Example: AI Engineer"
    )

    if st.button(
        "🚀 Generate AI Career Plan",
        use_container_width=True
    ):

        if not education or not skills or not career_goal:

            st.warning(
                "Please enter Education, Skills and Career Goal."
            )

        else:

            prompt = f"""
You are an expert AI Career Advisor.

Candidate Education:
{education}

Current Skills:
{skills}

Career Interests:
{interests}

Projects and Internship:
{experience}

Career Goal:
{career_goal}

Create a personalized AI Career Navigation Report.

Include:

1. Career Assessment
2. Recommended Career Roles
3. Skill Gap Analysis
4. Technical Skills Roadmap
5. 6-Month Learning Roadmap
6. Project Recommendations
7. Resume Recommendations
8. Interview Preparation
9. Job Search Strategy
10. 1-Year Career Roadmap
11. 3-Year Career Roadmap
12. 5-Year Career Roadmap
13. Final Recommendation

Keep the advice practical and realistic.
"""

            api_key = os.getenv(
                "GEMINI_API_KEY"
            )

            if not api_key:

                st.error(
                    "❌ GEMINI_API_KEY is not configured."
                )

            else:

                try:

                    from google import genai

                    client = genai.Client(
                        api_key=api_key
                    )

                    response = client.models.generate_content(
                        model=os.getenv(
                            "GEMINI_MODEL",
                            "gemini-3.6-flash"
                        ),
                        contents=prompt
                    )

                    if response.text:

                        st.divider()

                        st.subheader(
                            "📊 Your AI Career Report"
                        )

                        st.markdown(
                            response.text
                        )

                        st.download_button(
                            "📥 Download Career Report",
                            response.text,
                            file_name=(
                                "AI_Career_Navigator_Report.txt"
                            ),
                            mime="text/plain"
                        )

                except Exception as e:

                    st.error(
                        "❌ Gemini API Error"
                    )

                    st.exception(e)


# ============================================================
# RESUME ATS
# ============================================================


def resume_ats():

    st.header("📄 Resume + ATS Analysis")

    resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "txt"]
    )

    target_role = st.text_input(
        "Target Job Role",
        placeholder="Example: AI Engineer"
    )

    if st.button(
        "📊 Analyze Resume",
        use_container_width=True
    ):

        if not resume:

            st.warning(
                "Please upload your resume."
            )

        else:

            st.success(
                f"Resume uploaded: {resume.name}"
            )

            st.info(
                "Resume analysis module is ready."
            )


# ============================================================
# JOB MATCHING
# ============================================================


def job_matching():

    st.header("💼 Job Matching")

    skills = st.text_area(
        "Your Skills",
        placeholder="Python, SQL, Machine Learning..."
    )

    target_role = st.text_input(
        "Target Job Role",
        placeholder="AI Engineer"
    )

    location = st.text_input(
        "Preferred Location",
        placeholder="Chennai / Bangalore / Remote"
    )

    if st.button(
        "🔎 Find Suitable Jobs",
        use_container_width=True
    ):

        if skills and target_role:

            st.success(
                "Job matching analysis completed."
            )

            st.write(
                f"Target Role: **{target_role}**"
            )

            st.write(
                f"Preferred Location: **{location}**"
            )

        else:

            st.warning(
                "Please enter your skills and target role."
            )


# ============================================================
# LEARNING ROADMAP
# ============================================================


def learning_roadmap():

    st.header("📚 Learning Roadmap")

    goal = st.text_input(
        "Target Career",
        placeholder="AI Engineer"
    )

    duration = st.selectbox(
        "Duration",
        [
            "3 Months",
            "6 Months",
            "12 Months"
        ]
    )

    if st.button(
        "📚 Generate Roadmap",
        use_container_width=True
    ):

        if not goal:

            st.warning(
                "Please enter your target career."
            )

        else:

            st.success(
                f"{duration} roadmap created for {goal}."
            )

            st.write("### Month 1")
            st.write("Programming and fundamentals")

            st.write("### Month 2")
            st.write("Machine Learning")

            st.write("### Month 3")
            st.write("Deep Learning")

            st.write("### Month 4")
            st.write("Generative AI")

            st.write("### Month 5")
            st.write("Projects and deployment")

            st.write("### Month 6")
            st.write("Resume and interview preparation")


# ============================================================
# INTERVIEW PREPARATION
# ============================================================


def interview_preparation():

    st.header("🎤 Interview Preparation")

    role = st.text_input(
        "Target Job Role",
        placeholder="AI Engineer"
    )

    if st.button(
        "🎤 Generate Interview Questions",
        use_container_width=True
    ):

        if role:

            st.success(
                f"Interview preparation created for {role}."
            )

            st.write("### Technical Questions")

            st.write(
                "• Explain supervised and unsupervised learning.\n"
                "• What is overfitting?\n"
                "• Explain CNN.\n"
                "• What is a Transformer?\n"
                "• What is RAG?"
            )

            st.write("### HR Questions")

            st.write(
                "• Tell me about yourself.\n"
                "• Why should we hire you?\n"
                "• What are your career goals?"
            )

        else:

            st.warning(
                "Please enter your target role."
            )


# ============================================================
# PROGRESS TRACKING
# ============================================================


def progress_tracking():

    st.header("📊 Career Progress Tracking")

    tasks = [
        "Learn Python",
        "Learn SQL",
        "Learn Machine Learning",
        "Learn Deep Learning",
        "Learn Generative AI",
        "Build AI Project",
        "Build GenAI Project",
        "Complete Resume",
        "Practice Coding",
        "Practice Interviews"
    ]

    completed = 0

    for i, task in enumerate(tasks):

        if st.checkbox(
            task,
            key=f"task_{i}"
        ):

            completed += 1

    progress = completed / len(tasks)

    st.progress(
        progress
    )

    st.metric(
        "Career Preparation",
        f"{int(progress * 100)}%"
    )


# ============================================================
# SUBSCRIPTION
# ============================================================


def subscription():

    st.header("💳 Subscription")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🆓 Free")

        st.write("₹0 / month")

        st.write("✓ Basic Career Assessment")
        st.write("✓ Basic Learning Roadmap")
        st.write("✓ Basic Interview Preparation")

        st.button(
            "Current Plan",
            disabled=True,
            use_container_width=True
        )

    with col2:

        st.subheader("⭐ Pro")

        st.write("₹199 / month")

        st.write("✓ Advanced AI Career Assessment")
        st.write("✓ Resume ATS Analysis")
        st.write("✓ Job Matching")
        st.write("✓ Personalized Roadmap")
        st.write("✓ Interview Preparation")
        st.write("✓ Progress Tracking")

        if st.button(
            "⭐ Choose Pro",
            use_container_width=True
        ):

            st.info(
                "Payment gateway can be connected here."
            )


# ============================================================
# FOOTER
# ============================================================


def show_footer():

    st.markdown(
        """
        <div class="footer">
            © 2026 Barath. All Rights Reserved.<br>
            🚀 AI Career Navigator
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

if not st.session_state.logged_in:

    authentication_page()

else:

    page = show_sidebar()

    show_header()

    if page == "🏠 Dashboard":

        dashboard()

    elif page == "👤 Career Profile":

        career_profile()

    elif page == "🤖 AI Career Assessment":

        ai_career_assessment()

    elif page == "📄 Resume & ATS":

        resume_ats()

    elif page == "💼 Job Matching":

        job_matching()

    elif page == "📚 Learning Roadmap":

        learning_roadmap()

    elif page == "🎤 Interview Preparation":

        interview_preparation()

    elif page == "📊 Progress Tracking":

        progress_tracking()

    elif page == "💳 Subscription":

        subscription()

    show_footer()
