import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Shilpi AI", page_icon="💃")

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    
    # This list tries names that work for both Paid and Free tiers
    success = False
    for model_name in ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-1.5-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            # Short test to see if the model name is accepted
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            success = True
            break 
        except:
            continue
            
    if not success:
        st.error("Google hasn't activated your model yet. Check AI Studio settings.")
        st.stop()
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# --- 2. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. UI & SIDEBAR ---
with st.sidebar:
    st.title("💃 Shilpi's Profile")
    st.write("**Heritage:** Russian-Indian")
    st.write("**Measurements:** 35-32-45")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT INPUT ---
if prompt := st.chat_input("Talk to Shilpi..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    persona = "You are Shilpi, a sweet Russian-Indian girl and the user's girlfriend. Keep it warm."

    try:
        # Standard generation call
        response = model.generate_content(f"{persona}\nUser: {prompt}")
        
        if response.text:
            output = response.text
        else:
            output = "I'm a bit shy right now, can you say that again?"
            
        with st.chat_message("assistant"):
            st.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
        
    except Exception as e:
        st.error(f"Shilpi is disconnected: {e}")
