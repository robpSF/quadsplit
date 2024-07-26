import streamlit as st
from PIL import Image

# Load the image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Get image dimensions
    width, height = image.size
    st.write(f"Image dimensions: {width} x {height}")

    # Split the image into 4 parts
    img1 = image.crop((0, 0, width//2, height//2))
    img2 = image.crop((width//2, 0, width, height//2))
    img3 = image.crop((0, height//2, width//2, height))
    img4 = image.crop((width//2, height//2, width, height))

    st.write("Split Images:")
    st.image(img1, caption="Top-Left", use_column_width=True)
    st.image(img2, caption="Top-Right", use_column_width=True)
    st.image(img3, caption="Bottom-Left", use_column_width=True)
    st.image(img4, caption="Bottom-Right", use_column_width=True)
