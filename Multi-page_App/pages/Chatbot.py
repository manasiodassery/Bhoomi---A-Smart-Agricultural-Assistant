from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the Google AI API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to get responses from the Google Gemini model
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Page configuration and header
st.set_page_config(page_title="Bhoomi Chatbot", page_icon="💬")
st.image("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Image/bot.png", width=80)
st.title("💬 Bhoomi Chatbot")
st.markdown("**Ask Bhoomi about anything related to farming and agriculture!**")

# Chat interface styling with improved readability
with st.container():
    st.markdown(
        """
        <style>
        .stTextInput, .stButton>button {
            font-size: 16px;
            width: 100%;
        }
        .question, .response {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 16px;
        }
        .question {
            background-color: #d9f1ff; /* Light blue for questions */
            color: #003366; /* Darker blue for text */
        }
        .response {
            background-color: #e9f7ec; /* Light green for responses */
            color: #004d1a; /* Dark green for text */
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

# Chat input box and submit button
with st.form("chat_form"):
    input_question = st.text_input("Type your question:", placeholder="How to improve soil quality?")
    submit = st.form_submit_button("Ask Bhoomi")

# Process and display responses
if submit and input_question:
    # Generate response from Gemini
    response_text = get_gemini_response(input_question)
    
    # Append new question-response pair to history
    st.session_state.history.append({"question": input_question, "response": response_text})

# Display chat history in a user-friendly format
for i, conversation in enumerate(st.session_state.history):
    st.markdown(f"<div class='question'><b>Question {i+1}:</b> {conversation['question']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='response'><b>Response {i+1}:</b> {conversation['response']}</div>", unsafe_allow_html=True)

# Option to clear chat history
if st.button("Clear Chat History"):
    st.session_state.history = []
    st.experimental_rerun()
