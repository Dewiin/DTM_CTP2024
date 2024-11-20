import streamlit as st

home_page = st.Page(
  page='app_pages/model.py',
  title='Home',
  default=True
)

chatbot_page = st.Page(
  page='app_pages/blemish_chatbot.py',
  title='BlemishBot AI'
)

info_page = st.Page(
  page='app_pages/acne_info.py',
  title='Acne & Info'
)

pg = st.navigation(pages=[home_page, chatbot_page, info_page])

pg.run()
