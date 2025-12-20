import streamlit as st
import requests
import time
from datetime import datetime

# ---------------- BACKEND CONFIG ----------------
BACKEND_BASE = "http://127.0.0.1:8000"
LOGIN_URL = f"{BACKEND_BASE}/auth/login"
REGISTER_URL = f"{BACKEND_BASE}/auth/register"
ASK_URL = f"{BACKEND_BASE}/ask"
ME_URL = f"{BACKEND_BASE}/auth/me"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Enterprise RAG Assistant",
    layout="wide",
    page_icon="◆",
)

# ---------------- GLOBAL CSS (REFINED MINIMALIST) ----------------
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ====== App Background ====== */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(135deg, #1a1f3a 0%, #2d1b4e 50%, #1e2a4a 100%);
    position: relative;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.12) 0%, transparent 50%);
    pointer-events: none;
}

html, body, [class*="css"]{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #ffffff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Remove default padding */
.block-container{ 
    max-width: 1400px; 
    padding-top: 2rem; 
    padding-bottom: 2rem; 
}

/* Hide Streamlit footer/menu */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

/* Remove top header */
[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
    padding: 0 !important;
    margin: 0 !important;
}

header {
    background: transparent !important;
    height: 0px !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ====== Glass Card Components ====== */
.glass-card{
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
    border-color: rgba(168, 85, 247, 0.3);
    box-shadow: 
        0 12px 40px rgba(168, 85, 247, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

/* ====== Typography ====== */
.hero-title{
  font-size: 56px;
  font-weight: 700;
  letter-spacing: -0.03em;
  text-align: center;
  margin: 0 0 0.5rem 0;
  color: #ffffff;
}

.hero-subtitle{
  text-align: center;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.75);
  margin-bottom: 2rem;
  font-weight: 400;
  letter-spacing: -0.01em;
}

/* ====== Feature Cards (ChatGPT Style) ====== */
.feature-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: rgba(168, 85, 247, 0.4);
  box-shadow: 0 12px 40px rgba(168, 85, 247, 0.2);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #ffffff;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 0.75rem;
  letter-spacing: -0.01em;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
}

/* ====== Badges ====== */
.badge{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.3);
  color: #c4b5fd;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.01em;
  transition: all 0.2s ease;
}

.badge:hover {
    background: rgba(139, 92, 246, 0.25);
    border-color: rgba(139, 92, 246, 0.4);
}

.badge-muted{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  background: rgba(71, 85, 105, 0.2);
  border: 1px solid rgba(148, 163, 184, 0.15);
  color: #94a3b8;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.divider{
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  margin: 1.5rem 0;
}

/* ====== Chat Interface ====== */
.chat-shell{
  height: 68vh;
  overflow-y: auto;
  padding: 1.5rem;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
}

.chat-shell::-webkit-scrollbar {
  width: 8px;
}

.chat-shell::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.3);
  border-radius: 10px;
}

.chat-shell::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.3);
  border-radius: 10px;
  transition: background 0.2s ease;
}

.chat-shell::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 92, 246, 0.5);
}

/* Message rows */
.msg-row{
  display: flex;
  margin: 0.8rem 0;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.msg-left{ justify-content: flex-start; }
.msg-right{ justify-content: flex-end; }

/* Message bubbles */
.bubble-user{
  max-width: 75%;
  padding: 14px 18px;
  border-radius: 16px 16px 4px 16px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  color: #ffffff;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
  font-size: 15px;
  line-height: 1.5;
  font-weight: 400;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.bubble-user:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.bubble-ai{
  max-width: 75%;
  padding: 14px 18px;
  border-radius: 16px 16px 16px 4px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.15);
  color: #ffffff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  font-size: 15px;
  line-height: 1.6;
  font-weight: 400;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.bubble-ai:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.meta{
  font-size: 11px;
  color: rgba(148, 163, 184, 0.6);
  margin-top: 8px;
  font-style: italic;
}

/* ====== Sidebar Styling ====== */
section[data-testid="stSidebar"]{
  background: rgba(15, 23, 42, 0.7);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

section[data-testid="stSidebar"] h3 {
    color: #ffffff;
    font-weight: 600;
    letter-spacing: -0.02em;
}

section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label {
    color: rgba(255, 255, 255, 0.85) !important;
}

section[data-testid="stSidebar"] .stCaption {
    color: rgba(255, 255, 255, 0.6) !important;
}

section[data-testid="stSidebar"] .stButton button {
    background: rgba(139, 92, 246, 0.15);
    color: #c4b5fd;
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 10px;
    font-weight: 500;
    padding: 0.6rem 1rem;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(139, 92, 246, 0.25);
    border-color: rgba(139, 92, 246, 0.4);
    transform: translateY(-1px);
}

/* ====== Form Inputs ====== */
input[type="text"], input[type="password"], input[type="email"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #f1f5f9 !important;
    border-radius: 12px !important;
    padding: 0.9rem 1rem !important;
    transition: all 0.2s ease !important;
    font-size: 15px !important;
}

input[type="text"]:focus, input[type="password"]:focus, input[type="email"]:focus {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(168, 85, 247, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.15) !important;
    outline: none !important;
}

input::placeholder {
    color: rgba(226, 232, 240, 0.4) !important;
}

/* ====== Buttons ====== */
.stButton button {
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 500;
    padding: 0.7rem 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
}

/* ====== Select Box ====== */
.stSelectbox > div > div {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 10px;
    color: #e2e8f0;
}

/* ====== Radio Buttons ====== */
.stRadio > div {
    background: rgba(15, 23, 42, 0.4);
    padding: 0.5rem;
    border-radius: 10px;
}

/* ====== Chat Input ====== */
.stChatInput textarea {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
}

.stChatInput textarea:focus {
    border-color: rgba(139, 92, 246, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
}

/* ====== Success/Error Messages ====== */
.stSuccess {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #86efac;
    border-radius: 10px;
}

.stError {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #fca5a5;
    border-radius: 10px;
}

/* ====== Status Indicators ====== */
.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}

.status-online {
    background: #22c55e;
}

.status-offline {
    background: #ef4444;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
def _init_state():
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

    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

    if "current_conv_id" not in st.session_state:
        st.session_state.current_conv_id = None


_init_state()

# ---------------- HELPERS ----------------
def go_to(page: str):
    st.session_state.page = page
    st.rerun()


def is_authenticated() -> bool:
    return st.session_state.token is not None


def headers_with_auth():
    h = {"Content-Type": "application/json"}
    if st.session_state.token:
        h["Authorization"] = f"Bearer {st.session_state.token}"
    return h


def _new_chat(title: str | None = None):
    conv_id = f"c_{int(time.time() * 1000)}"
    st.session_state.conversations[conv_id] = {
        "title": title or "New conversation",
        "created_at": time.time(),
        "messages": [],
    }
    st.session_state.current_conv_id = conv_id


def _current_messages():
    cid = st.session_state.current_conv_id
    if not cid or cid not in st.session_state.conversations:
        _new_chat()
        cid = st.session_state.current_conv_id
    return st.session_state.conversations[cid]["messages"]


def _set_title_from_first_user_message(cid: str, user_text: str):
    words = user_text.strip().split()
    short = " ".join(words[:8]).strip()
    if len(words) > 8:
        short += "…"
    st.session_state.conversations[cid]["title"] = short or "Chat"


def _safe_get_me():
    try:
        r = requests.get(ME_URL, headers=headers_with_auth(), timeout=10)
        if r.status_code == 200:
            data = r.json()
            st.session_state.user_name = data.get("name") or st.session_state.user_name
            st.session_state.user_role = data.get("role") or st.session_state.user_role
    except Exception:
        pass


# ---------------- SIDEBAR ----------------
def render_sidebar():
    with st.sidebar:
        st.markdown("### Enterprise RAG")
        st.caption("Secure knowledge base assistant")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if is_authenticated():
            name = st.session_state.user_name or "User"
            email = st.session_state.user_email or "unknown"
            role = st.session_state.user_role or "user"

            st.markdown(
                f'<span class="status-dot status-online"></span>'
                f'<span class="badge">Authenticated</span> '
                f'<span class="badge-muted">{role}</span>',
                unsafe_allow_html=True,
            )
            st.write(f"**{name}**")
            st.caption(email)

            colA, colB = st.columns(2)
            with colA:
                if st.button("New Chat", use_container_width=True):
                    _new_chat()
                    go_to("chat")
            with colB:
                if st.button("Logout", use_container_width=True):
                    st.session_state.token = None
                    st.session_state.user_email = None
                    st.session_state.user_name = None
                    st.session_state.user_role = None
                    st.session_state.page = "landing"
                    st.rerun()

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            st.markdown("#### Conversation History")
            if not st.session_state.conversations:
                st.caption("No conversations yet. Start a new chat.")
            else:
                items = sorted(
                    st.session_state.conversations.items(),
                    key=lambda x: x[1]["created_at"],
                    reverse=True
                )

                ids = [k for k, _ in items]
                current = st.session_state.current_conv_id
                if current not in ids:
                    st.session_state.current_conv_id = ids[0] if ids else None
                    current = st.session_state.current_conv_id

                default_index = ids.index(current) if current in ids else 0
                chosen = st.selectbox(
                    "Select conversation",
                    options=ids,
                    index=default_index,
                    format_func=lambda cid: st.session_state.conversations[cid]["title"],
                    label_visibility="collapsed",
                )
                st.session_state.current_conv_id = chosen

                colD, colE = st.columns(2)
                with colD:
                    if st.button("Clear", use_container_width=True):
                        st.session_state.conversations[chosen]["messages"] = []
                        st.rerun()
                with colE:
                    if st.button("Delete", use_container_width=True):
                        st.session_state.conversations.pop(chosen, None)
                        st.session_state.current_conv_id = None
                        st.rerun()

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            nav = st.radio(
                "Navigation",
                ["Chat", "Landing"],
                index=0 if st.session_state.page == "chat" else 1,
                label_visibility="collapsed",
            )
            if nav == "Chat" and st.session_state.page != "chat":
                go_to("chat")
            if nav == "Landing" and st.session_state.page != "landing":
                go_to("landing")

        else:
            st.markdown(
                f'<span class="status-dot status-offline"></span>'
                f'<span class="badge-muted">Not authenticated</span>', 
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sign In", use_container_width=True):
                    go_to("login")
            with col2:
                if st.button("Register", use_container_width=True):
                    go_to("register")

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.caption("Switch between Sign In and Register using the sidebar buttons.")

# ---------------- PAGES ----------------
def render_landing():
    # Don't render sidebar on landing page
    if is_authenticated():
        go_to("chat")
        return

    # Top right auth buttons
    col1, col2, col3, col4 = st.columns([3, 1, 1, 0.3])
    with col2:
        if st.button("Sign In", use_container_width=True, key="landing_signin"):
            go_to("login")
    with col3:
        if st.button("Register", use_container_width=True, key="landing_register"):
            go_to("register")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Secure, intelligent conversations with your internal knowledge base</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ChatGPT-style cards
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Smart Search</h3>
                <p>Query your documents with FAISS-powered search and intelligent metadata filtering</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3>Secure Access</h3>
                <p>Protected authentication system keeps your data safe and accessible only to you</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <h3>Chat History</h3>
                <p>Access all your past conversations and continue right where you left off</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_login():
    render_sidebar()

    st.markdown('<div class="hero-title">Sign In</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Access your assistant securely</div>', unsafe_allow_html=True)

    colL, colC, colR = st.columns([1, 2, 1])
    with colC:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span class="badge">Authentication</span>', unsafe_allow_html=True)
        with col2:
            if st.button("Register", use_container_width=True, key="goto_register"):
                go_to("register")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please provide both email and password")
            else:
                try:
                    r = requests.post(LOGIN_URL, json={"email": email, "password": password}, timeout=20)
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.token = data.get("access_token")
                        st.session_state.user_email = email
                        st.session_state.user_name = email.split("@")[0]
                        st.session_state.user_role = "user"

                        _safe_get_me()

                        if not st.session_state.conversations:
                            _new_chat()
                        if not st.session_state.current_conv_id:
                            st.session_state.current_conv_id = next(iter(st.session_state.conversations.keys()), None)

                        go_to("chat")
                    else:
                        try:
                            msg = r.json().get("detail", "Authentication failed")
                        except Exception:
                            msg = "Authentication failed"
                        st.error(msg)
                except Exception as e:
                    st.error(f"Unable to reach backend: {e}")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if st.button("Back to Landing", use_container_width=True, key="back_to_landing_login"):
            go_to("landing")

        st.markdown("</div>", unsafe_allow_html=True)


def render_register():
    render_sidebar()

    st.markdown('<div class="hero-title">Create Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Join and start chatting with your knowledge base</div>', unsafe_allow_html=True)

    colL, colC, colR = st.columns([1, 2, 1])
    with colC:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span class="badge">Registration</span>', unsafe_allow_html=True)
        with col2:
            if st.button("Sign In", use_container_width=True, key="goto_signin"):
                go_to("login")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with st.form("register_form", clear_on_submit=False):
            name = st.text_input("Full Name", placeholder="Your Name")
            email = st.text_input("Email", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="Choose a strong password")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)

        if submitted:
            if not name or not email or not password or not confirm:
                st.error("All fields are required")
            elif password != confirm:
                st.error("Passwords do not match")
            else:
                try:
                    r = requests.post(
                        REGISTER_URL,
                        json={"name": name, "email": email, "password": password},
                        timeout=20,
                    )
                    if r.status_code in (200, 201):
                        st.success("Account created successfully. Please sign in.")
                        go_to("login")
                    else:
                        try:
                            msg = r.json().get("detail", "Registration failed")
                        except Exception:
                            msg = "Registration failed"
                        st.error(msg)
                except Exception as e:
                    st.error(f"Unable to reach backend: {e}")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if st.button("Back to Landing", use_container_width=True, key="back_to_landing_register"):
            go_to("landing")

        st.markdown("</div>", unsafe_allow_html=True)


def render_chat():
    render_sidebar()

    if not is_authenticated():
        go_to("login")

    if not st.session_state.conversations:
        _new_chat()
    if not st.session_state.current_conv_id:
        st.session_state.current_conv_id = next(iter(st.session_state.conversations.keys()))

    cid = st.session_state.current_conv_id
    conv = st.session_state.conversations[cid]
    messages = conv["messages"]

    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Ask questions about your internal documents with intelligent search</div>',
        unsafe_allow_html=True,
    )

    left, mid, right = st.columns([2.2, 1.2, 1.2])
    with left:
        name = st.session_state.user_name or "User"
        email = st.session_state.user_email or "unknown"
        role = st.session_state.user_role or "user"
        st.markdown(
            f'<span class="badge">{name}</span> <span class="badge-muted">{email}</span> <span class="badge-muted">{role}</span>',
            unsafe_allow_html=True,
        )
    with mid:
        st.markdown(
            f'<span class="badge-muted">{datetime.fromtimestamp(conv["created_at"]).strftime("%d/%m/%Y %H:%M")}</span>',
            unsafe_allow_html=True
        )
    with right:
        st.markdown(f'<span class="badge">{conv["title"]}</span>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    if not messages:
        st.markdown(
            """
            <div class="chat-shell">
              <div class="bubble-ai">
                Welcome to your Enterprise RAG Assistant. Ask me anything about your documents — policies, procedures, specifications, or course content.
                <div class="meta">Your conversation history is available in the sidebar</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        html = ['<div class="chat-shell">']
        for m in messages:
            if m["role"] == "user":
                html.append(
                    f'<div class="msg-row msg-right"><div class="bubble-user">{m["content"]}</div></div>'
                )
            else:
                html.append(
                    f'<div class="msg-row msg-left"><div class="bubble-ai">{m["content"]}</div></div>'
                )
        html.append("</div>")
        st.markdown("\n".join(html), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    prompt = st.chat_input("Ask about your documents...")

    if prompt:
        messages.append({"role": "user", "content": prompt})

        if len([m for m in messages if m["role"] == "user"]) == 1:
            _set_title_from_first_user_message(cid, prompt)

        try:
            r = requests.post(
                ASK_URL,
                json={"question": prompt},  
                headers=headers_with_auth(),
                timeout=90,
            )
            if r.status_code == 200:
                answer = r.json().get("answer", "No answer received")
            else:
                answer = f"Backend error ({r.status_code}). Check FastAPI logs."
        except Exception as e:
            answer = f"Backend not responding: {e}"

        messages.append({"role": "assistant", "content": answer})
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
else:
    render_landing()