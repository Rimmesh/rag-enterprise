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
    page_icon="💼",
)

# ---------------- GLOBAL CSS (GLASS / WOW UI) ----------------
GLOBAL_CSS = """
<style>
/* ====== App Background ====== */
[data-testid="stAppViewContainer"]{
    background:
      radial-gradient(900px 500px at 10% 10%, rgba(168,85,247,0.28), transparent 60%),
      radial-gradient(900px 500px at 90% 20%, rgba(79,70,229,0.22), transparent 55%),
      radial-gradient(900px 500px at 20% 90%, rgba(236,72,153,0.14), transparent 60%),
      linear-gradient(120deg, #fdfbff 0%, #f4f7ff 55%, #fff7fb 100%);
}

html, body, [class*="css"]{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* Remove default padding */
.block-container{ max-width: 1250px; padding-top: 1.6rem; padding-bottom: 2.2rem; }

/* Hide Streamlit footer/menu (optional) */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

/* ====== Layout Helpers ====== */
.glass-card{
  background: rgba(255,255,255,0.60);
  border: 1px solid rgba(255,255,255,0.38);
  box-shadow: 0 22px 55px rgba(15,23,42,0.18);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-radius: 26px;
  padding: 1.25rem 1.25rem;
}

.hero-title{
  font-size: 44px;
  font-weight: 900;
  letter-spacing: -0.02em;
  text-align: center;
  margin: 0.25rem 0 0.25rem 0;
  color: #2b1a4a;
}

.hero-subtitle{
  text-align: center;
  font-size: 16px;
  color: rgba(43,26,74,0.70);
  margin-bottom: 1.35rem;
}

.badge{
  display:inline-flex;
  align-items:center;
  gap:.45rem;
  padding:.25rem .75rem;
  border-radius:999px;
  background: rgba(124,58,237,0.12);
  border: 1px solid rgba(124,58,237,0.20);
  color:#4c1d95;
  font-size: 12px;
  font-weight: 600;
}

.badge-muted{
  display:inline-flex;
  align-items:center;
  gap:.45rem;
  padding:.25rem .75rem;
  border-radius:999px;
  background: rgba(2,6,23,0.05);
  border: 1px solid rgba(2,6,23,0.08);
  color: rgba(2,6,23,0.65);
  font-size: 12px;
  font-weight: 600;
}

.divider{
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(2,6,23,0.12), transparent);
  margin: 1rem 0;
}

/* ====== Chat ====== */
.chat-shell{
  height: 66vh;
  overflow: auto;
  padding: 1rem;
  border-radius: 22px;
  background: rgba(255,255,255,0.55);
  border: 1px solid rgba(255,255,255,0.35);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.5);
}

/* message rows */
.msg-row{
  display:flex;
  margin: .55rem 0;
}
.msg-left{ justify-content:flex-start; }
.msg-right{ justify-content:flex-end; }

/* bubbles */
.bubble-user{
  max-width: 72%;
  padding: 10px 14px;
  border-radius: 18px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: #fff;
  box-shadow: 0 10px 18px rgba(79,70,229,0.25);
  font-size: 14.8px;
  line-height: 1.35;
}

.bubble-ai{
  max-width: 72%;
  padding: 10px 14px;
  border-radius: 18px;
  background: rgba(255,255,255,0.82);
  border: 1px solid rgba(99,102,241,0.16);
  color: rgba(2,6,23,0.86);
  box-shadow: 0 10px 18px rgba(2,6,23,0.06);
  font-size: 14.8px;
  line-height: 1.45;
}

.meta{
  font-size: 11px;
  color: rgba(2,6,23,0.45);
  margin-top: 6px;
}

/* Sidebar polish */
section[data-testid="stSidebar"]{
  background: rgba(255,255,255,0.62);
  border-right: 1px solid rgba(255,255,255,0.40);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

/* === Remove top white bar WITHOUT killing sidebar === */
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

    # Conversations: {conv_id: {"title": str, "created_at": float, "messages":[...]}}
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
        "title": title or "New chat",
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
    # Small title = first 6-8 words
    words = user_text.strip().split()
    short = " ".join(words[:8]).strip()
    if len(words) > 8:
        short += "…"
    st.session_state.conversations[cid]["title"] = short or "Chat"


def _safe_get_me():
    """Optional: fetch name/role if backend provides it. If it fails, keep defaults."""
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
        st.markdown("### 💼 Enterprise RAG")
        st.caption("Glass UI • History • Secure chat")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if is_authenticated():
            name = st.session_state.user_name or "User"
            email = st.session_state.user_email or "unknown"
            role = st.session_state.user_role or "user"

            st.markdown(
                f'<span class="badge">✅ Signed in</span> '
                f'<span class="badge-muted">{role}</span>',
                unsafe_allow_html=True,
            )
            st.write(f"**{name}**")
            st.caption(email)

            colA, colB = st.columns(2)
            with colA:
                if st.button("➕ New chat", use_container_width=True):
                    _new_chat()
                    go_to("chat")
            with colB:
                if st.button("🚪 Logout", use_container_width=True):
                    # clear auth only (keep local history optional)
                    st.session_state.token = None
                    st.session_state.user_email = None
                    st.session_state.user_name = None
                    st.session_state.user_role = None
                    st.session_state.page = "landing"
                    st.rerun()

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            st.markdown("#### 🕘 History")
            if not st.session_state.conversations:
                st.caption("No chats yet. Start a new one.")
            else:
                # Sort by created_at desc
                items = sorted(
                    st.session_state.conversations.items(),
                    key=lambda x: x[1]["created_at"],
                    reverse=True
                )

                # Select chat
                labels = [f"{v['title']}" for _, v in items]
                ids = [k for k, _ in items]

                # Keep stable selection
                current = st.session_state.current_conv_id
                if current not in ids:
                    st.session_state.current_conv_id = ids[0] if ids else None
                    current = st.session_state.current_conv_id

                default_index = ids.index(current) if current in ids else 0
                chosen = st.selectbox(
                    "Select a chat",
                    options=ids,
                    index=default_index,
                    format_func=lambda cid: st.session_state.conversations[cid]["title"],
                    label_visibility="collapsed",
                )
                st.session_state.current_conv_id = chosen

                colD, colE = st.columns(2)
                with colD:
                    if st.button("🧹 Clear messages", use_container_width=True):
                        st.session_state.conversations[chosen]["messages"] = []
                        st.rerun()
                with colE:
                    if st.button("🗑️ Delete chat", use_container_width=True):
                        st.session_state.conversations.pop(chosen, None)
                        st.session_state.current_conv_id = None
                        st.rerun()

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # Quick navigation
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
            st.markdown('<span class="badge-muted">🔒 Not signed in</span>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sign in", use_container_width=True):
                    go_to("login")
            with col2:
                if st.button("Register", use_container_width=True):
                    go_to("register")

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.caption("Tip: If you’re stuck on Sign in, use the sidebar to switch to Register.")

# ---------------- PAGES ----------------
def render_landing():
    render_sidebar()

    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Chat securely with your internal knowledge base — fast, clean, and searchable.</div>',
        unsafe_allow_html=True,
    )

    colL, colC, colR = st.columns([1.2, 1.6, 1.2])
    with colC:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ✨ What you get")
        st.write(
            "- **RAG** over your documents (FAISS + metadata)\n"
            "- **Auth** (login/register)\n"
            "- **Chat history** in sidebar\n"
            "- **Minimal UI friction**"
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sign in", use_container_width=True):
                go_to("login")
        with c2:
            if st.button("Create an account", use_container_width=True):
                go_to("register")
        st.markdown("</div>", unsafe_allow_html=True)

    # If already logged in, go chat
    if is_authenticated():
        st.success("You’re already signed in — opening chat…")
        go_to("chat")


def render_login():
    render_sidebar()

    st.markdown('<div class="hero-title">Sign in</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Access your assistant in seconds.</div>', unsafe_allow_html=True)

    colL, colC, colR = st.columns([1.2, 1.6, 1.2])
    with colC:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        topA, topB = st.columns([1, 1])
        with topA:
            st.markdown('<span class="badge">🔑 Login</span>', unsafe_allow_html=True)
        with topB:
            if st.button("Need an account? → Register", use_container_width=True):
                go_to("register")

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in both email and password.")
            else:
                try:
                    r = requests.post(LOGIN_URL, json={"email": email, "password": password}, timeout=20)
                    if r.status_code == 200:
                        data = r.json()
                        # backend returns access_token
                        st.session_state.token = data.get("access_token")
                        st.session_state.user_email = email
                        st.session_state.user_name = email.split("@")[0]
                        st.session_state.user_role = "user"

                        # Optional: fetch /me if exists
                        _safe_get_me()

                        # Ensure at least one chat exists
                        if not st.session_state.conversations:
                            _new_chat()
                        if not st.session_state.current_conv_id:
                            st.session_state.current_conv_id = next(iter(st.session_state.conversations.keys()), None)

                        go_to("chat")
                    else:
                        # Show backend message if available
                        try:
                            msg = r.json().get("detail", "Login failed.")
                        except Exception:
                            msg = "Login failed."
                        st.error(msg)
                except Exception as e:
                    st.error(f"Backend not reachable: {e}")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if st.button("← Back to landing", use_container_width=True):
            go_to("landing")

        st.markdown("</div>", unsafe_allow_html=True)


def render_register():
    render_sidebar()

    st.markdown('<div class="hero-title">Create an account</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">One-time setup — then you chat.</div>', unsafe_allow_html=True)

    colL, colC, colR = st.columns([1.2, 1.6, 1.2])
    with colC:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        topA, topB = st.columns([1, 1])
        with topA:
            st.markdown('<span class="badge">🪪 Register</span>', unsafe_allow_html=True)
        with topB:
            if st.button("Already have an account? → Sign in", use_container_width=True):
                go_to("login")

        with st.form("register_form", clear_on_submit=False):
            name = st.text_input("Full name", placeholder="Your Name")
            email = st.text_input("Email", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="Choose a strong password")
            confirm = st.text_input("Confirm password", type="password", placeholder="Repeat password")
            submitted = st.form_submit_button("Create account", use_container_width=True)

        if submitted:
            if not name or not email or not password or not confirm:
                st.error("Please fill in all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                try:
                    # Backend auth.py ignores a 'role' field (it decides admin/user itself).
                    r = requests.post(
                        REGISTER_URL,
                        json={"name": name, "email": email, "password": password},
                        timeout=20,
                    )
                    if r.status_code in (200, 201):
                        st.success("Account created. You can now sign in.")
                        go_to("login")
                    else:
                        try:
                            msg = r.json().get("detail", "Registration failed.")
                        except Exception:
                            msg = "Registration failed."
                        st.error(msg)
                except Exception as e:
                    st.error(f"Backend not reachable: {e}")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if st.button("← Back to landing", use_container_width=True):
            go_to("landing")

        st.markdown("</div>", unsafe_allow_html=True)


def render_chat():
    render_sidebar()

    if not is_authenticated():
        go_to("login")

    # Ensure we have a chat
    if not st.session_state.conversations:
        _new_chat()
    if not st.session_state.current_conv_id:
        st.session_state.current_conv_id = next(iter(st.session_state.conversations.keys()))

    cid = st.session_state.current_conv_id
    conv = st.session_state.conversations[cid]
    messages = conv["messages"]

    # Header row
    st.markdown('<div class="hero-title">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Ask questions about your internal documents — with a clean, premium chat experience.</div>',
        unsafe_allow_html=True,
    )

    # Info bar
    left, mid, right = st.columns([2.2, 1.2, 1.2])
    with left:
        name = st.session_state.user_name or "User"
        email = st.session_state.user_email or "unknown"
        role = st.session_state.user_role or "user"
        st.markdown(
            f'<span class="badge">👤 {name}</span> <span class="badge-muted">{email}</span> <span class="badge-muted">{role}</span>',
            unsafe_allow_html=True,
        )
    with mid:
        st.markdown(
            f'<span class="badge-muted">🕘 {datetime.fromtimestamp(conv["created_at"]).strftime("%d/%m/%Y %H:%M")}</span>',
            unsafe_allow_html=True
        )
    with right:
        st.markdown(f'<span class="badge">💬 {conv["title"]}</span>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Main chat card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # Empty state
    if not messages:
        st.markdown(
            """
            <div class="chat-shell">
              <div class="bubble-ai">
                👋 Welcome. Ask me anything about your documents (policies, procedures, course content, specs…).
                <div class="meta">Tip: your chat history is in the sidebar.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Render messages inside scrollable shell
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

    st.markdown("</div>", unsafe_allow_html=True)  # close glass-card

    # Input row
    prompt = st.chat_input("Ask something about your documents…")

    if prompt:
        # Append user message
        messages.append({"role": "user", "content": prompt})

        # Update title if first user message
        if len([m for m in messages if m["role"] == "user"]) == 1:
            _set_title_from_first_user_message(cid, prompt)

        # Call backend (LOGIC: SAME, just correct key: query)
        try:
            r = requests.post(
                ASK_URL,
                json={"question": prompt},  
                headers=headers_with_auth(),
                timeout=90,
            )
            if r.status_code == 200:
                answer = r.json().get("answer", "No answer.")
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
