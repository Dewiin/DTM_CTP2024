import streamlit as st
from PIL import Image
import time

st.set_page_config(
  page_icon='📖',
)

def welcome_stream():
  welcome = 'Learn about different acne conditions.'
  for word in welcome.split():
    yield word + ' '
    time.sleep(0.1)

def show_welcome():
  col1, col2, col3 = st.columns([1.2,2,1])
  with col2:
    st.write_stream(welcome_stream())


st.markdown('<h1 style="text-align:center; padding:0">Acne & Info</h1>', unsafe_allow_html=True)

if "info_welcome_executed" not in st.session_state:
  show_welcome()
  st.session_state["info_welcome_executed"] = True
else:
  st.markdown('<h6 style="text-align:center;">Learn about different acne conditions</h6>', unsafe_allow_html=True)


papules, pustules, nodules = st.columns(spec=3)
cysts, blackheads, acne_scars = st.columns(spec=3, vertical_alignment='top')
with papules:
  st.markdown('<h4 style="text-align:center;">Papules</h4', unsafe_allow_html=True)
  with st.expander('', expanded=True):
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
      image = Image.open('acne_types_images/papules.webp')
      st.image(image)

    st.write('''Papules are small, red, inflamed bumps on the skin. They occur when a hair follicle becomes clogged and
             irritated, often without visible pus. Papules feel firm to the touch and may be tender or sensitive.''')
    

with pustules:
  st.markdown('<h4 style="text-align:center;">Pustules</h4', unsafe_allow_html=True)
  with st.expander('', expanded=True):
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
      image = Image.open('acne_types_images/pustules.webp')
      st.image(image)

    st.write('''Pustules are similar to papules but contain pus at their centers, appearing as white or yellow bumps surrounded 
             by red, inflamed skin. They are a classic sign of inflammatory acne and may burst, releasing their contents.''')
    

with nodules:
  st.markdown('<h4 style="text-align:center;">Nodules</h4', unsafe_allow_html=True)
  with st.expander('', expanded=True):
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
      image = Image.open('acne_types_images/nodules.webp')
      st.image(image)

    st.write('''Nodules are large, hard, and painful lumps that form deep beneath the skin's surface. They result from severe inflammation 
             in clogged pores and do not contain pus. Nodules often require medical treatment due to their severity and potential for scarring.''')


with cysts:
  st.markdown('<h4 style="text-align:center;">Cysts</h4', unsafe_allow_html=True)
  with st.expander('', expanded=True):
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
      image = Image.open('acne_types_images/cysts.webp')
      st.image(image)
    st.write('''Cysts are the most severe form of acne, characterized by large, soft, pus-filled lesions that develop deep under the skin.
             They are often painful and can lead to significant scarring if not properly treated by a dermatologist.''')


with blackheads:
  st.markdown('<h4 style="text-align:center;">Blackheads</h4', unsafe_allow_html=True)
  with st.expander('', expanded=True):
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
      image = Image.open('acne_types_images/blackheads.webp')
      st.image(image)
    st.write('''Blackheads are non-inflammatory acne lesions that appear as small, dark spots. They form when hair follicles 
             are clogged with oil and dead skin cells, but the pore remains open, allowing oxidation to turn the clog black.''')


with acne_scars:  
  st.markdown('<h4 style="text-align:center;">Acne Scars</h4', unsafe_allow_html=True)
  with st.expander('', expanded=True):
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
      image = Image.open('acne_types_images/acne_scars.jpg')
      image = image.resize([652,443])
      st.image(image)
    st.markdown('''Acne scars are the long-term effects of severe or improperly treated acne. They can appear as:<br>
                <b><i>Atrophic scars:</i></b> Depressions in the skin, such as boxcar scars, ice pick scars, or rolling scars.<br>
                <b><i>Hypertrophic scars:</i></b> Raised, thickened areas of skin, typically from an overproduction of collagen.<br>
                <b><i>Post-inflammatory hyperpigmentation (PIH):</i></b> Dark spots left behind after acne heals, more common in darker skin tones.''', 
                unsafe_allow_html=True)