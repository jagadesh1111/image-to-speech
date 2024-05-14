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

    
    filewrite = open("String.txt", "w")

    for z, a in enumerate(data2.splitlines()):

        

        if z != 0:

           

            a = a.split()

            

            if len(a) == 12:

                

                x, y = int(a[6]), int(a[7])

                w, h = int(a[8]), int(a[9])

                

                cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 1)

                

                cv2.putText(img2, a[11], (x - 15, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)

                

                filewrite.write(a[11] + " ")

    filewrite.close()

    
    summarize = transformers.pipeline("summarization")
    

    fileread = open("String.txt", "r")

    language = 'en'

    line = fileread.read()
    with open("summary.txt", "w") as f:
        f.write(summarize(line, max_length=len(line)+100, min_length=1, do_sample=False)[0]['summary_text'])
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
    
            with audio_file_path.open("rb") as f:
                audio_bytes = f.read()

   
            st.audio(audio_bytes, format="audio/mpeg")
    
    cv2.imshow('Image output', img2)

    cv2.waitKey(0)


def save_uploaded_image(image, filename):
  """Saves the uploaded image to the specified filename as JPG."""
  with open(os.path.join("uploads", filename+".jpeg"), "wb") as f:
    image.save(f, format="JPEG")  
    st.success(f"Image saved as: {filename}")


uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    try:
    
        image_bytes = uploaded_image.getvalue()

    
        image = Image.open(io.BytesIO(image_bytes))

    
        st.image(image, caption="Uploaded Image", use_column_width=True)

    
        if st.button("Summarize Image"):
      
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
        st.error(f"Error saving image: {e}") 


    




