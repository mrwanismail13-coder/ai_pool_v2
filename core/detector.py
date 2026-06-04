from ultralytics import YOLO
import numpy as np

from core.config import MODEL_PATH, YOLO_CONFIDENCE


class BallDetector:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

        self.model = YOLO(str(MODEL_PATH))

        print("=" * 50)
        print("YOLO LOADED")
        print("MODEL:", MODEL_PATH)
        print("CLASSES:", self.model.names)
        print("=" * 50)

    def detect(self, frame):

        if frame is None:
            return []

        try:
            results = self.model.predict(
                source=frame,
                conf=YOLO_CONFIDENCE,
                verbose=False
            )
        except Exception as e:
            print("YOLO PREDICT ERROR:", e)
            return []

        detections = []

        if not results or results[0].boxes is None:
            return detections

        r = results[0]

        for box in r.boxes:

            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            detections.append({
                "class_id": cls_id,
                "class_name": self.model.names[cls_id],
                "confidence": conf,
                "center": (cx, cy),
                "bbox": (int(x1), int(y1), int(x2), int(y2))
            })

        return detections
