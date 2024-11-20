import streamlit as st

model_page = st.Page(
  page='app_pages/model.py',
  title='BlemishBot - Model',
  default=True
)

chatbot_page = st.Page(
  page='app_pages/blemish_chatbot.py',
  title='BlemishAI - Chatbot'
)

info_page = st.Page(
  page='app_pages/acne_info.py',
  title='Acne & Info'
)

pg = st.navigation(pages=[model_page, chatbot_page, info_page])

pg.run()
