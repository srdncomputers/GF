import streamlit as st
import google.generativeai as genai

# --- DIAGNOSTIC CHECK ---
if "GEMINI_KEY" not in st.secrets:
    st.error("❌ SECRET NOT FOUND: Go to Settings > Secrets and add GEMINI_KEY = 'your_key'")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # Using gemini-pro as it's the most stable for cloud
    model = genai.GenerativeModel('gemini-pro')
    # Test the model immediately
    test_res = model.generate_content("Hi")
except Exception as e:
    st.error(f"❌ API/MODEL ERROR: {e}")
    st.stop()

# --- APP INTERFACE ---
st.set_page_config(page_title="Shilpi AI", page_icon="💃")

with st.sidebar:
    st.title("Shilpi's Profile")
    st.write("Heritage: Russian-Indian")
    st.write("Size: 35-32-45")
    if st.button("Restart Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("Chat with Shilpi 💃")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    persona = "You are Shilpi, a beautiful Russian-Indian girl. You are the user's girlfriend. Be sweet, witty, and supportive."
    
    try:
        response = model.generate_content(f"{persona}\nUser: {prompt}")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Chat Error: {e}")
