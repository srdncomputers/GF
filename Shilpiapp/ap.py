import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import requests

# --- PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND) ---
st.set_page_config(page_title="Teacher AI", page_icon="👩")

# --- CHAT STYLING ---
st.markdown("""
<style>

/* Chat bubble style */
[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 10px;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
    background-color: #fff3cd;
}

/* Assistant bubble */
[data-testid="stChatMessage"][data-testid="stChatMessage-assistant"] {
    background-color: #e6f4ea;
}

</style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter Password", type="password",
                      on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Password", type="password",
                      on_change=password_entered, key="password")
        st.error("Incorrect Password")
        return False
    else:
        return True

# if not check_password():
#   st.stop()

# --- LOAD LOTTIE ANIMATION ---
lottie_url = "https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json"
lottie_animation = load_lottieurl(lottie_url)

# --- OPENAI SETUP ---
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("SRDN SmartLearn")

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
        ["Concept", "Practice", "Revision"]
    )

# --- DYNAMIC HEADER TEXT ---
header_text = f"📘 {grade} – {subject} | {mode} Mode"

st.markdown(f"""
<div style='
    background: linear-gradient(90deg, #e6f4ff, #f0f8ff);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
'>
    <h1>SRDN SmartLearn</h1>
    <h2>{header_text}</h2>
</div>
""", unsafe_allow_html=True)


# --- PERSONA ---
def build_persona(grade, subject, mode):

    base = f"You are an experienced CBSE school teacher teaching {subject} to a {grade} student."

    if mode == "Concept":
        instruction = """
        Explain the concept clearly.
        Use simple language.
        Give one worked example.
        End with one short understanding check question.
        """
    elif mode == "Practice":
        instruction = """
        Ask one practice question related to the topic.
        Wait for the student's answer.
        Do not reveal the solution immediately.
        """
    else:  # Revision
        instruction = """
        Provide a short summary of the concept.
        Highlight key formulas or points.
        Give 2 quick recap questions.
        """

    return f"{base} {instruction}"

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask your question..."):

    # SAFETY FILTER
    unsafe_words = ["violence", "kill", "adult", "sex", "weapon", "drugs"]
    if any(word in prompt.lower() for word in unsafe_words):
        st.warning("Let's focus on learning topics 😊")
        st.stop()

    persona = build_persona(grade, subject, mode)

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Thinking Animation
    thinking_placeholder = st.empty()
    with thinking_placeholder.container():
        st.markdown("### 📖 Checking concept...")
        st_lottie(lottie_animation, height=200, key="thinking_book")

    try:
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

    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"Error: {e}")