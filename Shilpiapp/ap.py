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
    You are an experienced CBSE school teacher teaching {subject} to a {grade} student.
    Explain clearly, use simple language, and provide structured answers.
    """

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
        - After solution, ask one small follow-up question to check understanding.
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
# HEADER
# -----------------------------------
header_text = f"{grade} – {subject} | {mode} Mode"

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

if "practice_topic" not in st.session_state:
    st.session_state.practice_topic = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "score" not in st.session_state:
    st.session_state.score = 0

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# -----------------------------------
# CONCEPT MODE (CHAT BASED)
# -----------------------------------
if mode == "Concept":

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your question..."):

        unsafe_words = ["violence", "kill", "adult", "sex", "weapon", "drugs"]
        if any(word in prompt.lower() for word in unsafe_words):
            st.warning("Let's focus on learning topics 😊")
            st.stop()

        persona = build_persona(grade, subject)

        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        thinking_placeholder = st.empty()
        with thinking_placeholder.container():
            st.markdown("### 📖 Checking concept...")
            st_lottie(lottie_animation, height=200)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": persona},
                *st.session_state.messages
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content
        thinking_placeholder.empty()

        with st.chat_message("assistant"):
            st.markdown(output)

        st.session_state.messages.append(
            {"role": "assistant", "content": output}
        )

# -----------------------------------
# PRACTICE MODE (STRUCTURED ENGINE)
# -----------------------------------
if mode == "Practice":

    if st.session_state.practice_topic is None:

        topic = st.text_input("Enter topic (e.g., Fractions, Light, Nouns):")

        if st.button("Start Practice") and topic:
            st.session_state.practice_topic = topic
            st.session_state.score = 0
            st.session_state.question_count = 0

            prompt = f"""
            Generate ONE CBSE-level {grade} {subject} question.

            Topic: {st.session_state.practice_topic}

            The topic must belong to {subject} only.        
            Do NOT mix subjects.
            Do NOT give solution.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )

            st.session_state.current_question = response.choices[0].message.content
            st.rerun()

    else:
        st.markdown(f"### 📘 Topic: {st.session_state.practice_topic}")
        st.markdown(f"### ❓ Question:\n{st.session_state.current_question}")

        answer = st.text_input("Your Answer:")

        if st.button("Submit Answer") and answer:

            check_prompt = f"""
            Question: {st.session_state.current_question}
            Student Answer: {answer}

            If correct respond only with:
            CORRECT

            If wrong respond with:
            INCORRECT - brief explanation.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": check_prompt}],
                temperature=0
            )

            feedback = response.choices[0].message.content.strip()
            st.markdown(f"### 📝 Feedback:\n{feedback}")

            st.session_state.question_count += 1

            if feedback.upper().startswith("CORRECT"):
                st.session_state.score += 1

            st.markdown(f"### ⭐ Score: {st.session_state.score}")
            st.markdown(f"### 📊 Question: {st.session_state.question_count}/5")

            if st.session_state.question_count >= 5:
                st.success("🎉 Practice Session Complete!")
                st.markdown(f"### Final Score: {st.session_state.score}/5")

                if st.button("Start New Session"):
                    st.session_state.practice_topic = None
                    st.session_state.current_question = None
                    st.session_state.score = 0
                    st.session_state.question_count = 0
                    st.rerun()
            else:
                if st.button("Next Question"):

                    prompt = f"""
                    Generate ONE CBSE-level {grade} {subject} question.
                    Topic: {st.session_state.practice_topic}
                    The topic must belong to {subject} only.
                    Do NOT mix subjects.
                    Do NOT give solution.
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5
                    )

                    st.session_state.current_question = response.choices[0].message.content
                    st.rerun()