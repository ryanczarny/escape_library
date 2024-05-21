import base64
from pathlib import Path
import streamlit as st

# Function to encode the image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as file:
        binary_content = file.read()
    return base64.b64encode(binary_content).decode()

def background_image():
    # Path to your image file
    image_path = Path("background.png").resolve()

    # Verify the image path
    if not image_path.is_file():
        st.error(f"Image not found at {image_path}")
    else:
        # Encode the image
        base64_image = get_base64_of_bin_file(image_path)

        # Define the CSS with the base64-encoded image
        background_image = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
            position: relative;
            z-index: 1;
        }}
        [data-testid="stAppViewContainer"] > .main::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;  /* Cover the viewport */
            background-position: center;  
            background-repeat: no-repeat;
            opacity: 0.1;  /* 50% opacity */
            z-index: -1;  /* Ensure it is behind the content */
        }}
        </style>
        """

        # Apply the CSS with st.markdown
        st.markdown(background_image, unsafe_allow_html=True)