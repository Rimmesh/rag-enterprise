import streamlit as st
import requests

# ---------------- BACKEND CONFIG ----------------
BACKEND_BASE = "http://127.0.0.1:8000"
LOGIN_URL = f"{BACKEND_BASE}/auth/login"
REGISTER_URL = f"{BACKEND_BASE}/auth/register"
ASK_URL = f"{BACKEND_BASE}/ask"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Enterprise RAG Assistant",
    layout="wide",
    page_icon="💼"
)

# ---------------- GLOBAL CSS ----------------
GLOBAL_CSS = """
<style>
html, body, [class*="css"] {
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

body {
    background: radial-gradient(circle at top left, #f3e8ff 0, #fdfbff 40%, #f1f5ff 100%);
}

.block-container {
    max-width: 1100px;
    padding-top: 1.8rem;
}

/* Titles */
.hero-title, .chat-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #3a2b67;
}

.hero-subtitle, .chat-sub {
    text-align: center;
    font-size: 16px;
    color: #6b5a99;
    margin-bottom: 2rem;
}

/* Glass chat container */
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 1.6rem;
    border-radius: 26px;
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 20px 45px rgba(15,23,42,0.18);
    border: 1px solid rgba(255,255,255,0.4);
    min-height: 420px;
}

/* Bubbles */
.user-bubble {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 70%;
    font-size: 15px;
    box-shadow: 0 6px 16px rgba(79,70,229,0.35);
}

.assistant-bubble {
    background: #f3f4ff;
    color: #1f2937;
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 70%;
    font-size: 15px;
    border: 1px solid rgba(199,210,254,0.9);
}

/* Welcome */
.welcome-bubble {
    text-align: center;
    margin: 0 auto 1.4rem auto;
    max-width: 650px;
    padding: 0.9rem 1.4rem;
    border-radius: 999px;
    background: rgba(244,235,255,0.9);
    color: #4c1d95;
    font-size: 14px;
    box-shadow: 0 6px 13px rgba(148,163,184,0.35);
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HELPERS ----------------
def go_to(page):
    st.session_state.page = page
    st.rerun()

def is_authenticated():
    return st.session_state.token is not None

def headers_with_auth():
    h = {"Content-Type": "application/json"}
    if st.session_state.token:
        h["Authorization"] = f"Bearer {st.session_state.token}"
    return h

# ---------------- PAGES ----------------
def render_landing():
    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Chat securely with your internal knowledge base</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Sign in", use_container_width=True):
            go_to("login")
    with c2:
        if st.button("Create an account", use_container_width=True):
            go_to("register")

def render_login():
    st.markdown('<div class="hero-title">Sign in</div>', unsafe_allow_html=True)
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            r = requests.post(LOGIN_URL, json={"email": email, "password": password})
            if r.status_code == 200:
                data = r.json()
                st.session_state.token = data["access_token"]
                st.session_state.user_email = email
                st.session_state.user_name = data.get("name", email.split("@")[0])
                st.session_state.user_role = data.get("role", "user")
                st.session_state.messages = []
                go_to("chat")
            else:
                st.error("Login failed")

def render_register():
    st.markdown('<div class="hero-title">Register</div>', unsafe_allow_html=True)
    with st.form("register"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        if st.form_submit_button("Create account"):
            r = requests.post(
                REGISTER_URL,
                json={"name": name, "email": email, "password": password, "role": role},
            )
            if r.status_code in (200, 201):
                go_to("login")
            else:
                st.error("Registration failed")

def render_chat():
    if not is_authenticated():
        go_to("login")

    st.markdown('<div class="chat-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-sub">Ask questions about your internal documents</div>', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown('<div class="welcome-bubble">Ask me anything about your documents.</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="display:flex;justify-content:flex-end;"><div class="user-bubble">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="display:flex;justify-content:flex-start;"><div class="assistant-bubble">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

    prompt = st.chat_input("Ask something about your documents...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            r = requests.post(
                ASK_URL,
                json={"question": prompt},  # ✅ FIXED HERE
                headers=headers_with_auth(),
                timeout=60,
            )
            if r.status_code == 200:
                answer = r.json().get("answer", "No answer.")
            else:
                answer = f"Backend error ({r.status_code})"
        except Exception as e:
            answer = f"Backend not responding: {e}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

# ---------------- ROUTER ----------------
if st.session_state.page == "landing":
    render_landing()
elif st.session_state.page == "login":
    render_login()
elif st.session_state.page == "register":
    render_register()
elif st.session_state.page == "chat":
    render_chat()
