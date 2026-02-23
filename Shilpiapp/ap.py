import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="Shilpi AI", page_icon="💃")

# This function finds a model that actually works on your account
def get_working_model():
    try:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # We check these 3 names in order of most likely to work
        for model_name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(model_name)
                m.generate_content("Hi") # Test it
                return m
            except:
                continue
        return None
    except Exception as err:
        st.error(f"Secret Key Error: {err}")
        return None

# Initialize the model
if "model" not in st.session_state:
    st.session_state.model = get_working_model()

# 2. SIDEBAR
with st.sidebar:
    st.title("Shilpi's Profile")
    st.write("Heritage: Russian-Indian")
    st.write("Measurements: 35-32-45")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 3. CHAT LOGIC
st.title("Chat with Shilpi 💃")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.model is None:
        st.error("I couldn't connect to Google AI. Please check your API key in Secrets.")
    else:
        try:
            persona = "You are Shilpi, a Russian-Indian girl. You are the user's girlfriend. Be sweet."
            response = st.session_state.model.generate_content(f"{persona}\nUser: {prompt}")
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Chat Error: {e}")
