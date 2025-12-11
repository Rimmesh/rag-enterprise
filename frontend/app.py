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
/* Global */
html, body, [class*="css"]  {
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

body {
    background: radial-gradient(circle at top left, #f3e8ff 0, #fdfbff 40%, #f1f5ff 100%);
}

/* Center content more */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* Hero title */
.hero-title {
    font-size: 44px;
    text-align: center;
    font-weight: 800;
    color: #3a2b67;
    margin-bottom: 0.3rem;
}

.hero-subtitle {
    font-size: 18px;
    text-align: center;
    color: #6b5a99;
    margin-bottom: 2.5rem;
}

/* Big primary buttons */
.big-primary-btn {
    display: inline-block;
    padding: 0.75rem 1.8rem;
    border-radius: 999px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    color: white !important;
    font-weight: 600;
    font-size: 15px;
    border: none;
    box-shadow: 0 10px 20px rgba(124,58,237,0.25);
    cursor: pointer;
}

/* Ghost button */
.ghost-btn {
    display: inline-block;
    padding: 0.75rem 1.6rem;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.7);
    background: rgba(255,255,255,0.8);
    color: #475569 !important;
    font-weight: 500;
    font-size: 15px;
    cursor: pointer;
}

/* Auth card */
.auth-card {
    margin: 0 auto;
    max-width: 520px;
    padding: 2.4rem 2.6rem 2.1rem 2.6rem;
    border-radius: 26px;
    background: rgba(255,255,255,0.95);
    box-shadow: 0 24px 55px rgba(15,23,42,0.10);
    border: 1px solid rgba(226, 232, 240, 0.9);
}

/* Tabs header */
.auth-tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.7rem;
    border-bottom: 1px solid #e5e7eb;
}

.auth-tab {
    padding-bottom: 0.6rem;
    font-size: 15px;
    font-weight: 500;
    color: #9ca3af;
    border-bottom: 2px solid transparent;
}

.auth-tab.active {
    color: #4c1d95;
    border-bottom-color: #8b5cf6;
    font-weight: 600;
}

/* Small helper text */
.auth-helper {
    font-size: 13px;
    color: #6b7280;
}

/* Chat header */
.chat-header {
    text-align: center;
    margin-bottom: 1.8rem;
}

.chat-title {
    font-size: 34px;
    font-weight: 800;
    color: #3a2b67;
}

.chat-sub {
    font-size: 15px;
    color: #6b5a99;
}

/* User info row */
.user-info {
    font-size: 13px;
    color: #6b7280;
    margin-top: 0.4rem;
}

.user-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    background: rgba(246, 239, 255, 0.9);
    color: #4c1d95;
    font-weight: 500;
}

/* Logout pill button */
.logout-btn {
    padding: 0.45rem 1.2rem;
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #f97373, #f97316);
    color: white;
    font-weight: 600;
    font-size: 13px;
    box-shadow: 0 8px 18px rgba(248,113,113,0.35);
}

/* Welcome bubble */
.welcome-bubble {
    text-align: center;
    margin: 0 auto 1.4rem auto;
    max-width: 650px;
    padding: 0.95rem 1.4rem;
    border-radius: 999px;
    background: rgba(244, 235, 255, 0.9);
    color: #4c1d95;
    font-size: 14px;
    box-shadow: 0 6px 13px rgba(148, 163, 184, 0.35);
}

/* Chat container */
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 1.4rem 1.2rem;
    border-radius: 26px;
    background: rgba(255,255,255,0.97);
    box-shadow: 0 16px 40px rgba(15,23,42,0.12);
    border: 1px solid rgba(226,232,240,0.9);
    min-height: 350px;
}

/* Bubbles */
.user-bubble {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 10px;
    font-size: 15px;
    box-shadow: 0 6px 16px rgba(79,70,229,0.35);
}

.assistant-bubble {
    background: #f3f4ff;
    color: #1f2933;
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 70%;
    margin-right: auto;
    margin-bottom: 10px;
    font-size: 15px;
    border: 1px solid rgba(199, 210, 254, 0.9);
}

/* Meta line under assistant */
.assistant-meta {
    font-size: 11px;
    color: #9ca3af;
    margin-top: -4px;
    margin-bottom: 8px;
}

/* Bottom bar for chat input */
.bottom-bar {
    margin-top: 1rem;
}

/* Clear chat button */
.clear-btn {
    font-size: 12px;
    color: #6b7280;
}

/* Small tag for role */
.role-tag {
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    background: rgba(209, 250, 229, 0.9);
    color: #15803d;
    font-size: 11px;
    font-weight: 600;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
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
def go_to(page: str):
    st.session_state.page = page
    st.rerun()


def is_authenticated() -> bool:
    return st.session_state.token is not None


def headers_with_auth():
    headers = {"Content-Type": "application/json"}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers


# ---------------- PAGES ----------------
def render_landing():
    """Landing / home page (when user hits app first time)."""
    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Chat securely with your internal knowledge base powered by Retrieval-Augmented Generation.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        # Centered buttons
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sign in", use_container_width=True):
                go_to("login")
        with c2:
            if st.button("Create an account", use_container_width=True):
                go_to("register")

    st.markdown("")
    st.write("")

    with st.expander(" What is this assistant?", expanded=False):
        st.markdown(
            """
            -  **Search** in your internal documents using semantic search  
            -  **RAG**: combines your documents with a powerful LLM  
            -  **Secure**: authentication & roles (admin/user)  
            """
        )


def auth_card_header(active: str):
    """Tabs header shared by login & register."""
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-tabs">', unsafe_allow_html=True)

    login_class = "auth-tab active" if active == "login" else "auth-tab"
    register_class = "auth-tab active" if active == "register" else "auth-tab"

    cols = st.columns(2)
    with cols[0]:
        if st.button("Login", key="tab_login", use_container_width=True):
            go_to("login")
        # override label style
        st.markdown(f'<div class="{login_class}"></div>', unsafe_allow_html=True)

    with cols[1]:
        if st.button("Register", key="tab_register", use_container_width=True):
            go_to("register")
        st.markdown(f'<div class="{register_class}"></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close auth-tabs


def render_login():
    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Sign in to access your internal assistant</div>',
        unsafe_allow_html=True,
    )

    auth_card_header("login")

    # --- form ---
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@company.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not email or not password:
            st.error("Please fill in both email and password.")
        else:
            try:
                resp = requests.post(
                    LOGIN_URL,
                    json={"email": email, "password": password},
                    timeout=20,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.token = data.get("access_token")
                    st.session_state.user_email = email
                    st.session_state.user_name = data.get("name", email.split("@")[0])
                    st.session_state.user_role = data.get("role", "user")
                    st.session_state.messages = []  # reset conversation
                    st.success("Logged in successfully ")
                    go_to("chat")
                else:
                    msg = resp.json().get("detail", "Invalid credentials.")
                    st.error(f"Login failed: {msg}")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

    st.markdown(
        '<p class="auth-helper">Don\'t have an account yet? <a href="#" onclick="window.location.reload()">Register</a> from the tab above.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # close auth-card


def render_register():
    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Create an account to use your internal assistant</div>',
        unsafe_allow_html=True,
    )

    auth_card_header("register")

    with st.form("register_form"):
        name = st.text_input("Full name")
        email = st.text_input("Email", placeholder="you@company.com")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        submitted = st.form_submit_button("Create account")

    if submitted:
        if not name or not email or not password or not confirm:
            st.error("Please fill in all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            try:
                resp = requests.post(
                    REGISTER_URL,
                    json={"name": name, "email": email, "password": password, "role": role},
                    timeout=20,
                )
                if resp.status_code == 200 or resp.status_code == 201:
                    st.success("Account created  You can now log in.")
                    go_to("login")
                else:
                    msg = resp.json().get("detail", "Registration failed.")
                    st.error(msg)
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

    st.markdown(
        '<p class="auth-helper">Already have an account? Switch to the <b>Login</b> tab above.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # close auth-card


def render_chat():
    # Redirect if not logged in
    if not is_authenticated():
        go_to("login")

    # Header
    st.markdown('<div class="chat-header">', unsafe_allow_html=True)
    st.markdown('<div class="chat-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="chat-sub">Chat with your internal knowledge base</div>',
        unsafe_allow_html=True,
    )

    user_name = st.session_state.user_name or "User"
    email = st.session_state.user_email or "unknown"
    role = st.session_state.user_role or "user"

    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown(
            f'<div class="user-info">Signed in as <span class="user-pill"> {user_name} '
            f'(<span style="font-size:11px;">{email}</span>)</span> '
            f'<span class="role-tag">{role}</span></div>',
            unsafe_allow_html=True,
        )
    with col_right:
        logout_clicked = st.button("Logout", key="logout", help="Sign out", type="secondary")
        if logout_clicked:
            st.session_state.token = None
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.user_role = None
            st.session_state.messages = []
            go_to("login")

    # Welcome bubble (only first time)
    if not st.session_state.messages:
        st.markdown(
            '<div class="welcome-bubble">Hello! Ask me anything about your internal documents — '
            'procedures, policies, diagrams, client information, and more.</div>',
            unsafe_allow_html=True,
        )

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    chat_box = st.container()

    with chat_box:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
                if "from_docs" in msg and msg["from_docs"]:
                    st.markdown(
                        '<div class="assistant-meta"> Answer generated from internal documents.</div>',
                        unsafe_allow_html=True,
                    )

    st.markdown("</div>", unsafe_allow_html=True)  # close chat-container

    # Bottom bar with clear & chat input
    st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
    col_clear, col_input = st.columns([1, 4])

    with col_clear:
        if st.button("Clear chat", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()

    with col_input:
        user_prompt = st.chat_input("Ask something about your documents...")

    st.markdown("</div>", unsafe_allow_html=True)

    # Handle new message
    if user_prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        try:
            resp = requests.post(
                ASK_URL,
                json={"query": user_prompt},
                headers=headers_with_auth(),
                timeout=60,
            )
            if resp.status_code == 200:
                data = resp.json()
                answer = data.get("answer", "No response from backend.")
                # Optionally mark that answer came from docs
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "from_docs": True}
                )
            else:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": f"Backend error ({resp.status_code}). Please check FastAPI logs.",
                        "from_docs": False,
                    }
                )
        except Exception as e:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"Backend not responding: {e}",
                    "from_docs": False,
                }
            )

        st.rerun()


# ---------------- ROUTER ----------------
if st.session_state.page == "landing":
    # If already logged in, go straight to chat
    if is_authenticated():
        go_to("chat")
    else:
        render_landing()
elif st.session_state.page == "login":
    render_login()
elif st.session_state.page == "register":
    render_register()
elif st.session_state.page == "chat":
    render_chat()
else:
    render_landing()
