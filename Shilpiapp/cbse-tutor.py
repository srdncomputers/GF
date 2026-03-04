import streamlit as st
from openai import OpenAI

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vidya – CBSE AI Tutor",
    page_icon="🦉",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Chat container card */
section.main > div {
    background: white;
    border-radius: 24px;
    padding: 0 !important;
    max-width: 780px;
    margin: 20px auto;
    box-shadow: 0 30px 80px rgba(0,0,0,0.3);
    overflow: hidden;
}

/* Header */
.tutor-header {
    background: linear-gradient(135deg, #6C5CE7, #a29bfe);
    padding: 20px 28px 16px;
    color: white;
}
.tutor-title {
    font-size: 24px;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin: 0;
}
.tutor-sub {
    font-size: 13px;
    opacity: 0.85;
    margin: 2px 0 0;
}

/* Stat badges */
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    font-weight: 700;
    margin-right: 8px;
}

/* Chat messages */
.user-msg {
    background: linear-gradient(135deg, #6C5CE7, #a29bfe);
    color: white;
    border-radius: 20px 20px 4px 20px;
    padding: 12px 16px;
    margin: 6px 0 6px 60px;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 2px 12px rgba(108,92,231,0.25);
}
.bot-msg {
    background: #f5f4ff;
    color: #2d2d2d;
    border-radius: 20px 20px 20px 4px;
    padding: 12px 16px;
    margin: 6px 60px 6px 0;
    font-size: 15px;
    line-height: 1.6;
    border: 1px solid #e0d8ff;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.msg-label {
    font-size: 11px;
    font-weight: 700;
    opacity: 0.6;
    margin-bottom: 4px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1a1a2e !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton > button {
    border-radius: 20px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    border: 2px solid #e0d8ff !important;
    color: #6C5CE7 !important;
    background: white !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #f0f0ff !important;
    transform: scale(1.02);
}

/* Input box */
.stTextInput > div > div > input,
.stTextArea textarea {
    border-radius: 20px !important;
    border: 2px solid #e0d8ff !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 15px !important;
    background: #fafaff !important;
    padding: 12px 18px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #6C5CE7 !important;
    box-shadow: 0 0 0 2px rgba(108,92,231,0.15) !important;
}

/* Select boxes */
.stSelectbox > div > div {
    border-radius: 14px !important;
    border: 2px solid #e0d8ff !important;
    font-family: 'Nunito', sans-serif !important;
    background: #fafaff !important;
}

/* Hide Streamlit default footer */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────
SUBJECTS = {
    "🔢 Maths": "Maths",
    "🔬 Science": "Science",
    "📖 English": "English",
    "🇮🇳 Hindi": "Hindi",
    "🌍 Social Studies": "Social Studies",
    "💻 Computers": "Computers",
}

GRADES = [f"Class {i}" for i in range(1, 11)]

QUICK_PROMPTS = [
    "Explain this topic simply 🧠",
    "Give me a quiz question ❓",
    "Help me with my homework 📝",
    "Tell me a fun fact! 🌟",
    "Give me a memory trick 🎯",
    "Make a short summary 📋",
]


# ── Session state init ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "points" not in st.session_state:
    st.session_state.points = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦉 Vidya Tutor")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Your key is never stored. Paste it here each session.",
    )

    st.markdown("### 🎓 Select Grade")
    grade = st.selectbox("Grade", GRADES, index=5, label_visibility="collapsed")

    st.markdown("### 📚 Select Subject")
    subject_emoji = st.selectbox("Subject", list(SUBJECTS.keys()), label_visibility="collapsed")
    subject = SUBJECTS[subject_emoji]

    st.markdown("---")
    st.markdown("### ⚡ Quick Prompts")
    for prompt in QUICK_PROMPTS:
        if st.button(prompt, use_container_width=True):
            st.session_state["quick_input"] = prompt

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⭐ Points", st.session_state.points)
    with col2:
        st.metric("🔥 Streak", st.session_state.streak)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.points = 0
        st.session_state.streak = 0
        st.rerun()

    st.markdown("---")
    st.caption("Built with ❤️ for CBSE students")


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="tutor-header">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; align-items:center; gap:14px;">
      <div style="font-size:40px;">🦉</div>
      <div>
        <p class="tutor-title">Vidya – AI Tutor</p>
        <p class="tutor-sub">Your Smart CBSE Learning Companion</p>
      </div>
    </div>
    <div>
      <span class="badge">📚 {subject}</span>
      <span class="badge">🎓 {grade}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── System prompt builder ──────────────────────────────────────────────────────
def build_system_prompt(grade, subject):
    return f"""You are Vidya, a friendly and enthusiastic AI tutor for CBSE school students in India.
You are currently helping a student in {grade} with {subject}.

Key guidelines:
- Use simple, clear language appropriate for {grade} students
- Follow CBSE curriculum and NCERT textbook content strictly
- Be encouraging, warm and patient — use emojis to make learning fun!
- When explaining concepts, use relatable Indian examples (cricket, Bollywood, festivals, food, etc.)
- Break down complex topics into small, easy steps
- For Maths: show step-by-step solutions with working
- For Science: connect concepts to everyday life in India
- For English: help with grammar, writing and comprehension
- For Hindi: assist with व्याकरण, निबंध, and comprehension  
- For SST: relate history/geography/civics to current events in India
- For Computers: use simple analogies and practical examples
- Add fun facts and memory tricks (mnemonics) wherever helpful
- End responses with a motivating line or follow-up question to check understanding
- Keep responses concise but complete — not too long for a school kid
- Always praise good questions with encouragement"""


# ── Chat display ───────────────────────────────────────────────────────────────
# Welcome message if no history
if not st.session_state.messages:
    st.markdown(f"""
    <div class="bot-msg">
      <div class="msg-label">🦉 Vidya</div>
      Namaste! 🙏 I'm <b>Vidya</b>, your personal AI tutor!<br>
      I'm here to help you with all your CBSE subjects.<br><br>
      Currently set to: <b>{subject_emoji} {subject}</b> for <b>{grade}</b> 🎓<br><br>
      What would you like to learn today? 😊
    </div>
    """, unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-msg">
          <div class="msg-label">🧒 You</div>
          {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-msg">
          <div class="msg-label">🦉 Vidya</div>
          {msg["content"]}
        </div>
        """, unsafe_allow_html=True)


# ── Input area ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

# Check for quick prompt injection
default_input = st.session_state.pop("quick_input", "")

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Ask Vidya...",
            value=default_input,
            placeholder=f"Ask about {subject} ({grade})...",
            label_visibility="collapsed",
        )
    with col2:
        submitted = st.form_submit_button("🚀 Send", use_container_width=True)


# ── API call ───────────────────────────────────────────────────────────────────
if submitted and user_input.strip():
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API Key in the sidebar to continue.")
        st.stop()

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # Build messages for API
    api_messages = [
        {"role": "system", "content": build_system_prompt(grade, subject)}
    ] + st.session_state.messages

    # Call OpenAI
    try:
        client = OpenAI(api_key=api_key)
        with st.spinner("Vidya is thinking... 🦉"):
            response = client.chat.completions.create(
                model="gpt-4o",          # Change to "gpt-3.5-turbo" if needed
                messages=api_messages,
                max_tokens=800,
                temperature=0.7,
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.points += 10
        st.session_state.streak += 1
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.messages.pop()  # Remove the user message if API failed