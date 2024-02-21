from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Configure Gem AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A")
st.header("Chatbot Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input field for user question
input_question = st.text_input("Input: ", key="input")

# Button to ask the question
submit_button = st.button("Ask the question")

# Process user input and display response
if submit_button and input_question:
    response = get_gemini_response(input_question)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_question))
    st.subheader("The Response is:")
    # Concatenate lines of the response into a single block of text
    response_text = "\n".join(chunk.text for chunk in response)
    st.write(response_text)
    st.session_state['chat_history'].append(("Bot", response_text))

