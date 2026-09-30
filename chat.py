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
# Adding some custom styling to make the UI look more modern
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Adjusting chat message styling */
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Header styling */
    h1 {
        color: #1E3A8A;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712010.png", width=80)
    st.title("Chat Settings")
    st.write("Welcome to your modern AI Chat Assistant. Configure your settings here.")
    
    # Model selection (mockup)
    selected_model = st.selectbox("Choose a Model", ["GPT-4 Turbo", "Claude 3 Opus", "Gemini 1.5 Pro"])
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")

# --- MAIN APP LAYOUT ---
st.title("✨ AI Chat Assistant")
st.caption(f"Currently chatting with: **{selected_model}**")

# --- SESSION STATE INITIALIZATION ---
# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI assistant. How can I help you today?"}
    ]

# --- DISPLAY CHAT MESSAGES ---
# Display messages from history on app rerun
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- CHAT INPUT & LOGIC ---
# Accept user input
if prompt := st.chat_input("Type your message here..."):
    
    # 1. Display user message in chat message container
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # 2. Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 3. Display assistant response in chat message container
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate a streaming response from an AI model
        mock_response = f"I am a simulated AI. You said: '{prompt}'. This is where you would connect an API (like OpenAI, Anthropic, or Google) to generate real responses based on the conversation history."
        
        # Stream the response word by word
        for chunk in mock_response.split():
            full_response += chunk + " "
            time.sleep(0.05) # Simulate typing speed
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
            
        # Final display without the cursor
        message_placeholder.markdown(full_response)
        
    # 4. Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})