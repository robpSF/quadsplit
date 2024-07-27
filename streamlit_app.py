import streamlit as st
from PIL import Image
import io
import zipfile
import requests

# Function to save images to a zip file
def save_images_to_zip(img1, img2, img3, img4, title):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        img_list = [img1, img2, img3, img4]
        names = [f"{title}-1.png", f"{title}-2.png", f"{title}-3.png", f"{title}-4.png"]
        
        for img, name in zip(img_list, names):
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            zip_file.writestr(name, img_buffer.getvalue())
    
    return zip_buffer.getvalue()

# Set up the Streamlit app
st.title("Image Splitter")
st.header("Upload an Image or Enter a URL to Download the Split Parts as a ZIP File")

# Option to choose image source
option = st.selectbox("Choose image source", ("Upload", "URL"))

image = None

if option == "Upload":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
elif option == "URL":
    url = st.text_input("Enter the image URL")
    if url:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))

if image is not None:
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Get image dimensions
    width, height = image.size
    st.write(f"Image dimensions: {width} x {height}")

    # Get title for the images
    title = st.text_input("Enter a title for the images", value="image")

    # Split the image into 4 parts
    img1 = image.crop((0, 0, width//2, height//2))
    img2 = image.crop((width//2, 0, width, height//2))
    img3 = image.crop((0, height//2, width//2, height))
    img4 = image.crop((width//2, height//2, width, height))

    st.write("Split Images:")
    st.image(img1, caption=f"{title}-1", use_column_width=True)
    st.image(img2, caption=f"{title}-2", use_column_width=True)
    st.image(img3, caption=f"{title}-3", use_column_width=True)
    st.image(img4, caption=f"{title}-4", use_column_width=True)

    # Save images to a zip file and provide a download link
    zip_data = save_images_to_zip(img1, img2, img3, img4, title)
    
    st.download_button(
        label="Download Images as ZIP",
        data=zip_data,
        file_name=f"{title}_split_images.zip",
        mime="application/zip"
    )
