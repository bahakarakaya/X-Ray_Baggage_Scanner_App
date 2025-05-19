import streamlit as st
import pandas as pd
import requests
from PIL import Image
import base64
from io import BytesIO
from db.database import get_all_predictions

st.title("📦 X-Ray Security System 📦")

uploaded_file = st.file_uploader("Pls upload a X-Ray image", type=["jpg", "jpeg", "png"])
tab1, tab2 = st.tabs(["📤 X-Ray Analysis", "📜 Prediction History"])

with tab1:
    if uploaded_file:
        #Show img on screen
        image = Image.open(uploaded_file)
        img_placeholder = st.image(image, caption="Original image", use_container_width=True)

        if st.button("🕵️‍♀️ Detect Risky Objects"):
            with st.spinner("Image is getting processed... Wait for it"):

                api_url = 'http://127.0.0.1:5000/predict'   #flask api address
                files = {'image': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                try:
                    response = requests.post(api_url, files=files)
                    response.raise_for_status()
                    result = response.json()

                    st.success("Prediction is complete ✅")
                    st.subheader("🚨 Detected objects: ")
                    for obj in result["objects_detected"]:
                        st.write(f"- **{obj['label']}** ({round(obj['conf']*100)}% confidence)")

                    st.subheader("Current Status:")
                    st.write(result["status"])

                    if "bbox_image_base64" in result:
                        img_bytes = base64.b64decode(result["bbox_image_base64"])
                        bbox_image = Image.open(BytesIO(img_bytes))
                        img_placeholder.image(bbox_image, caption="Detected Objects", use_container_width=True)

                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")

                except Exception as e:
                    st.error(f"An error has occured: {e}. Response: {response.text}")

with tab2:
    st.subheader("📊 Previous Predictions")
    predictions = get_all_predictions()

    if predictions:
        df = pd.DataFrame(predictions, columns=["image_id", "objects_detected", "status", "created_at"])
        df["created_at"] = pd.to_datetime(df["created_at"])
        st.dataframe(df, column_config={
            "image_id": "Image Id",
            "objects_detected": "Detected Objects",
            "status": "Status",
            "created_at": "Created at"
        }, use_container_width=True)
    else:
        st.info("No predictions have been registered yet.")