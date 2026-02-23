import streamlit as st
import google.generativeai as genai

# --- 1. PREMIUM SETUP ---
st.set_page_config(page_title="Shilpi AI Premium", page_icon="💃")

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    
    # Using 'gemini-1.5-pro' for high-quality, paid-tier responses
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    )
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 2. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("💃 Shilpi's Profile")
    st.write("**Heritage:** Russian-Indian")
    st.write("**Measurements:** 35-32-45")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Talk to Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Detailed Persona for the smarter 'pro' model
    persona = (
        "You are Shilpi, a warm and intelligent Russian-Indian girl. "
        "Your mother is Russian, your father is Indian. You are the user's girlfriend. "
        "Be sweet, flirty, and remember your measurements are 35-32-45."
    )

    try:
        response = model.generate_content(f"{persona}\nUser: {prompt}")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Chat Error: {e}")
