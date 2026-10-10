import os
import io
from contextlib import redirect_stdout
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def llm_code(question):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a SymPy code writer. Write Python code using sympy to solve the user's math question. Rules: import sympy as sp at the start; use print() to display the answer; output ONLY the Python code, no markdown, no backticks."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


if "messages" not in st.session_state:
    st.session_state.messages = []
if "prefill" not in st.session_state:
    st.session_state.prefill = ""


st.markdown("""
<style>
/* ===== GLOBAL BACKGROUND ===== */
html, body, [data-testid="stAppViewContainer"], .main, .stApp {
    background-color: #1a1a1a !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] {
    background-color: #1a1a1a !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #1a1a1a !important;
    border-right: 1px solid #262626 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 20px !important;
}

[data-testid="stSidebar"] * {
    color: #d4d4d4 !important;
}

[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    padding: 0 8px !important;
}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #888888 !important;
    font-size: 12px !important;
    padding: 0 8px !important;
}

/* Sidebar buttons — like DeepSeek */
[data-testid="stSidebar"] button {
    background-color: transparent !important;
    color: #d4d4d4 !important;
    border: none !important;
    border-radius: 8px !important;
    text-align: left !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    margin: 2px 0 !important;
}

[data-testid="stSidebar"] button:hover {
    background-color: #2a2a2a !important;
}

/* New Chat button — special */
[data-testid="stSidebar"] button[kind="secondary"]:first-of-type {
    background-color: #2a2a2a !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-weight: 500 !important;
}

/* ===== MAIN CONTENT — narrow like DeepSeek ===== */
.block-container {
    max-width: 750px !important;
    padding-top: 20px !important;
    padding-bottom: 140px !important;
    margin: 0 auto !important;
}

/* Hide main headings if any */
.block-container > h1:first-child {
    display: none !important;
}

/* ===== AVATARS HATAAO ===== */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"],
[data-testid*="stChatMessageAvatar"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* ===== CHAT MESSAGE BASE ===== */
.stChatMessage {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* ===== USER BUBBLE ===== */
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
    background-color: #2f2f2f !important;
    border-radius: 18px !important;
    padding: 10px 16px !important;
    margin: 12px 0 12px auto !important;
    max-width: 70% !important;
    width: fit-content !important;
    display: block !important;
}

.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"],
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdown"],
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown,
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) .stMarkdownContainer,
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown > div {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    width: auto !important;
    min-width: 0 !important;
}

.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) p,
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) span,
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) div {
    color: #f5f5f5 !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
    margin: 0 !important;
    padding: 0 !important;
    word-break: break-word !important;
}

/* ===== AI MESSAGE ===== */
.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) {
    background-color: transparent !important;
    padding: 8px 0 !important;
    margin: 12px 0 !important;
    max-width: 100% !important;
}

.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) p,
.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) span {
    color: #ececec !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    margin: 0 !important;
}

.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) .stAlert {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    color: #ececec !important;
}

/* ===== BOTTOM INPUT AREA ===== */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stChatInputContainer"] {
    background-color: #1a1a1a !important;
}

[data-testid="stChatInput"] {
    background-color: #2f2f2f !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 24px !important;
    padding: 12px 20px !important;
    max-width: 750px !important;
    margin: 0 auto !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 90% !important;
}

[data-testid="stChatInputTextArea"] {
    background-color: transparent !important;
    color: #e5e5e5 !important;
    border: none !important;
    font-size: 15px !important;
}

[data-testid="stChatInputTextArea"]::placeholder {
    color: #888888 !important;
}

/* ===== DIVIDERS ===== */
hr {
    border-color: #262626 !important;
    margin: 12px 0 !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #1a1a1a;
}
::-webkit-scrollbar-thumb {
    background: #3a3a3a;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #4a4a4a;
}

/* ===== FONT ===== */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}
/* ===== EXPANDER — code ke liye ===== */
[data-testid="stExpander"] {
    background-color: transparent !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    margin-top: 8px !important;
    margin-bottom: 8px !important;
}

[data-testid="stExpander"] summary {
    color: #888888 !important;
    font-size: 13px !important;
    padding: 8px 12px !important;
}

[data-testid="stExpander"] summary:hover {
    color: #d4d4d4 !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background-color: transparent !important;
    padding: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🧮 ARYABHATA-AI")
    st.caption("Math made simple")

    st.write("")
    if st.button("➕  New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("**📜 History**")
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    if user_msgs:
        for msg in reversed(user_msgs[-10:]):
            text = msg["content"][:30] + ("..." if len(msg["content"]) > 30 else "")
            st.caption(f"• {text}")
    else:
        st.caption("Nothing yet...")

    st.divider()

    st.markdown("**📚 Examples**")
    examples = [
        "Solve x^2 - 9 = 0",
        "Derivative of x^3",
        "Integrate sin(x)",
        "Factor x^2 - 5x + 6",
        "Limit of sin(x)/x",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
            st.session_state.prefill = ex
            st.rerun()


# ===== MAIN AREA =====
# Koi title nahi — seedha chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            if "code" in message and message["code"]:
                with st.expander("📝 View SymPy Code"):
                    st.code(message["code"], language="python")
            st.write(message["content"])
        else:
            st.write(message["content"])

user_input = st.chat_input("Message ARYABHATA-AI")

if st.session_state.prefill:
    user_input = st.session_state.prefill
    st.session_state.prefill = ""

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
        
    })

    with st.spinner("Thinking..."):
        code = llm_code(user_input)

    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            exec(code)
        answer = buffer.getvalue()
    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "code" : code
    })

    st.rerun()