import streamlit as st
import json
import os
from datetime import datetime
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
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { background: #1a1a2e !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e0d8ff !important; }

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #2d2b55 !important; border: 1.5px solid #5a4fcf !important;
    border-radius: 12px !important; color: #ffffff !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div > div { color: #ffffff !important; }
[data-testid="stSidebar"] .stSelectbox svg { fill: #a29bfe !important; }

[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: #2d2b55 !important; border: 1.5px solid #5a4fcf !important;
    border-radius: 12px !important; color: #ffffff !important;
    font-family: 'Nunito', sans-serif !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder { color: #8a7fcf !important; }

[data-testid="stSidebar"] .stButton > button {
    background: #2d2b55 !important; border: 1.5px solid #5a4fcf !important;
    color: #a29bfe !important; border-radius: 20px !important;
    font-family: 'Nunito', sans-serif !important; font-weight: 700 !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #3d3b75 !important; border-color: #a29bfe !important; color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #2d2b55; border-radius: 12px; padding: 8px 12px; border: 1px solid #5a4fcf;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #a29bfe !important; font-size: 22px !important; font-weight: 900 !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: #c5b8f5 !important; font-size: 12px !important; }
[data-testid="stSidebar"] .stAlert { background: #2d2b55 !important; border-radius: 12px !important; color: #e0d8ff !important; }
[data-testid="stSidebar"] hr { border-color: #3d3b75 !important; }
[data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] small { color: #7a6fcf !important; }

/* ── MAIN AREA ── */
section.main > div {
    background: white; border-radius: 24px; padding: 0 !important;
    max-width: 780px; margin: 20px auto;
    box-shadow: 0 30px 80px rgba(0,0,0,0.3); overflow: hidden;
}

.tutor-header {
    background: linear-gradient(135deg, #6C5CE7, #a29bfe);
    padding: 20px 28px 16px; color: white;
}
.tutor-title { font-size: 24px; font-weight: 900; letter-spacing: -0.5px; margin: 0; }
.tutor-sub   { font-size: 13px; opacity: 0.85; margin: 2px 0 0; }
.badge {
    display: inline-block; background: rgba(255,255,255,0.2);
    border-radius: 20px; padding: 4px 14px; font-size: 13px; font-weight: 700; margin-right: 8px;
}

/* Memory card */
.memory-card {
    background: #f0f7ff; border: 1px solid #c8e0ff; border-radius: 14px;
    padding: 12px 16px; margin: 10px 0; font-size: 13px; color: #2d2d2d;
}
.memory-card b { color: #4a6fa5; }
.memory-tag {
    display: inline-block; background: #e8f0fe; color: #4a6fa5;
    border-radius: 10px; padding: 2px 10px; font-size: 12px;
    font-weight: 700; margin: 2px 3px;
}
.memory-tag.weak { background: #fff0f0; color: #d63031; }
.memory-tag.strong { background: #f0fff4; color: #00b894; }

/* Chat bubbles */
.user-msg {
    background: linear-gradient(135deg, #6C5CE7, #a29bfe); color: white;
    border-radius: 20px 20px 4px 20px; padding: 12px 16px;
    margin: 6px 0 6px 60px; font-size: 15px; line-height: 1.6;
    box-shadow: 0 2px 12px rgba(108,92,231,0.25);
}
.bot-msg {
    background: #f5f4ff; color: #2d2d2d;
    border-radius: 20px 20px 20px 4px; padding: 12px 16px;
    margin: 6px 60px 6px 0; font-size: 15px; line-height: 1.6;
    border: 1px solid #e0d8ff; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.msg-label { font-size: 11px; font-weight: 700; opacity: 0.6; margin-bottom: 4px; }

/* Main input */
.stTextInput > div > div > input {
    border-radius: 20px !important; border: 2px solid #e0d8ff !important;
    font-family: 'Nunito', sans-serif !important; font-size: 15px !important;
    background: #fafaff !important; padding: 12px 18px !important; color: #2d2d2d !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6C5CE7 !important; box-shadow: 0 0 0 2px rgba(108,92,231,0.15) !important;
}

/* Send button */
.stForm .stButton > button {
    background: linear-gradient(135deg, #6C5CE7, #a29bfe) !important;
    color: white !important; border: none !important; border-radius: 20px !important;
    font-family: 'Nunito', sans-serif !important; font-weight: 800 !important;
    font-size: 15px !important; padding: 10px !important;
}
.stForm .stButton > button:hover { opacity: 0.9 !important; }

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
[data-testid="stHeader"], header[data-testid="stHeader"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-bottom: none !important;
}
[data-testid="stToolbar"]  { background: transparent !important; }
[data-testid="stDecoration"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }
</style>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────
SUBJECTS = {
    "🔢 Maths": "Maths", "🔬 Science": "Science",
    "📖 English": "English", "🇮🇳 Hindi": "Hindi",
    "🌍 Social Studies": "Social Studies", "💻 Computers": "Computers",
}
GRADES = [f"Class {i}" for i in range(1, 11)]
QUICK_PROMPTS = [
    "Explain this topic simply 🧠", "Give me a quiz question ❓",
    "Help me with my homework 📝", "Tell me a fun fact! 🌟",
    "Give me a memory trick 🎯",   "Make a short summary 📋",
]
MEMORY_FILE = "student_memory.json"


# ── API Key ────────────────────────────────────────────────────────────────────
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    OPENAI_API_KEY = None


# ── Memory helpers ─────────────────────────────────────────────────────────────
def load_all_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_all_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_student_memory(name):
    """Return memory dict for a student, creating if not exists."""
    all_mem = load_all_memory()
    key = name.strip().lower()
    if key not in all_mem:
        all_mem[key] = {
            "name": name.strip().title(),
            "grade": "",
            "points": 0,
            "streak": 0,
            "sessions": 0,
            "last_seen": "",
            "topics_asked": [],       # all topics ever asked
            "weak_topics": [],        # topics asked 3+ times (needs help)
            "strong_topics": [],      # topics answered well
            "favourite_subject": "",
            "notes": "",              # teacher/tutor notes
        }
        save_all_memory(all_mem)
    return all_mem[key]

def update_student_memory(name, updates):
    all_mem = load_all_memory()
    key = name.strip().lower()
    if key in all_mem:
        all_mem[key].update(updates)
        save_all_memory(all_mem)

def add_topic(name, topic, is_weak=False):
    """Track topics; mark as weak if asked 3+ times."""
    all_mem = load_all_memory()
    key = name.strip().lower()
    if key not in all_mem:
        return
    mem = all_mem[key]
    mem["topics_asked"].append(topic)
    # Keep last 50 topics
    mem["topics_asked"] = mem["topics_asked"][-50:]
    # Count repeats → weak topic
    if is_weak and topic not in mem["weak_topics"]:
        mem["weak_topics"].append(topic)
        mem["weak_topics"] = mem["weak_topics"][-20:]
    save_all_memory(all_mem)

def list_students():
    all_mem = load_all_memory()
    return list(all_mem.keys())

def memory_summary(mem):
    """Build a text summary of student memory for the system prompt."""
    lines = [f"Student name: {mem['name']}"]
    if mem.get("grade"):        lines.append(f"Grade: {mem['grade']}")
    if mem.get("sessions"):     lines.append(f"Total sessions: {mem['sessions']}")
    if mem.get("last_seen"):    lines.append(f"Last studied: {mem['last_seen']}")
    if mem.get("weak_topics"):  lines.append(f"Topics needing extra help: {', '.join(mem['weak_topics'][-5:])}")
    if mem.get("strong_topics"):lines.append(f"Topics the student is good at: {', '.join(mem['strong_topics'][-5:])}")
    if mem.get("favourite_subject"): lines.append(f"Favourite subject: {mem['favourite_subject']}")
    if mem.get("notes"):        lines.append(f"Teacher notes: {mem['notes']}")
    return "\n".join(lines)


# ── Session state init ─────────────────────────────────────────────────────────
for k, v in [("messages", []), ("student_name", ""), ("logged_in", False),
             ("points", 0), ("streak", 0)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════════════════════════════════
# ── LOGIN SCREEN (if not logged in) ───────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px 20px;">
      <div style="font-size:64px;">🦉</div>
      <h1 style="color:white; font-size:36px; font-weight:900; margin:10px 0 4px;">Vidya AI Tutor</h1>
      <p style="color:rgba(255,255,255,0.8); font-size:16px;">Your Smart CBSE Learning Companion</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background:white; border-radius:20px; padding:28px 24px;
                    box-shadow:0 20px 60px rgba(0,0,0,0.25);">
          <h3 style="color:#6C5CE7; font-weight:900; margin:0 0 16px; text-align:center;">
            👋 Who's studying today?
          </h3>
        </div>
        """, unsafe_allow_html=True)

        existing = list_students()
        login_tab, new_tab = st.tabs(["📂 Returning Student", "🆕 New Student"])

        with login_tab:
            if existing:
                selected = st.selectbox(
                    "Select your name",
                    [s.title() for s in existing],
                    label_visibility="visible"
                )
                if st.button("▶️ Continue Learning", use_container_width=True):
                    mem = get_student_memory(selected)
                    st.session_state.student_name = mem["name"]
                    st.session_state.points  = mem.get("points", 0)
                    st.session_state.streak  = mem.get("streak", 0)
                    st.session_state.logged_in = True
                    # Update session count & last seen
                    update_student_memory(selected, {
                        "sessions": mem.get("sessions", 0) + 1,
                        "last_seen": datetime.now().strftime("%d %b %Y"),
                    })
                    st.rerun()
            else:
                st.info("No students yet. Create a new profile! 👉")

        with new_tab:
            new_name = st.text_input("Your name", placeholder="e.g. Arjun, Priya...")
            if st.button("🚀 Start Learning!", use_container_width=True):
                if new_name.strip():
                    mem = get_student_memory(new_name)
                    st.session_state.student_name = mem["name"]
                    st.session_state.points  = 0
                    st.session_state.streak  = 0
                    st.session_state.logged_in = True
                    update_student_memory(new_name, {
                        "sessions": 1,
                        "last_seen": datetime.now().strftime("%d %b %Y"),
                    })
                    st.rerun()
                else:
                    st.warning("Please enter your name!")
    st.stop()


# ════════════════════════════════════════════════════════════════════════════════
# ── MAIN TUTOR (logged in) ─────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════════
student_name = st.session_state.student_name
mem = get_student_memory(student_name)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## 🦉 Hi, {student_name}! 👋")

    if not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY missing in Secrets.")

    st.markdown("---")
    st.markdown("### 🎓 Grade")
    grade = st.selectbox("Grade", GRADES,
                         index=GRADES.index(mem["grade"]) if mem["grade"] in GRADES else 5,
                         label_visibility="collapsed")
    update_student_memory(student_name, {"grade": grade})

    st.markdown("### 📚 Subject")
    subject_emoji = st.selectbox("Subject", list(SUBJECTS.keys()), label_visibility="collapsed")
    subject = SUBJECTS[subject_emoji]

    st.markdown("---")
    st.markdown("### ⚡ Quick Prompts")
    for prompt in QUICK_PROMPTS:
        if st.button(prompt, use_container_width=True):
            st.session_state["quick_input"] = prompt

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.metric("⭐ Points",  st.session_state.points)
    with c2: st.metric("🔥 Streak",  st.session_state.streak)
    st.metric("📅 Sessions", mem.get("sessions", 1))

    # ── Student Memory Panel ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🧠 My Memory")

    weak    = mem.get("weak_topics",   [])[-5:]
    strong  = mem.get("strong_topics", [])[-5:]
    last    = mem.get("last_seen", "Today")

    if weak:
        st.markdown("**📌 Needs practice:**")
        st.markdown(" ".join([f"`{t}`" for t in weak]))
    if strong:
        st.markdown("**✅ Doing well:**")
        st.markdown(" ".join([f"`{t}`" for t in strong]))

    # Teacher note
    with st.expander("📝 Add a note"):
        note = st.text_input("Note", value=mem.get("notes",""), label_visibility="collapsed",
                             placeholder="e.g. struggles with fractions")
        if st.button("💾 Save Note"):
            update_student_memory(student_name, {"notes": note})
            st.success("Saved!")

    # Mark strong topic
    with st.expander("🌟 Mark topic as strong"):
        strong_input = st.text_input("Topic", label_visibility="collapsed", placeholder="e.g. Photosynthesis")
        if st.button("✅ Mark Strong"):
            if strong_input.strip():
                updated = list(set(mem.get("strong_topics", []) + [strong_input.strip()]))
                update_student_memory(student_name, {"strong_topics": updated[-20:]})
                st.success("Marked!")

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔚 Switch Student", use_container_width=True):
        # Save points/streak before logout
        update_student_memory(student_name, {
            "points": st.session_state.points,
            "streak": st.session_state.streak,
        })
        for k in ["messages", "student_name", "logged_in", "points", "streak"]:
            del st.session_state[k]
        st.rerun()

    st.markdown("---")
    st.caption("Built with ❤️ for CBSE students")


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="tutor-header">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
    <div style="display:flex;align-items:center;gap:14px;">
      <div style="font-size:40px;">🦉</div>
      <div>
        <p class="tutor-title">Vidya – AI Tutor</p>
        <p class="tutor-sub">Welcome back, {student_name}! Ready to learn? 🚀</p>
      </div>
    </div>
    <div>
      <span class="badge">{subject_emoji} {subject}</span>
      <span class="badge">🎓 {grade}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Show memory recap card if student has history
if mem.get("weak_topics") or mem.get("last_seen"):
    weak_html = "".join([f'<span class="memory-tag weak">{t}</span>' for t in mem.get("weak_topics", [])[-3:]])
    strong_html = "".join([f'<span class="memory-tag strong">{t}</span>' for t in mem.get("strong_topics", [])[-3:]])
    last_seen = mem.get("last_seen", "")
    sessions  = mem.get("sessions", 1)
    st.markdown(f"""
    <div class="memory-card">
      <b>🧠 Vidya remembers:</b> &nbsp;
      {f"Last studied <b>{last_seen}</b> &nbsp;•&nbsp;" if last_seen else ""}
      <b>{sessions}</b> session{'s' if sessions != 1 else ''} completed
      {f"<br>📌 Needs practice: {weak_html}" if weak_html else ""}
      {f"<br>✅ Strong at: {strong_html}" if strong_html else ""}
    </div>
    """, unsafe_allow_html=True)


# ── System prompt with memory ──────────────────────────────────────────────────
def build_system_prompt(grade, subject, mem):
    mem_text = memory_summary(mem)
    return f"""You are Vidya, a friendly and enthusiastic AI tutor for CBSE school students in India.

STUDENT PROFILE:
{mem_text}

You are currently helping this student with {subject} ({grade}).

Guidelines:
- Always address the student by their first name warmly
- If they have weak topics noted, gently revisit and reinforce those concepts
- If they are strong at a topic, give them slightly harder challenges to keep them growing
- Follow CBSE curriculum and NCERT textbook content strictly
- Use simple, clear language appropriate for {grade} students
- Be encouraging, warm and patient — use emojis to make learning fun!
- Use relatable Indian examples (cricket, Bollywood, festivals, food, etc.)
- Break complex topics into small easy steps
- For Maths: show step-by-step solutions with full working
- For Science: connect concepts to everyday life in India
- For English: help with grammar, writing and comprehension
- For Hindi: assist with व्याकरण, निबंध, and comprehension
- For SST: relate history/geography/civics to current Indian events
- For Computers: use simple analogies and practical examples
- Add fun facts and memory tricks (mnemonics) wherever helpful
- End with a motivating line or follow-up question
- Keep responses concise — not too long for a school kid
- If the student seems to repeatedly ask about the same topic, note it as a weak area"""


# ── Chat display ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    greeting = f"Namaste {student_name}! 🙏"
    if mem.get("sessions", 1) > 1:
        greeting += f" Great to see you again! You've completed <b>{mem['sessions']}</b> sessions — keep it up! 🌟"
    if mem.get("weak_topics"):
        greeting += f"<br>I remember you were working on <b>{mem['weak_topics'][-1]}</b> last time — want to continue? 💪"
    else:
        greeting += " I'm ready to help with all your CBSE subjects. What shall we learn today? 😊"

    st.markdown(f"""
    <div class="bot-msg">
      <div class="msg-label">🦉 Vidya</div>
      {greeting}
    </div>""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-msg">
          <div class="msg-label">🧒 {student_name}</div>
          {msg["content"]}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-msg">
          <div class="msg-label">🦉 Vidya</div>
          {msg["content"]}
        </div>""", unsafe_allow_html=True)


# ── Input form ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
default_input = st.session_state.pop("quick_input", "")

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "msg", value=default_input,
            placeholder=f"Ask Vidya about {subject} ({grade})...",
            label_visibility="collapsed",
        )
    with col2:
        submitted = st.form_submit_button("🚀 Send", use_container_width=True)


# ── OpenAI call ────────────────────────────────────────────────────────────────
if submitted and user_input.strip():
    if not OPENAI_API_KEY:
        st.error("⚠️ API Key not configured. Add OPENAI_API_KEY in Streamlit Secrets.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # Track topic (use first 6 words as topic label)
    topic_label = " ".join(user_input.strip().split()[:6])
    add_topic(student_name, topic_label)

    api_messages = [
        {"role": "system", "content": build_system_prompt(grade, subject, mem)}
    ] + st.session_state.messages

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        with st.spinner("Vidya is thinking... 🦉"):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=api_messages,
                max_tokens=800,
                temperature=0.7,
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # Update points, streak, favourite subject
        new_points = st.session_state.points + 10
        new_streak = st.session_state.streak + 1
        st.session_state.points = new_points
        st.session_state.streak = new_streak
        update_student_memory(student_name, {
            "points": new_points,
            "streak": new_streak,
            "favourite_subject": subject,
        })
        st.rerun()

    except Exception as e:
        st.error(f"❌ OpenAI Error: {str(e)}")
        st.session_state.messages.pop()