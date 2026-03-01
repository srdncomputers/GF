import streamlit as st
from openai import OpenAI

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="SRDN SmartLearn", page_icon="📘")

# -----------------------------------
# STYLING
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
     background: linear-gradient(90deg, #0f172a, #1e3a8a);
    padding: 50px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 40px;
'>
    <h1 style='font-size: 48px; margin-bottom:10px;'>EduVeda</h1>
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
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
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

    if prompt := st.chat_input("Ask your concept question..."):

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