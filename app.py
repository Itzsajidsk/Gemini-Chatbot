import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini - IMPORTANT: Use the correct model name
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model - Updated model name
model = genai.GenerativeModel('gemini-1.0-pro')  # Changed from 'gemini-pro'

# --- UI Configuration ---
st.set_page_config(
    page_title="🤖 Gemini AI Chatbot",
    page_icon="✨",
    layout="centered"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    .stChatInput {position: fixed; bottom: 2rem;}
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
    }
    [data-testid="stChatMessageUser"] {
        background-color: #e3f2fd;
        border-left: 4px solid #4b8bf5;
    }
    [data-testid="stChatMessageAssistant"] {
        background-color: #f5f5f5;
        border-left: 4px solid #2e7d32;
    }
    .stSpinner > div {
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- Chatbot Logic ---
st.title("💬 Gemini AI Chatbot")
st.caption("Powered by Google's latest AI technology")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            bot_response = f"⚠️ Sorry, I encountered an error: {str(e)}"
    
    # Display bot response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
