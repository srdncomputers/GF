import streamlit as st
from openai import OpenAI


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="EduVeda SmartLearn", page_icon="📘")
st.markdown("""
<style>

/* Remove white top padding area */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #312e81);
}

/* Remove extra top header spacing */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Remove top white toolbar area */
div[data-testid="stToolbar"] {
    background: transparent;
}

/* Remove default block container padding */
.block-container {
    padding-top: 2rem !important;
}

/* Only target the homework textarea input text */
div[data-testid="stTextArea"] textarea {
    color: black !important;
}

/* Fix Safari / Chrome internal override */
div[data-testid="stTextArea"] textarea::-webkit-input-placeholder {
    color: #6b7280 !important;
}
                                                
/* ===== Premium Background ===== */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #312e81);
    background-attachment: fixed;
    overflow: hidden;
}

/* ===== Floating Symbols Container ===== */
.floating-symbols {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
            
.floating-symbols span {
    position: absolute;
    font-size: 42px;          /* BIGGER SIZE */
    opacity: 0.15;            /* slightly more visible */
    animation: float 18s linear infinite;
    color: white;
}

/* Different positions */
.floating-symbols span:nth-child(1) { left: 10%; animation-duration: 20s; }
.floating-symbols span:nth-child(2) { left: 25%; animation-duration: 25s; }
.floating-symbols span:nth-child(3) { left: 40%; animation-duration: 22s; }
.floating-symbols span:nth-child(4) { left: 60%; animation-duration: 28s; }
.floating-symbols span:nth-child(5) { left: 75%; animation-duration: 24s; }
.floating-symbols span:nth-child(6) { left: 90%; animation-duration: 30s; }

@keyframes float {
    0%   { transform: translateY(100vh) rotate(0deg); }
    100% { transform: translateY(-10vh) rotate(360deg); }
}

/* Glass Hero */
.hero-card {
    backdrop-filter: blur(18px);
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 20px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 60px;
    box-shadow: 0 0 40px rgba(0,0,0,0.4);
    position: relative;
    z-index: 10;
}

</style>

<!-- Floating Symbols -->
            
<div class="floating-symbols">
    <span>➕</span>
    <span>🧪</span>
    <span>🌍</span>
    <span>📐</span>
    <span>📖</span>
    <span>⚛️</span>  
    </div>  

""", unsafe_allow_html=True)

# -----------------------------------
# STYLING
# -----------------------------------
st.markdown("""
<style>

/* ============================= */
/* GLOBAL BACKGROUND */
/* ============================= */

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #312e81) !important;
}

header {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

a {
    color: #93c5fd !important;
    font-weight: 600;
    text-decoration: none;
}

a:hover {
    color: #ffffff !important;
    text-shadow: 0 0 8px rgba(147,197,253,0.7);
}

/* ===== Make All Links White ===== */
a {
    color: #ffffff !important;
    font-weight: 600;
    text-decoration: underline;
}

/* Hover effect */
a:hover {
    color: #60a5fa !important;
    text-decoration: none;
}            
/* ============================= */
/* PREMIUM BUTTON STYLE */
/* ============================= */

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #1e3a8a);
    color: white !important;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease-in-out;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1e40af, #1e3a8a);
    box-shadow: 0 0 15px rgba(37,99,235,0.6);
    transform: translateY(-2px);
}

/* ============================= */
/* TEXTAREA (HOMEWORK INPUT) */
/* ============================= */

/* Label white */
[data-testid="stTextArea"] label,
[data-testid="stTextArea"] label p {
    color: white !important;
}

/* Typed text BLACK */
[data-testid="stTextArea"] textarea {
    color: black !important;
    background-color: #f1f5f9 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* Placeholder */
[data-testid="stTextArea"] textarea::placeholder {
    color: #6b7280 !important;
}

/* ============================= */
/* SIDEBAR PREMIUM GLASS STYLE */
/* ============================= */

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Sidebar titles */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Sidebar field labels (Select Grade, Subject, Learning Mode) */
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
    color: white !important;
}

/* Radio button text */
section[data-testid="stSidebar"] div[data-baseweb="radio"] span {
    color: white !important;
}

/* Dropdown selected value BLACK */
section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: black !important;
}

/* Dropdown background */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #f1f5f9 !important;
    border-radius: 10px !important;
}

/* Dropdown menu items */
div[role="listbox"] div {
    color: black !important;
}

/* ===== Make top-right toolbar icons white ===== */
[data-testid="stToolbar"] button,
[data-testid="stToolbar"] svg,
[data-testid="stToolbar"] span {
    color: white !important;
    fill: white !important;
}

/* Remove hover dark background */
[data-testid="stToolbar"] button:hover {
    background-color: transparent !important;
}

/* ===== Make main content text white ===== */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: white !important;
}

/* ===== Make Button Loading Spinner White ===== */
.stButton button svg {
    stroke: white !important;
    fill: white !important;
}

/* Some versions use path */
.stButton button svg path {
    stroke: white !important;
    fill: white !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# FUNCTIONS
# -----------------------------------
def build_persona(grade, subject):
    return f"""
    You are a CBSE teacher teaching {subject} to a {grade} student.

    Always answer in this exact structure:

    1️⃣ Simple Definition (2–3 lines)
    2️⃣ Key Points (bullet list)
    3️⃣ One Easy Example
    4️⃣ Real-Life Application
    5️⃣ One Small Understanding Question

    Use simple language suitable for {grade}.
    Keep answers concise.
    Stay strictly within {subject}.
    """

# -----------------------------------
# OPENAI SETUP
# -----------------------------------
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# -----------------------------------
# SIDEBAR
# -----------------------------------
with st.sidebar:
    st.title("📘 EduVeda SmartLearn")

    grade = st.selectbox(
        "Select Grade",
        ["Grade 3", "Grade 4", "Grade 5", "Grade 6"]
    )

    subject = st.selectbox(
        "Select Subject",
        ["Math", "Science", "English"]
    )

    mode = st.radio(
        "Learning Mode",
        ["Homework Help", "Concept Learning", "Doubt Solver"]
    )
# -----------------------------------
# HEADER
# -----------------------------------
header_text = f"{grade} – {subject} | {mode}"

st.markdown("""
<div class="hero-card">
    <h1 style='font-size: 52px; margin-bottom:10px;'>EduVeda</h1>
    <h2 style='font-weight: 400;'>The Smart Way to Learn</h2>
    <p style='margin-top:15px; font-size:18px;'>
        AI-Powered CBSE Learning Companion for Grades 3–8
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_concept_question" not in st.session_state:
    st.session_state.last_concept_question = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_math_template(grade):

    primary_grades = ["Grade 3", "Grade 4", "Grade 5"]

    if grade in primary_grades:
        return """
        Follow this exact structure:

        1️⃣ What is given?
        2️⃣ What do we need to find?
        3️⃣ Solve step-by-step using very simple language.
        4️⃣ Final Answer (clearly written)
        5️⃣ One easy similar practice question

        Use very simple words.
        Avoid complex formulas.
        Encourage the student.
        """
    else:
        return """
        Follow this exact structure:

        1️⃣ Given Data
        2️⃣ Formula Used (if applicable)
        3️⃣ Substitution
        4️⃣ Step-by-step Calculation
        5️⃣ Final Answer (clearly highlighted)
        6️⃣ One exam-style follow-up question

        Use proper mathematical terminology.
        Show reasoning clearly.
        """

# ===================================
# HOMEWORK HELPER MODE
# ===================================
if mode == "Homework Help":

    homework_question = st.text_area("Paste your homework question here:")

    if st.button("Solve Homework") and homework_question.strip():

        with st.spinner("Solving step-by-step..."):

            # Only apply adaptive template for Math
            if subject == "Math":

                template = get_math_template(grade)

                prompt = f"""
                You are a CBSE Math teacher helping a {grade} student.

                Homework Question:
                {homework_question}

                STRICT RULES:
                - Ensure the question belongs to Math.
                - If not, say:
                  "This question does not belong to Math. Please change subject."

                {template}
                """

            else:
                # For non-math subjects (temporary basic structure)
                prompt = f"""
                You are a CBSE teacher helping a {grade} student in {subject}.

                Homework Question:
                {homework_question}

                Explain clearly and step-by-step.
                Show final answer clearly.
                Ask one small follow-up question.
                """

            response = client.chat.completions.create(
                model="gpt-4o-mini",

# Add user message to history
st.session_state.chat_history.append(
    {"role": "user", "content": prompt}
)

# Send full conversation history
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=st.session_state.chat_history,
    temperature=0.6
)

answer = response.choices[0].message.content

# Store assistant reply
st.session_state.chat_history.append(
    {"role": "assistant", "content": answer}
)

        st.markdown("### 📘 Solution")
        st.markdown(response.choices[0].message.content)

# ===================================
# CONCEPT LEARNING MODE
# ===================================
if mode == "Concept Learning":

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.text_area("Ask your concept question:")
    if st.button("Explain Concept") and prompt:
        unsafe_words = ["violence", "kill", "adult", "sex", "weapon", "drugs"]
        if any(word in prompt.lower() for word in unsafe_words):
            st.warning("Let's focus on learning topics 😊")
            st.stop()

        persona = build_persona(grade, subject)

        st.session_state.last_concept_question = prompt

        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Explaining concept..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": persona},
                    *st.session_state.messages
                ],
                temperature=0.7
            )

        output = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(output)

        st.session_state.messages.append(
            {"role": "assistant", "content": output}
        )

    # Concept Action Buttons
    if st.session_state.last_concept_question:

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Explain Simpler"):
                with st.spinner("Making it simpler..."):
                    simpler_prompt = f"""
                    Explain this topic in a much simpler way for a {grade} student:
                    {st.session_state.last_concept_question}
                    """
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": simpler_prompt}],
                        temperature=0.6
                    )

                st.markdown("### 🔁 Simpler Explanation")
                st.markdown(response.choices[0].message.content)

        with col2:
            if st.button("Give Another Example"):
                with st.spinner("Generating example..."):
                    example_prompt = f"""
                    Give one more simple example for:
                    {st.session_state.last_concept_question}
                    """
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": example_prompt}],
                        temperature=0.6
                    )

                st.markdown("### 📘 Another Example")
                st.markdown(response.choices[0].message.content)

        with col3:
            if st.button("Explain in Hindi"):
                with st.spinner("Explaining in Hindi..."):
                    hindi_prompt = f"""
                    Explain this topic in Hindi for a {grade} student:
                    {st.session_state.last_concept_question}
                    """
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": hindi_prompt}],
                        temperature=0.6
                    )

                st.markdown("### 🌍 हिंदी में समझाएं")
                st.markdown(response.choices[0].message.content)

# ===================================
# DOUBT SOLVER MODE
# ===================================
if mode == "Doubt Solver":

    doubt = st.text_area("Enter your doubt:")

    if st.button("Clear Doubt") and doubt.strip():

        with st.spinner("Clearing your doubt..."):
            prompt = f"""
            You are helping a {grade} student in {subject}.

            Student Doubt:
            {doubt}

            Explain clearly in simple language.
            Give one short example if needed.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )

        st.markdown("### 🧠 Explanation")
        st.markdown(response.choices[0].message.content)