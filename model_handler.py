from ultralytics import YOLO
import cv2
import base64

class YOLOModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path, verbose=False)

    def predict(self, image_path):
        results = self.model(image_path)

        img = cv2.imread(image_path)

        objects_detected = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls_id]

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
                cv2.putText(img, f"{label} {conf:.2f}", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                objects_detected.append({
                    'label': label,
                    'conf': conf})

        status = "Dangerous object detected" if len(objects_detected) > 0 else "Safe"

        _, buffer = cv2.imencode('.jpg', img)
        img_bytes = buffer.tobytes()

        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {
            'objects_detected': objects_detected,
            'status': status,
            'bbox_image_base64': img_base64
        }


