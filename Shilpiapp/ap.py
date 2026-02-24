import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import requests

import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import requests

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
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_5ngs2ksb.json"
lottie_animation = load_lottieurl(lottie_url)

# --- SIDEBAR ---
with st.sidebar:
    st_lottie(
        lottie_animation,
        height=250,
        key="avatar"
    )

# --- 1. SETUP ---
st.set_page_config(page_title="Shilpi AI", page_icon="💃")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# --- 2. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. UI & SIDEBAR ---
with st.sidebar:
    st_lottie(
        lottie_animation,
        height=250,
        key="avatar"
    )

    st.title("👩 Mom Teacher")
    st.write("Teaching with love and patience ❤️")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT INPUT ---
# --- CHAT INPUT ---
if prompt := st.chat_input("Ask Mom anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

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

        with st.chat_message("assistant"):
            st.markdown(output)

        st.session_state.messages.append(
            {"role": "assistant", "content": output}
        )

    except Exception as e:
        st.error(f"Error: {e}")