import streamlit as st
from PIL import Image

model_page = st.Page(
  page='app_pages/model.py',
  icon='💥',
  title='BlemishBot - Model',
  default=True
)

chatbot_page = st.Page(
  page='app_pages/blemish_chatbot.py',
  icon='💬',
  title='BlemishAI - Chatbot'
)

info_page = st.Page(
  page='app_pages/acne_info.py',
  icon='📖',
  title='Acne & Info'
)

pg = st.navigation(pages=[model_page, chatbot_page, info_page])

pg.run()
