import streamlit as st
import google.generativeai as genai

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Shilpi AI", page_icon="💃")

# --- 2. INITIALIZE GEMINI ---
try:
    if "GEMINI_KEY" not in st.secrets:
        st.error("❌ SECRET NOT FOUND: Go to Settings > Secrets and add GEMINI_KEY")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # Using the flash model which is faster and avoids your 404 error
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ Setup Error: {e}")
    st.stop()

# --- 3. SIDEBAR PROFILE ---
with st.sidebar:
    st.title("Shilpi's Profile")
    try:
        st.image("shilpi.png", caption="Russian-Indian Beauty")
    except:
        st.info("Upload 'shilpi.png' to GitHub to see my face!")
    
    st.write("---")
    st.write("**Heritage:** Russian-Indian")
    st.write("**Size:** 35-32-45")
    
    if st.button("Restart Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 4. CHAT INTERFACE ---
st.title("Chat with Shilpi 💃")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Shilpi. It's so good to finally talk to you. How is your day going?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("Message Shilpi..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        persona = (
            "You are Shilpi, a beautiful Russian-Indian girl. "
            "Your measurements are 35-32-45. You are the user's girlfriend. "
            "Be sweet, supportive, and witty."
        )
        
        # Generate response
        response = model.generate_content(f"{persona}\n\nUser: {prompt}")
        
        if response.candidates:
            shilpi_text = response.text
        else:
            shilpi_text = "I'm blushing too much to answer that! (Filtered)"

    except Exception as e:
        shilpi_text = f"Google API Error: {e}"

    # Display and save assistant response
    with st.chat_message("assistant"):
        st.markdown(shilpi_text)
    st.session_state.messages.append({"role": "assistant", "content": shilpi_text})
