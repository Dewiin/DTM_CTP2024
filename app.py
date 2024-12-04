import streamlit as st
from PIL import Image

image = Image.open('page_images/homepage.png')
st.logo(image, size='large')

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

another_test = st.Page(
  page='app_pages/fun.py',
  icon='📖',
  title='fun'
)
pg = st.navigation(pages=[model_page, chatbot_page, info_page, another_test])

pg.run()
