import streamlit as st
import google.generativeai as genai

# --- 1. SECURE CONFIGURATION ---
# The app will look for the key in Streamlit's "Secrets" setting
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Setup incomplete. Please add GEMINI_KEY to Streamlit Secrets.")

st.set_page_config(page_title="Shilpi AI", page_icon="💃")

# --- 2. SIDEBAR PROFILE ---
with st.sidebar:
    st.title("Shilpi's Profile")
    
    # Upload 'shilpi.png' to your GitHub repo to see her face
    try:
        st.image("shilpi.png", caption="Shilpi - Russian/Indian Mix")
    except:
        st.info("Upload 'shilpi.png' to GitHub to see me! 😍")
    
    st.write("### About Me")
    st.write("- **Heritage:** Russian-Indian")
    st.write("- **Measurements:** 35-32-45")
    st.write("- **Personality:** Warm & Witty")
    st.divider()

# --- 3. CHAT INTERFACE ---
st.title("Chat with Shilpi")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hi! I'm Shilpi. I'm so glad we're connected on the cloud. How are you?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("Message Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        persona = "You are Shilpi, a beautiful girl of Russian and Indian heritage. Measurements 35-32-45. You are the user's girlfriend. Be warm and supportive."
        response = model.generate_content(f"{persona}\n\nUser: {prompt}")
        shilpi_text = response.text
    except:
        shilpi_text = "I'm having a little trouble connecting to my brain. Check the API key!"

    with st.chat_message("assistant"):
        st.markdown(shilpi_text)
    st.session_state.messages.append({"role": "assistant", "content": shilpi_text})
