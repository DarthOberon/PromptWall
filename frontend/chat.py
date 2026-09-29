import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PromptWall",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* ---------- PromptWall styling ---------- */

/* Let Streamlit handle light/dark colors */
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    border-right: 1px solid rgba(128, 128, 128, 0.20);
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: var(--text-color);
}

/* Chat messages */
.stChatMessage {
    border-radius: 12px;
}

/* Chat input */
[data-testid="stChatInput"] {
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
}

/* Keep Streamlit's header consistent with the selected theme */
header[data-testid="stHeader"] {
    background-color: var(--background-color);
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712010.png", width=80)
    st.title("PromptWall")
    
    st.divider()

    st.caption("USER")
    st.write("**Student 101**")

    st.caption("Model")
    selected_model = "Gemini 3.5 Flash-Lite"
    st.write("Gemini 3.5 Flash-lite")

    st.caption("Security")    
    st.markdown("<span style='color:#22c55e; font-weight:600;'>● Active</span>", unsafe_allow_html=True)
    # st.write("**Active**")

    st.caption("MODE")
    st.write("**Read-only**")
    
    st.divider()
    
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    

# --- MAIN APP LAYOUT ---
st.title("🛡️ PromptWall")
st.caption(f"Currently chatting with: **{selected_model}**")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI assistant. How can I help you today?"}
    ]

for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"],unsafe_allow_html=True)

if prompt := st.chat_input("Type your message here..."):
    
   
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    
   
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        rows = []
        
        user = {"user_id": 1, "role":"Student","student_id":101}
        
        try:
            response = requests.post("http://127.0.0.1:5000/api/ask", json={"user":user, "message": prompt}, timeout=30)
            result = response.json()

            if result.get("decision") == "ALLOW":
                rows = result.get("rows",[])

                full_response = (
                    f"**Security Decision:** "
                    f"<span style='color: green; font-weight:700;'>ALLOW</span>\n\n"
                    f"**Reason:** {result.get('reason')}\n\n"
                    f"**Database Results:**\n\n"
                    
                )
            else:
                full_response = (
                    f"**Security Decision:** "
                    f"<span style='color: red; font-weight:700;'>BLOCK</span>\n\n"
                    f"**Reason:** {result.get('reason')}"
                )

        except requests.RequestException as exc:
            full_response = f"Error: Could not connect to PromptWall backend:`{exc}`"

        message_placeholder.markdown(full_response, unsafe_allow_html=True) 
        if result.get("decision") == "ALLOW" and rows:
            st.dataframe(rows, use_container_width=True,hide_index=True)
            

                          
        
   
    st.session_state.messages.append({"role": "assistant", "content": full_response})