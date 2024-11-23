import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(
  page_icon='🤖'
)

GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def welcome_stream():
  welcome = 'How can I help you?'
  for word in welcome.split():
    yield word + ' '
    time.sleep(0.1)

def show_welcome():
  col1, col2, col3 = st.columns([1.85,2,1])
  with col2:
    st.write_stream(welcome_stream())

# Title
st.markdown('<h1 style="text-align: center; padding: 0"> BlemishAI</h1>', unsafe_allow_html=True)

if "chatbot_welcome_executed" not in st.session_state:
  show_welcome()
  st.session_state["chatbot_welcome_executed"] = True
else:
  st.markdown('<h6 style="text-align: center;"> How can I help you? </h6>', unsafe_allow_html=True)



# Gemini response
def generate_response(user_input):
  try:
    context = get_chat_history(st.session_state.chat_history)

    prompt = f'''The following context is a conversation between you and a user: {context}.
    Answer this new input: {user_input}, add some emojis. You are designed for skincare advice. 
    Respectfully decline questions that are off-topic and unrelated to skincare. 
    Do not say anything offensive and always respond respectfully.'''
    response = gemini_model.generate_content(prompt, stream=True)

    for chunk in response:
      yield chunk.text
      time.sleep(0.05)
  except:
    st.error("There was an error processing your response.")

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


# Prevent typing when a response is generating
if 'is_generating' not in st.session_state:
  st.session_state.is_generating = False


# Display chat messages from history on app rerun
for chat in st.session_state.chat_history:
  with st.chat_message(chat['role']):
    st.markdown(chat['content'])


user_input = st.chat_input('E.g., How can I treat acne scars?', disabled=st.session_state.is_generating)
if user_input or st.session_state.is_generating:
  if not st.session_state.is_generating:
    # Add user input to chat history
    st.session_state.is_generating = True 
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
      st.markdown(user_input)
      st.rerun()

  with st.chat_message('assistant'):
    st.session_state.is_generating = False
    response = st.write_stream(generate_response(user_input))
    # Add chat response to chat history 
    st.session_state.chat_history.append({'role': 'assistant', 'content': response})


  # Limit chat history to the last 10 messages
  st.session_state.chat_history = st.session_state.chat_history[-10:]
  st.rerun()







