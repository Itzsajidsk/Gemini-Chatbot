import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from environment variable
load_dotenv()  

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.0-pro')

# --- UI Config ---
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stChatInput {position: fixed; bottom: 2rem;}
    .stChatMessage {border-radius: 15px; padding: 10px;}
    .user-message {background-color: #e3f2fd;}
    .bot-message {background-color: #f5f5f5;}
    </style>
""", unsafe_allow_html=True)

# --- Chatbot Logic ---
st.title("💬 Gemini AI Chatbot")
st.caption("Ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message..."):
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
            bot_response = f"⚠️ Error: {str(e)}"
    
    # Display bot response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

