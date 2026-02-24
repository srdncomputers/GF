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
lottie_url = "https://app.lottiefiles.com/animation/a3ea3aac-6a92-4149-8997-547c4991e314"
lottie_animation = load_lottieurl(lottie_url)

# --- SIDEBAR ---
with st.sidebar:
    st_lottie(lottie_animation, height=250, key="avatar")
    st.title("👩 Mom Teacher")
    st.write("Teaching with love and patience ❤️")

# --- OPENAI SETUP ---
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# --- PERSONA ---
persona = """
You are a loving, patient mother teaching her child.
Explain concepts in simple language.
Use small examples.
Encourage curiosity.
Be kind and supportive.
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