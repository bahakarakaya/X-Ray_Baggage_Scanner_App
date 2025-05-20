# 📦 X-Ray Object Detection System

A computer vision-based X-ray object detection app prototype that identifies potentially dangerous items in X-ray scans. Built with a YOLOv11 custom-trained model and powered by a Python-based backend (Flask) and frontend (Streamlit).

## 🧠 Features

- ✅ Real-time object detection on X-ray images  
- 🧠 Custom-trained YOLOv11 model  
- 📊 Detection confidence & status reports  
- 📸 Annotated output images with bounding boxes  
- 🗃️ Upload your own image or use sample images  
- 💾 Export detection logs as CSV

## 📷 Sample Screenshots
<p align="left">
  <img src="https://github.com/user-attachments/assets/2b4f2ecd-38be-4e12-a894-290ce9b51c5e" width="380"/>
  <img src="https://github.com/user-attachments/assets/25daa5c4-95aa-42b7-ab1a-3e1770674f03" width="380"/>
  <img src="https://github.com/user-attachments/assets/f0a99420-bfb4-4fa7-b5ae-04b420609b8d" width="760"/>
</p>

## 🔍 How It Works

1. **User uploads or selects an image** through the Streamlit frontend.
2. **Image is sent to the Flask API** endpoint at `/predict`.
3. The **YOLOv11 model** performs inference on the image.
4. The **API returns** detected object data and the **annotated image**.
5. The **frontend displays** the detection results and allows **CSV export** of the detected objects.


## 🏗️ Tech Stack

- *Model:* **YOLOv11** (by [Ultralytics](https://github.com/ultralytics))
- *Backend:* **Flask** (for handling prediction requests)
- *Frontend:* **Streamlit** (for the web interface)
- *Database:* **PostgreSQL** (for logging detection history)
- *Image Handling:* **OpenCV**

## 📦 Features

- Upload image files and detect multiple objects.
- View annotated image with bounding boxes.
- Download detection results as CSV.
- (Optional) Log detection history to PostgreSQL.

---

**Data Source**: https://universe.roboflow.com/siewchinyip-outlook-my/sixray
    
 - Trained for 32 epochs on Yolov11m.pt base
 - **Metrics:**
     - Model accuracy measured on validation set
     - mAP50: 0.906
     - mAP50-95: 0.643
     - Precision: 0.92
     - Recall: 0.82

---

```
python app.py
streamlit run app_frontend.py
```
