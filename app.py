import os
import streamlit as st
import google.generativeai as genai


@st.cache_resource
def load_model():
    return genai.GenerativeModel('gemini-1.0-pro')
# Configure Gemini - using Streamlit secrets for deployment
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("🔑 API key not configured. Please check your deployment settings.")
    st.stop()

# Initialize the model with correct name
try:
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    st.error(f"🚨 Failed to initialize model: {str(e)}")
    st.stop()

# --- Beautiful UI Configuration ---
st.set_page_config(
    page_title="✨ Gemini AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f9f9f9;
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
    }
    
    /* Assistant messages */
    [data-testid="stChatMessageAssistant"] {
        background-color: #ffffff;
        border-left: 4px solid #2e7d32;
    }
    
    /* Input box */
    .stChatInput {
        position: fixed;
        bottom: 2rem;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Spinner */
    .stSpinner > div {
        margin: 0 auto;
        color: #4b8bf5;
    }
</style>
""", unsafe_allow_html=True)

# --- Chatbot Logic ---
st.title("💬 Gemini AI Chatbot")
st.caption("Ask me anything and I'll do my best to help!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your Gemini AI assistant. How can I help you today?"
    })

# Display chat messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Get Gemini response
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(prompt)
            bot_response = response.text
        except Exception as e:
            bot_response = f"⚠️ Sorry, I encountered an error. Please try again. (Error: {str(e)})"
    
    # Display bot response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
