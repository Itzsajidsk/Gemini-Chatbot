import os
import streamlit as st
import google.generativeai as genai
from google.api_core import retry




# Add this function to your imports
# def load_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# In your app code, right before UI components:
# load_css("style.css")
# Add this right after your imports
# CUSTOM_CSS = """
# <style>
#     /* Main container */
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
#         font-family: 'Segoe UI', Roboto, sans-serif;
#     }
    
#     /* Chat container */
#     .stChatFloatingInputContainer {
#         background: transparent !important;
#         box-shadow: none !important;
#     }
    
#     /* Chat messages */
#     .stChatMessage {
#         border-radius: 18px !important;
#         padding: 16px 20px !important;
#         margin: 12px 0 !important;
#         max-width: 80%;
#         position: relative;
#         animation: fadeIn 0.3s ease-out;
#     }
    
#     /* User messages */
#     [data-testid="stChatMessageUser"] {
#         background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%) !important;
#         color: white !important;
#         margin-left: auto;
#         border-bottom-right-radius: 4px !important;
#         box-shadow: 0 4px 12px rgba(106, 17, 203, 0.2);
#     }
    
#     /* Assistant messages */
#     [data-testid="stChatMessageAssistant"] {
#         background: white !important;
#         margin-right: auto;
#         border-bottom-left-radius: 4px !important;
#         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
#         border-left: 4px solid #6a11cb;
#     }
    
#     /* Input box */
#     .stChatInput {
#         position: fixed !important;
#         bottom: 2rem !important;
#         left: 50% !important;
#         transform: translateX(-50%) !important;
#         width: 80% !important;
#         max-width: 700px !important;
#         background: white !important;
#         padding: 1rem 1.5rem !important;
#         border-radius: 50px !important;
#         box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
#         border: none !important;
#         font-size: 1rem !important;
#     }
    
#     /* Input box focus */
#     .stChatInput:focus {
#         outline: none !important;
#         box-shadow: 0 4px 20px rgba(106, 17, 203, 0.2) !important;
#     }
    
#     /* Spinner */
#     .stSpinner > div {
#         width: 2.5rem !important;
#         height: 2.5rem !important;
#         border-width: 3px !important;
#         border-color: #6a11cb transparent transparent transparent !important;
#     }
    
#     /* Avatar styling */
#     .stChatMessage .avatar {
#         width: 32px !important;
#         height: 32px !important;
#         font-size: 16px !important;
#         background: white !important;
#         color: #6a11cb !important;
#         display: flex !important;
#         align-items: center !important;
#         justify-content: center !important;
#         border-radius: 50% !important;
#         box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
#     }
    
#     /* Header styling */
#     .stApp header {
#         background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%) !important;
#         color: white !important;
#     }
    
#     /* Animation */
#     @keyframes fadeIn {
#         from { opacity: 0; transform: translateY(10px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
    
#     /* Model indicator */
#     .model-indicator {
#         position: fixed;
#         bottom: 5.5rem;
#         right: 1.5rem;
#         background: white;
#         padding: 0.5rem 1rem;
#         border-radius: 50px;
#         font-size: 0.8rem;
#         color: #6a11cb;
#         font-weight: 600;
#         box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }
    
#     .model-indicator::before {
#         content: "";
#         display: block;
#         width: 10px;
#         height: 10px;
#         background: #6a11cb;
#         border-radius: 50%;
#         animation: pulse 1.5s infinite;
#     }
    
#     @keyframes pulse {
#         0% { transform: scale(1); opacity: 1; }
#         50% { transform: scale(1.2); opacity: 0.7; }
#         100% { transform: scale(1); opacity: 1; }
#     }
# </style>
# """

# # Add this right before your Streamlit components
# st.markdown(CUSTOM_CSS, unsafe_allow_html=True)














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
st.caption("Powered by fastest AI model")

# Model indicator
st.markdown('<div class="model-indicator">Model: Gemini 1.5 Flash</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm your AI assistant. How can I help you today?"
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
    st.sidebar.write("Current model: 1.5-flash Model")







