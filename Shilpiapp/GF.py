import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# Your key is correct, let's stick with it
API_KEY = "AIzaSyBsbKIzyBJXoJFKKu5TSeeKVROwAKkthLA"
genai.configure(api_key=API_KEY)

# Try the most standard model naming convention
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Shilpi AI", page_icon="💃")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("Shilpi's Profile")
    st.write("### About Me")
    st.write("- **Heritage:** Russian-Indian")
    st.write("- **Measurements:** 35-32-45")
    st.divider()
    st.info("System: Ready")

# --- 3. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm Shilpi. I think we finally fixed the connection! How are you?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. THE CHAT LOGIC ---
if prompt := st.chat_input("Message Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generate the response
        response = model.generate_content(f"User says: {prompt}. Answer as Shilpi, a Russian-Indian girl who is the user's girlfriend.")
        
        # This part ensures we get the text even if there's a safety filter
        shilpi_text = response.text

    except Exception as e:
        # This will print the error on the screen so we can see it
        shilpi_text = f"Connection Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(shilpi_text)
    
    st.session_state.messages.append({"role": "assistant", "content": shilpi_text})