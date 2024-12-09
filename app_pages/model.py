import cv2
import time
import streamlit as st
from ultralytics import YOLO
import numpy as np
import google.generativeai as genai
from PIL import Image


st.set_page_config(
  page_title='Welcome!',
  page_icon='👋'
)


IMG_SIZE = 320


# Load YuNet face detection model
yunet_path = 'models/face_detection_yunet_2023mar.onnx'
yunet_face_detector = cv2.FaceDetectorYN_create(yunet_path, "", (IMG_SIZE, IMG_SIZE), score_threshold=0.5)


# Load acne detection model
yolo_path = 'models/acne.pt'
yolo_acne_model = YOLO(yolo_path)


# No acne model
no_acne_yolo_path = 'models/no_acne_model.pt'
yolo_no_acne_model = YOLO(no_acne_yolo_path)


# Gemini model
GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')


def welcome_stream():
  welcome = 'Upload an image and receive treatment suggestions.'
  for word in welcome.split():
    yield word + ' '
    time.sleep(0.1)

def show_welcome():
  col1, col2, col3 = st.columns([1.1,3,1])
  with col2:
    st.write_stream(welcome_stream())


def prepare_image(uploaded_file):
  # Convert UploadedFile object to numpy array
  image = Image.open(uploaded_file)
  image = np.array(image)

  # Convert uploaded image to three channels (BGR format)
  if len(image.shape) == 2:  # Grayscale image
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  elif len(image.shape) == 3:
    if image.shape[2] == 1:  # Single channel grayscale
      image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] == 3:  # RGB image
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif image.shape[2] == 4:   #RGBA image
      image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
  else:
    st.error("Unsupported image format. Please upload a valid image.")
    st.stop() 

  h,w = image.shape[:2]
  new_size = max(h,w)

  padded_image = np.full((new_size, new_size, 3), (0,0,0), dtype=np.uint8)

  # Calculate the position to place the original image
  x_offset = (new_size - w) // 2
  y_offset = (new_size - h) // 2

  padded_image[y_offset:y_offset+h, x_offset:x_offset+w] = image

  return padded_image


def face_detection_crop(padded_image):
  # Resize image for YuNet model
  resized_image = cv2.resize(padded_image, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)

  faces = yunet_face_detector.detect(resized_image)

  # Assert that faces were detected
  if faces[1] is None:
    st.error("No face detected.")
  # Assert that only one face is detected
  elif len(faces[1]) > 1:
    st.error("There can only be one face in the image")
  else:
    for face in faces[1]:
      x,y,w,h = map(int, [face[0], face[1], face[2], face[3]])

      x = max(0, x)
      y = max(0, y)
      w = min(w, IMG_SIZE - x)
      h = min(h, IMG_SIZE - y)

      cropped_image = resized_image[y:y+h, x:x+w]
      return cropped_image


def acne_detection(cropped_image):
  check_none = yolo_no_acne_model.predict(cropped_image)
  if len(check_none[0].boxes) == 0:
    return []

  predictions = yolo_acne_model.predict(cropped_image, conf=0.01, agnostic_nms=True)

  results = set()

  for prediction in predictions:
    for box in prediction.boxes:
      label = int(box.cls)
      results.add(yolo_acne_model.names[label])

  if 'Pores' in results:
    results.remove('Pores')
  return list(results)


def get_acne_treatments(acne_list):
  acne = ', '.join(acne_list)
  prompt = f'''Suggest treatment options for all these acne types: {acne}. Provide clear steps and product recommendations. Try to keep the
  response within 5 bullet points and within 100 words. Add some emojis.'''
  response = gemini_model.generate_content(prompt, stream=True)

  for chunk in response:
    yield chunk.text
    time.sleep(1)


def clear_treatments():
  prompt = f'''I have clear skin. How can I maintain this and keep my skin healthy and clear? Try to keep the response within
  5 bullet points and within 100 words. Add some emojis.'''
  response = gemini_model.generate_content(prompt, stream=True)

  for chunk in response:
    yield chunk.text
    time.sleep(1)


def get_spend(routine):
  prompt = f'''I have these acne conditions and I want to buy OTC products according to these recommendations: {routine}. How much money can 
  I expect to spend in USD? I just want to see bullet points of how much I'm spending for each product. Do not return too many words.'''
  response = gemini_model.generate_content(prompt)
  
  with st.expander('How much might you spend?'):
    st.markdown(response.text)


page_bg_img = f'''
<style>

[data-testid='stFileUploaderDropzone'] {{
background-color: rgba(0,0,0,0);
}}

</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; padding: 0"> BlemishBot </h1>', unsafe_allow_html=True)
if 'model_welcome_executed' not in st.session_state:
  show_welcome()
  st.session_state['model_welcome_executed'] = True
else:
  st.markdown('<h6 style="text-align:center; padding: 0">Upload an image and receive treatment suggestions.</h6>', unsafe_allow_html=True)

image = Image.open('page_images/homepage.png')

left,center,right = st.columns([0.8,2,1])
with center:
  st.image(image)
uploaded_file = st.file_uploader('', type=['png', 'jpg', 'jpeg', 'webp'])

if uploaded_file:
  col1, col2 = st.columns([1,1])
  with col1:
    st.image(uploaded_file)
  padded_image = prepare_image(uploaded_file)
  cropped_image = face_detection_crop(padded_image)
  detected_classes = acne_detection(cropped_image)

  # Display results
  if detected_classes:
    with st.spinner('Analyzing...'):
      with col2:
        time.sleep(1.5)
        for acne_type in detected_classes:
          time.sleep(0.5)
          st.write(f"- {acne_type}")

    st.success("Possible Solutions:")
    with st.spinner('Getting treatments...'):
      response = st.write_stream(get_acne_treatments(detected_classes))
    
    with st.spinner('Calculating price ranges...'):
      get_spend(response)
  else:
    st.success("We detected clear skin! Here's how you can keep your skin healthy 😊")
    st.write_stream(clear_treatments())
    
