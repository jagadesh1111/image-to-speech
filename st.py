import streamlit as st
from PIL import Image
import cv2
from pathlib import Path
import pytesseract
import io
from gtts import gTTS
import transformers
import time
import os

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def texttospeech():

    # Open the file with write permission
    # wordtwo()
    filewrite = open("String.txt", "w")

    for z, a in enumerate(data2.splitlines()):

        # Counter

        if z != 0:

            # Converts 'data1' string into a list stored in 'a'

            a = a.split()

            # Checking if array contains a word

            if len(a) == 12:

                # Storing values in the right variables

                x, y = int(a[6]), int(a[7])

                w, h = int(a[8]), int(a[9])

                # Display bounding box of each word

                cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 1)

                # Display detected word under each bounding box

                cv2.putText(img2, a[11], (x - 15, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)

                # Writing to the file

                filewrite.write(a[11] + " ")

    filewrite.close()

    # Open the file with read permission
    summarize = transformers.pipeline("summarization")
    

    fileread = open("String.txt", "r")

    language = 'en'

    line = fileread.read()
    with open("summary.txt", "w") as f:
        f.write(summarize(line, max_length=len(line), min_length=1, do_sample=False)[0]['summary_text'])
    with open("summary.txt", "r") as f:
        l = f.read()
        if(len(line)<20):
            l = line
        if l != " ":

            fileread.close()

            speech = gTTS(text=l, lang=language, slow=False)

            speech.save("test.mp3")
        st.write(l)
        audio_file_path = Path("test.mp3")
        if audio_file_path.exists():
    # Read the MP3 file
            with audio_file_path.open("rb") as f:
                audio_bytes = f.read()

    # Display the audio player
            st.audio(audio_bytes, format="audio/mpeg")
    # Output the bounding box with the image
    cv2.imshow('Image output', img2)

    cv2.waitKey(0)

# Upload image with file type restriction
def save_uploaded_image(image, filename):
  """Saves the uploaded image to the specified filename as JPG."""
  with open(os.path.join("uploads", filename+".jpeg"), "wb") as f:
    image.save(f, format="JPEG")  # Explicitly set format to JPEG
    st.success(f"Image saved as: {filename}")# Display success message

# Upload image with file type restriction
uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    try:
    # Read the uploaded image as bytes
        image_bytes = uploaded_image.getvalue()

    # Convert bytes to PIL Image object
        image = Image.open(io.BytesIO(image_bytes))

    # Display the uploaded image (optional)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Save button and logic
        if st.button("Summarize Image"):
      # Generate a unique filename with extension (optional, adjust as needed)
            filename, extension = os.path.splitext(uploaded_image.name)
            filename = f"{filename}_{int(time.time())}{extension}"
            uploads_dir = os.path.join("uploads")
            save_uploaded_image(image, "img")
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            img2 = cv2.imread("uploads/img.jpeg")
            h2Img, w2Img, none2 = img2.shape
            box2 = pytesseract.image_to_boxes(img2)
            data2 = pytesseract.image_to_data(img2)
            texttospeech()
    except Exception as e:
        st.error(f"Error saving image: {e}")  # Handle potential errors

# Create the "uploads" directory if it doesn't exist (optional, adjust path)
    




