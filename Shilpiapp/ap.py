import streamlit as st
from openai import OpenAI

# --- 1. SETUP ---
st.set_page_config(page_title="Shilpi AI", page_icon="💃")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
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
        # Create full conversation with persona as system message
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # cost effective
            messages=[
                {"role": "system", "content": persona},
                *st.session_state.messages
            ],
            temperature=0.8
        )

        output = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(output)

        st.session_state.messages.append(
            {"role": "assistant", "content": output}
        )

    except Exception as e:
        st.error(f"Shilpi is disconnected: {e}")
