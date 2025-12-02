import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Enterprise RAG Assistant", layout="wide")

# ---------------- CUSTOM CSS ----------------
css = """
<style>

body {
    background: linear-gradient(135deg, #f8eaff 0%, #f3dfff 30%, #f8f5ff 100%);
    font-family: 'Inter', sans-serif;
}

/* HEADER */
.header-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #4b2775;
    margin-top: 10px;
}

.header-sub {
    text-align: center;
    font-size: 19px;
    color: #6e4e93;
    margin-bottom: 35px;
}

/* Chat bubbles */
.user-bubble {
    background: #decdfc;
    color: #331d5d;
    padding: 12px 18px;
    border-radius: 18px;
    max-width: 60%;
    margin-left: auto;
    margin-bottom: 14px;
    font-size: 16px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.15);
}

.assistant-bubble {
    background: #f4ecff;
    color: #3c2774;
    padding: 12px 18px;
    border-radius: 18px;
    max-width: 60%;
    margin-right: auto;
    margin-bottom: 14px;
    font-size: 16px;
    border-left: 4px solid #b98cff;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.12);
}

/* Welcome message */
.welcome {
    text-align: center;
    background: #f7f0ff;
    padding: 18px 20px;
    border-radius: 20px;
    margin: 0 auto 25px auto;
    max-width: 55%;
    color: #4b2775;
    font-size: 17px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.07);
}

</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header-title'>Enterprise RAG Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='header-sub'>Chat with your internal knowledge base</div>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------------- CHATGPT-STYLE FLOW ----------------
# Welcome message only if no messages exist
if len(st.session_state["messages"]) == 0:
    st.markdown("<div class='welcome'>Hello! Ask me anything about your internal documents.</div>", unsafe_allow_html=True)

# Render every message in order
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
prompt = st.chat_input("Ask something about your documents...")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Temporary placeholder response
    bot_reply = "This is your assistant speaking. Soon connected to your RAG backend."
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    st.rerun()
