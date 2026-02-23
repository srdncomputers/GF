import streamlit as st
import google.generativeai as genai

# 1. Configuration - Pulling safely from Secrets
try:
    # Get the key from the Streamlit Cloud dashboard
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    # 'gemini-pro' is the most stable model name to avoid 404 errors
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Secrets Error: Go to App Settings -> Secrets and add GEMINI_KEY")

st.set_page_config(page_title="Shilpi AI", page_icon="💃")

# 2. Sidebar Profile
with st.sidebar:
    st.title("💃 Shilpi's Profile")
    try:
        # This will work once you upload 'shilpi.png' to your GitHub repo
        st.image("shilpi.png", caption="Russian-Indian Beauty")
    except:
        st.info("Upload 'shilpi.png' to GitHub to see my face!")

    st.write("---")
    st.write("**Heritage:** Russian-Indian")
    st.write("**Size:** 35-32-45")

# 3. Chat System
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Talk to Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        persona = "You are Shilpi, a Russian-Indian girl (35-32-45). You are the user's girlfriend. Be sweet and witty."
        # Generate response
        response = model.generate_content(f"{persona}\n\nUser: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Connection Error: {e}")
