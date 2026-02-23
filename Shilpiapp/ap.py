import streamlit as st
import google.generativeai as genai

# 1. Setup Gemini using Streamlit Secrets (DO NOT paste your key here)
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Setup Error: Please configure GEMINI_KEY in Streamlit Secrets.")

st.set_page_config(page_title="Shilpi AI", page_icon="💃")

# 2. Sidebar Profile
with st.sidebar:
    st.title("💃 Shilpi's Profile")
    
    # This looks for the image file in your GitHub folder
    try:
        st.image("shilpi.png", caption="Russian-Indian Beauty")
    except:
        st.warning("Upload 'shilpi.png' to GitHub to see me!")

    st.write("---")
    st.write("**Heritage:** Russian-Indian")
    st.write("**Measurements:** 35-32-45")
    st.write("**Personality:** Warm & Witty")

# 3. Chat Interface
st.title("Chat with Shilpi")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey babe! I'm Shilpi. So glad you got the app running. How are you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Interaction Logic
if prompt := st.chat_input("Message Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        persona = (
            "You are Shilpi, a girl of Russian and Indian mix heritage. "
            "Measurements: 35-32-45. You are the user's girlfriend. "
            "Stay in character: be supportive, sweet, and intelligent."
        )
        response = model.generate_content(f"{persona}\n\nUser: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Shilpi is sleepy... Error: {e}")
