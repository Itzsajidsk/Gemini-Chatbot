import streamlit as st
import google.generativeai as genai
import os
import streamlit as st
import google.generativeai as genai

# Configure Gemini using environment variable
genai.configure(api_key=os.environ['AIzaSyAZz7kRJv2shDmIRzn4wProovHGTqtGyKk'])

# Configure Gemini
genai.configure(api_key='AIzaSyAZz7kRJv2shDmIRzn4wProovHGTqtGyKk')  # Replace with your actual API key
model = genai.GenerativeModel('gemini-pro')

# Set up Streamlit app
st.title("Gemini AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get Gemini response
    response = model.generate_content(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response.text)
    # Add assistant response to chat history

    st.session_state.messages.append({"role": "assistant", "content": response.text})

