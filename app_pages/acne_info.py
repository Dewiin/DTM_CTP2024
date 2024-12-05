import streamlit as st
from PIL import Image

st.markdown('<h1 style="text-align:center; padding:0">📖 Acne & Info 📖</h1>', unsafe_allow_html=True)
st.markdown('<h6 style="text-align:center; padding:0">Read About Skin Conditions</h6>', unsafe_allow_html=True)

# Define image paths and descriptions
image_data = {
        "Papules": {
            "path": "page_images/papulesBetter.webp",
            "description": '''Papules are small, red, inflamed bumps on the skin. They occur when a hair follicle becomes clogged and
             irritated, often without visible pus. Papules feel firm to the touch and may be tender or sensitive.'''
        },
        "Pustules": {
            "path": "page_images/pustules.webp",
            "description": '''Pustules are similar to papules but contain pus at their centers, appearing as white or yellow bumps surrounded 
             by red, inflamed skin. They are a classic sign of inflammatory acne and may burst, releasing their contents.'''
        },
        "Nodules": {
            "path": "page_images/nodules.webp",
            "description": '''Nodules are large, hard, and painful lumps that form deep beneath the skin's surface. They result from severe inflammation 
             in clogged pores and do not contain pus. Nodules often require medical treatment due to their severity and potential for scarring.'''
        },
        "Cysts": {
            "path": "page_images/cysts.webp",
            "description": '''Cysts are the most severe form of acne, characterized by large, soft, pus-filled lesions that develop deep under the skin.
             They are often painful and can lead to significant scarring if not properly treated by a dermatologist.'''
        },
        "Blackheads": {
            "path": "page_images/blackheads.webp",
            "description": '''Blackheads are non-inflammatory acne lesions that appear as small, dark spots. They form when hair follicles 
             are clogged with oil and dead skin cells, but the pore remains open, allowing oxidation to turn the clog black.'''
        },
        "Acne Scars": {
            "path": "page_images/acne_scars.jpg",
           "description": '''
        Acne scars are the long-term effects of severe or improperly treated acne. They can appear as:
        <ul>
            <li><b><i>Atrophic scars:</i></b> Depressions in the skin, such as boxcar scars, ice pick scars, or rolling scars.</li>
            <li><b><i>Hypertrophic scars:</i></b> Raised, thickened areas of skin, typically from an overproduction of collagen.</li>
            <li><b><i>Post-inflammatory hyperpigmentation (PIH):</i></b> Dark spots left behind after acne heals, more common in darker skin tones.</li>
        </ul>
        '''
        },
    }

# Radio buttons for selecting skin condition
selected_condition = st.radio(
    label = '',
    options=list(image_data.keys()),
    horizontal=True,
)

# Get the selected image path and description
selected_image_path = image_data[selected_condition]["path"]
selected_description = image_data[selected_condition]["description"]

# Open and resize the image
with Image.open(selected_image_path) as img:
    resized_img = img.resize((800, 400))  # Resize to 800x400

# Display the resized image
st.image(resized_img, use_container_width=True)

# Display the larger caption below the image
st.markdown(f"<h3 style='text-align: center;'>{selected_condition}</h3>", unsafe_allow_html=True)

# Display the description below the image
st.markdown(f"<p style='text-align: left;'>{selected_description}</p>", unsafe_allow_html=True)