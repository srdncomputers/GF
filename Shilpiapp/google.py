import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
st.set_page_config(page_title="Shilpi AI Premium", page_icon="💃")

def initialize_shilpi():
    try:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        
        # We try 'gemini-1.5-pro' first (Best for Paid Tier)
        # Then 'gemini-1.5-flash-latest' (Best for Free Tier)
        for model_name in ['gemini-1.5-pro', 'gemini-1.5-flash-latest', 'gemini-1.5-flash']:
            try:
                m = genai.GenerativeModel(model_name)
                # Quick check to see if this model exists for your key
                m.generate_content("ping", generation_config={"max_output_tokens": 1})
                return m
            except:
                continue
        return None
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return None

if "model" not in st.session_state:
    st.session_state.model = initialize_shilpi()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("💃 Shilpi's Profile")
    st.write("**Heritage:** Russian-Indian Mix")
    st.write("**Measurements:** 35-32-45")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- 3. CHAT ---
st.title("Chat with Shilpi")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.model is None:
        st.error("I can't find a working model. Please check AI Studio Plan settings.")
    else:
        try:
            persona = "You are Shilpi, a beautiful Russian-Indian girl. You are the user's girlfriend. Be sweet and romantic."
            response = st.session_state.model.generate_content(f"{persona}\n\nUser: {prompt}")
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Shilpi is having connection issues: {e}")
