import streamlit as st
import google.generativeai as genai
import time
import os

st.set_page_config(
  page_icon='🤖'
)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')


# Title
st.markdown('<h1 style="text-align: center; padding: 0"> BlemishAI</h1>', unsafe_allow_html=True)
st.markdown('<h6 style="text-align: center;"> How can I help you?</h1>', unsafe_allow_html=True)


# Gemini response
def generate_response(user_input):
  context = get_chat_history(st.session_state.chat_history)

  prompt = f'''The following context is a conversation between you and a user: {context}.
  Answer this new input: {user_input}. You are designed for skincare advice. 
  Respectfully decline questions that are off-topic and unrelated to skincare. 
  Do not say anything offensive and always respond respectfully.'''
  response = gemini_model.generate_content(prompt, stream=True)

  for chunk in response:
    yield chunk.text
    time.sleep(0.05)

def get_chat_history(history):
  context = ''

  for chat in history:
    role = chat['role']
    content = chat['content']
    context += f'{role} : {content}\n'
  return context


# Initialize chat history
if 'chat_history' not in st.session_state:
  st.session_state.chat_history = []


# Display chat messages from history on app rerun
for chat in st.session_state.chat_history:
  with st.chat_message(chat['role']):
    st.markdown(chat['content'])


user_input = st.chat_input('E.g., How can I treat acne scars?')
if user_input:
  # Add user input to chat history
  st.session_state.chat_history.append({'role': 'user', 'content': user_input})
  with st.chat_message('user'):
    st.session_state.is_generating = True 
    st.markdown(user_input)

  with st.chat_message('assistant'):
    response = st.write_stream(generate_response(user_input))
    # Add chat response to chat history
    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
    st.session_state.is_generating = False





