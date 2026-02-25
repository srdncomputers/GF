import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import requests

# --- PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND) ---
st.set_page_config(page_title="Mom Teacher AI", page_icon="👩")

st.markdown("""
<style>
/* Soft classroom background */
.stApp {
    background-color: #fdf6ec;
}

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

if not check_password():
    st.stop()

# --- LOAD LOTTIE ANIMATION ---
lottie_url = "https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json"
lottie_animation = load_lottieurl(lottie_url)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📚 Smart Learning Book")

    age_group = st.selectbox(
        "Select Age Group",
        ["1-4", "5-8", "9-12", "13-16"]
    )

    subject = st.selectbox(
        "Select Subject",
        ["General", "Math", "Science", "English", "Stories", "GK"]
    )

    mode = st.radio(
        "Learning Mode",
        ["Teach", "Quiz", "Story"]
    )

# --- PERSONA ---
def build_persona(age_group, subject, mode):
    base = "You are a loving, patient mother teaching a child."
    if age_group == "1-4":
        style = "Use very short sentences, simple words, emojis, and repetition."
    elif age_group == "5-8":
        style = "Explain in simple language with small examples."
    elif age_group == "9-12":
        style = "Explain clearly step-by-step and encourage thinking."
    else:
        style = "Explain concepts clearly and give structured answers."

    if mode == "Quiz":
        mode_instruction = "Ask questions and wait for the child to answer."
    elif mode == "Story":
        mode_instruction = "Tell a short engaging story related to the topic."
    else:
        mode_instruction = "Teach the concept clearly."

    return f"{base} Subject: {subject}. {style} {mode_instruction}"
"""

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask Mom anything..."):
    
persona = build_persona(age_group, subject, mode)
response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": persona},
            *st.session_state.messages
            
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Beautiful thinking block
    thinking_placeholder = st.empty()

    with thinking_placeholder.container():
        st.markdown("### 📖 Let me check in my book...")
        st_lottie(lottie_animation, height=220, key="thinking_book")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": persona},
                *st.session_state.messages
            ],
            temperature=0.8
        )

        output = response.choices[0].message.content

        thinking_placeholder.empty()  # remove animation

        with st.chat_message("assistant"):
            st.markdown(output)

        st.session_state.messages.append(
            {"role": "assistant", "content": output}
        )

    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"Error: {e}")