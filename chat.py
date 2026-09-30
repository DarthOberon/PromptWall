import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    h1 { color: #1E3A8A; font-family: 'Inter', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712010.png", width=80)
    st.title("Chat Settings")
    st.write("Welcome to your modern AI Chat Assistant. Configure your settings here.")
    
    selected_model = st.selectbox("Choose a Model", ["GPT-4 Turbo", "Claude 3 Opus", "Gemini 1.5 Pro"])
    
    st.divider()
    
    # Improved Clear Chat: Resets to the initial greeting instead of a blank screen
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI assistant. How can I help you today?"}
        ]
        st.rerun()
        
    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")

# --- MAIN APP LAYOUT ---
st.title("✨ AI Chat Assistant")
st.caption(f"Currently chatting with: **{selected_model}**")

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI assistant. How can I help you today?"}
    ]

# --- DISPLAY CHAT MESSAGES ---
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- STREAMING GENERATOR ---
# This function yields words one by one for Streamlit's native write_stream
def stream_mock_response(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

# --- CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Type your message here..."):
    
    # 1. Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # 2. Display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        mock_text = f"I am a simulated AI. You said: '{prompt}'. This is where you would connect a real API."
        
        # Streamlit's built-in streaming (much smoother than manual placeholders)
        full_response = st.write_stream(stream_mock_response(mock_text))
        
    # 3. Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": full_response})