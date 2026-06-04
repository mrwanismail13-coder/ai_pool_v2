import cv2
import numpy as np


class TableDetector:

    def __init__(self):
        self.table_box = None  # (x1, y1, x2, y2)

    # =========================
    # AUTO DETECT TABLE
    # =========================
    def detect_table(self, frame):

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 🎯 green table mask (8ball pool default)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        # clean noise
        kernel = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        # largest contour = table
        largest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest)

        self.table_box = (x, y, x + w, y + h)

        return self.table_box

    # =========================
    # CHECK INSIDE TABLE
    # =========================
    def inside_table(self, point):

        if self.table_box is None:
            return True

        x, y = point
        x1, y1, x2, y2 = self.table_box

        return x1 <= x <= x2 and y1 <= y <= y2

    # =========================
    # FILTER DETECTIONS
    # =========================
    def filter_detections(self, detections):

        if self.table_box is None:
            return detections

        filtered = []

        for det in detections:
            cx, cy = det.get("center", (0, 0))

            if self.inside_table((cx, cy)):
                filtered.append(det)

        return filtered
