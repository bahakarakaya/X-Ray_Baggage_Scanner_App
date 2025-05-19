import streamlit as st
import pandas as pd
import requests
import os
from PIL import Image
import base64
from io import BytesIO
from db.database import get_all_predictions

st.title("📦 X-Ray Security System 📦")

EXAMPLE_DIR = "example_xray_photos"
example_files = os.listdir(EXAMPLE_DIR)

upload_option = st.radio(
    "Select Photo",
    ("📂 Upload Photo", "🖼️ Use Sample Photos")
)
selected_image = None

tab1, tab2 = st.tabs(["📤 X-Ray Analysis", "📜 Prediction History"])

def detect_objects_func(uploaded_file_or_image, img_placeholder):
    if st.button("🕵️‍♀️ Detect Risky Objects"):
        with st.spinner("Image is getting processed... Wait for it"):

            api_url = 'http://127.0.0.1:5000/predict'  # flask api address
            if isinstance(uploaded_file_or_image, Image.Image):
                img_byte_arr = BytesIO()
                uploaded_file_or_image.save(img_byte_arr, format='JPEG')
                files = {'image': ('image.jpg', img_byte_arr.getvalue(), 'image/jpg')}
            else:
                files = {'image': (uploaded_file_or_image.name, uploaded_file_or_image.getvalue(),
                                   uploaded_file_or_image.type)}

            try:
                response = requests.post(api_url, files=files)
                response.raise_for_status()
                result = response.json()

                st.success("Prediction is complete ✅")
                st.subheader("🚨 Detected objects: ")
                for obj in result["objects_detected"]:
                    st.write(f"- **{obj['label']}** ({round(obj['conf'] * 100)}% confidence)")

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


with tab1:
    if upload_option == "📂 Upload Photo":
        uploaded_file = st.file_uploader("Pls upload a X-Ray image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            #Show img on screen
            image = Image.open(uploaded_file)
            img_placeholder = st.image(image, caption="Original image", use_container_width=True)

            detect_objects_func(uploaded_file, img_placeholder)

    else:
        example_choice = st.selectbox("Select example photo:", example_files)
        if example_choice:
            img_path = os.path.join(EXAMPLE_DIR, example_choice)
            selected_image = Image.open(img_path)

            if selected_image:
                img_placeholder = st.image(selected_image, caption="Selected Photo", use_column_width=True)

                detect_objects_func(selected_image, img_placeholder)

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

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as .csv",
            data=csv,
            file_name='xray_pred_history.csv',
            mime='text/csv'
        )

    else:
        st.info("No predictions have been registered yet.")