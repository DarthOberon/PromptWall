
import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="PromptWall",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Each browser session gets its own HTTP cookie jar.
if "http" not in st.session_state:
    st.session_state.http = requests.Session()

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

http = st.session_state.http

st.markdown("""
<style>
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}
[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    border-right: 1px solid rgba(128, 128, 128, 0.20);
}
[data-testid="stSidebar"] * {
    color: var(--text-color);
}
.stChatMessage {
    border-radius: 12px;
}
[data-testid="stChatInput"] {
    border-radius: 12px;
}
.stButton > button {
    border-radius: 8px;
}
header[data-testid="stHeader"] {
    background-color: var(--background-color);
}
</style>
""", unsafe_allow_html=True)


def login_screen():
    st.title("🛡️ PromptWall")
    st.caption("Sign in to access the AI database assistant.")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="e.g. student_101")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in", use_container_width=True)

    if submitted:
        try:
            response = http.post(
                f"{API_BASE}/api/login",
                json={"username": username, "password": password},
                timeout=15,
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.user = data["user"]
                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": (
                            f"Welcome, **{data['user']['username']}**! "
                            "How can I help you today?"
                        ),
                    }
                ]
                st.rerun()
            elif response.status_code == 401:
                st.error("Invalid username or password.")
            else:
                st.error(
                    response.json().get(
                        "error", "Login failed. Please try again."
                    )
                )
        except requests.RequestException:
            st.error("Could not connect to the PromptWall backend.")

if not st.session_state.user:
    login_screen()
    st.stop()


user = st.session_state.user

with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712010.png",
        width=80,
    )
    st.title("PromptWall")
    st.divider()

    st.caption("SIGNED IN AS")
    st.write(f"**{user['username']}**")
    st.caption("Role")
    st.write(f"**{user['role']}**")

    selected_model = "Gemini 3.5 Flash-Lite"
    st.caption("Model")
    st.write(selected_model)

    st.caption("Security")
    st.markdown(
        "<span style='color:#22c55e; font-weight:600;'>● Active</span>",
        unsafe_allow_html=True,
    )

    st.caption("MODE")
    st.write("**Read-only**")
    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("Log out", use_container_width=True):
        try:
            http.post(f"{API_BASE}/api/logout", timeout=10)
        except requests.RequestException:
            pass

        http.cookies.clear()
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()


st.title("🛡️ PromptWall")
st.caption(f"Currently chatting with: **{selected_model}**")

for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        result = None
        rows = []

        try:
            response = http.post(
                f"{API_BASE}/api/ask",
                json={"message": prompt},
                timeout=30,
            )

            if response.status_code == 401:
                st.session_state.user = None
                st.error("Your session has expired. Please log in again.")
                st.rerun()

            result = response.json()

            if result.get("decision") == "ALLOW":
                rows = result.get("rows", [])
                full_response = (
                    "**Security Decision:** "
                    "<span style='color: green; font-weight:700;'>ALLOW</span>\n\n"
                    f"**Reason:** {result.get('reason')}\n\n"
                    "**Database Results:**"
                )
            else:
                full_response = (
                    "**Security Decision:** "
                    "<span style='color: red; font-weight:700;'>BLOCK</span>\n\n"
                    f"**Reason:** {result.get('reason', 'REQUEST_BLOCKED')}"
                )

        except requests.RequestException:
            full_response = "Error: Could not connect to PromptWall backend."
        except ValueError:
            full_response = "Error: Backend returned an invalid response."

        message_placeholder.markdown(full_response, unsafe_allow_html=True)

        if result and result.get("decision") == "ALLOW" and rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
