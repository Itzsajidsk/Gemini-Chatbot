import os
import streamlit as st
import google.generativeai as genai
from google.api_core import retry

# Configure Gemini with proper error handling
try:
    # Get API key from Streamlit secrets (for deployment) or environment (for local)
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 API key not configured. Please set GEMINI_API_KEY in secrets or environment variables.")
        st.stop()
    
    genai.configure(api_key=api_key)
    
    # Use Gemini 1.5 Flash model
    model = genai.GenerativeModel('gemini-1.5-flash')

except Exception as e:
    st.error(f"🔌 Connection Error: {str(e)}")
    st.stop()

# Modern UI Configuration
st.set_page_config(
    page_title="✨ Flash Chatbot 1.5",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS styling
st.markdown("""
<style>
    /* Main chat container */
    .main {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* User messages */
    [data-testid="stChatMessageUser"] {
        background-color: #e6f2ff;
        border-left: 4px solid #4b8bf5;
        margin-left: 15%;
    }
    
    /* Assistant messages */
    [data-testid="stChatMessageAssistant"] {
        background-color: #f8f9fa;
        border-left: 4px solid #2e7d32;
        margin-right: 15%;
    }
    
    /* Input box */
    .stChatInput {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        max-width: 700px;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        z-index: 100;
    }
    
    /* Spinner animation */
    .stSpinner > div {
        margin: 0 auto;
        color: #4b8bf5;
        width: 3rem;
        height: 3rem;
    }
    
    /* Flash model indicator */
    .model-indicator {
        position: fixed;
        bottom: 5rem;
        right: 1rem;
        background: #f0f0f0;
        padding: 0.3rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Chatbot UI and Logic
st.title("⚡ Sajid-AI")
st.caption("Powered by Google's fastest AI model")

# Model indicator
st.markdown('<div class="model-indicator">Model: Gemini 1.5 Flash</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm your AI assistant powered by Gemini 1.5 Flash. How can I help you today?"
    })

# Display chat messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# User input handling
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Get AI response with retry logic
    @retry.Retry()
    def generate_response(prompt):
        return model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9
            )
        )
    
    with st.spinner("Thinking..."):
        try:
            response = generate_response(prompt)
            bot_response = response.text
        except Exception as e:
            bot_response = f"⚠️ Sorry, I encountered an error. Please try again later. (Error: {str(e)})"
            st.error(f"Detailed error: {str(e)}")
    
    # Display assistant response
    with st.chat_message("assistant", avatar="⚡"):
        st.markdown(bot_response)
    
    # Add to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Debug section (visible only in development)
if os.getenv("DEBUG_MODE"):
    st.sidebar.markdown("### Debug Info")
    st.sidebar.write("Current model: gemini-1.5-flash")

