import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import requests

import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import requests

# -----------------------------------
# PAGE CONFIG (MUST BE FIRST)
# -----------------------------------
st.set_page_config(page_title="SRDN SmartLearn", page_icon="📘")

# -----------------------------------
# CHAT STYLING
# -----------------------------------
st.markdown("""
<style>
[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 10px;
}
[data-testid="stChatMessage-user"] {
    background-color: #fff3cd;
}
[data-testid="stChatMessage-assistant"] {
    background-color: #e6f4ea;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# FUNCTIONS
# -----------------------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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
    Keep answers concise but clear.
    Stay strictly within {subject}.
    """

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Explain Simpler"):
        # regenerate with simpler instruction

with col2:
    if st.button("Give Another Example"):
        # regenerate example only

with col3:
    if st.button("Explain in Hindi"):
        # regenerate in Hindi

# -----------------------------------
# LOAD ANIMATION
# -----------------------------------
lottie_url = "https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json"
lottie_animation = load_lottieurl(lottie_url)

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
    st.title("📘 SRDN SmartLearn")

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

st.markdown(f"""
<div style='
    background: linear-gradient(90deg, #e6f4ff, #f0f8ff);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
'>
    <h1>SRDN SmartLearn</h1>
    <h3>{header_text}</h3>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION STATE INIT
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------
# HOMEWORK HELPER MODE
# -----------------------------------
if mode == "Homework Help":

    homework_question = st.text_area("Paste your homework question here:")

    if st.button("Solve Homework") and homework_question:

        thinking_placeholder = st.empty()

        with thinking_placeholder.container():
            st.markdown("### 📖 Solving step-by-step...")
            st_lottie(lottie_animation, height=200)

        prompt = f"""
        You are a CBSE teacher helping a {grade} student in {subject}.

        Homework Question:
        {homework_question}

        STRICT RULES:
        - Explain step-by-step.
        - Show formulas used.
        - Use simple language.
        - Clearly show final answer at end.
        - After solution, ask one small follow-up question.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        output = response.choices[0].message.content

        thinking_placeholder.empty()

        st.markdown("### 📘 Solution")
        st.markdown(output)

# -----------------------------------
# CONCEPT LEARNING MODE
# -----------------------------------
# -----------------------------------
# CONCEPT ACTION BUTTONS
# -----------------------------------

if "last_concept_question" in st.session_state:

    col1, col2, col3 = st.columns(3)

    # Explain Simpler
    with col1:
        if st.button("Explain Simpler"):
            simpler_prompt = f"""
            Explain this topic in an even simpler way for a {grade} student.

            Topic:
            {st.session_state.last_concept_question}

            Use very short sentences and easy examples.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": simpler_prompt}],
                temperature=0.6
            )

            st.markdown("### 🔁 Simpler Explanation")
            st.markdown(response.choices[0].message.content)

    # Another Example
    with col2:
        if st.button("Give Another Example"):
            example_prompt = f"""
            Give one more simple example for this topic:

            {st.session_state.last_concept_question}

            Keep it short and easy for {grade}.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": example_prompt}],
                temperature=0.6
            )

            st.markdown("### 📘 Another Example")
            st.markdown(response.choices[0].message.content)

    # Hindi Explanation
    with col3:
        if st.button("Explain in Hindi"):
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

# -----------------------------------
# DOUBT SOLVER MODE
# -----------------------------------
if mode == "Doubt Solver":

    doubt = st.text_area("Enter your doubt:")

    if st.button("Clear Doubt") and doubt:

        prompt = f"""
        You are helping a {grade} student in {subject}.

        Student Doubt:
        {doubt}

        Explain clearly and simply.
        If needed, give a small example.
        Keep explanation short and clear.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        output = response.choices[0].message.content

        st.markdown("### 🧠 Explanation")
        st.markdown(output)