import streamlit as st
from PIL import Image
import io
import zipfile

# Function to save images to a zip file
def save_images_to_zip(img1, img2, img3, img4):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        img_list = [img1, img2, img3, img4]
        names = ["Top-Left.png", "Top-Right.png", "Bottom-Left.png", "Bottom-Right.png"]
        
        for img, name in zip(img_list, names):
            img = img.resize((500, 500))  # Resize image to 500x500
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            zip_file.writestr(name, img_buffer.getvalue())
    
    return zip_buffer.getvalue()

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
    st.image(img1.resize((500, 500)), caption="Top-Left", use_column_width=True)
    st.image(img2.resize((500, 500)), caption="Top-Right", use_column_width=True)
    st.image(img3.resize((500, 500)), caption="Bottom-Left", use_column_width=True)
    st.image(img4.resize((500, 500)), caption="Bottom-Right", use_column_width=True)

    # Save images to a zip file and provide a download link
    zip_data = save_images_to_zip(img1, img2, img3, img4)
    
    st.download_button(
        label="Download Images as ZIP",
        data=zip_data,
        file_name="split_images.zip",
        mime="application/zip"
    )
