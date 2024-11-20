import streamlit as st
import json
import requests
import base64
from PIL import Image
import io

#CONSTANTS
PREDICTED_LABELS = ['High squamous intra-epithelial lesion','Low squamous intra-epithelial lesion','Negative for Intraepithelial malignancy','Squamous cell carcinoma']
IMAGE_URL = "https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=HSIL%20of%20the%20Cervix%2C%20Nuclear-to-Cytoplasmic%20Ratio&p=BOOKS&id=430728_HSIL01.jpg"

PREDICTED_LABELS.sort()

def get_prediction(image_data):
  #replace your image classification ai service endpoint URL
  url = 'https://askai.aiclub.world/38aa96f6-83f5-4369-b80f-1937d42323a7'  
  r = requests.post(url, data=image_data)
  response = r.json()['predicted_label']
  score = r.json()['score']
  #print("Predicted_label: {} and confidence_score: {}".format(response,score))
  return response, score



#Building the website

#title of the web page
st.title("Cancer Cell Image Classification")

#setting the main picture
st.image(IMAGE_URL, caption = "Cancer Cell Classification")

#about the web app
st.header("About the Web App")

#details about the project
with st.expander("Web App 🌐"):
    st.subheader("Cancer Cell Predictions")
    st.write("""My app is designed to predict and classify cancer cell images into one of the following categories :
    1.High squamous intra-epithelial lesion
    2.Low squamous intra-epithelial lesion
    3.Negative for Intraepithelial malignancy
    4.Squamous cell carcinoma""")

#setting file uploader
image =st.file_uploader("Upload a cancer cell image",type = ['jpg','png','jpeg'])
if image:
  #converting the image to bytes
  img = Image.open(image).convert('RGB') #ensuring to convert into RGB as model expects the image to be in 3 channel
  buf = io.BytesIO()
  img.save(buf,format = 'JPEG')
  byte_im = buf.getvalue()

  #converting bytes to b64encoding
  payload = base64.b64encode(byte_im)

  #file details
  file_details = {
    "file name": image.name,
    "file type": image.type,
    "file size": image.size
  }

  #write file details
  #st.write(file_details) #uncomment if you need to show file details

  #setting up the image
  st.image(img)

  #predictions
  response, scores = get_prediction(payload)

  #if you are using the model deployment in navigator
  #you need to define the labels
  response_label = PREDICTED_LABELS[response]

  st.metric("Prediction Label",response_label)
  st.metric("Confidence Score", max(scores))
  
