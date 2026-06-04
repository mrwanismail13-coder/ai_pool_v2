import cv2
import numpy as np


class TableDetector:

    def __init__(self):
        self.last_table = None

    def detect_table(self, frame):

        if frame is None:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        # أكبر contour = الطاولة
        largest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest)

        # فلترة بسيطة (منع أخطاء صغيرة)
        if w < 200 or h < 200:
            return None

        self.last_table = (x, y, x + w, y + h)
        return self.last_table

    def is_inside(self, point, table):
        if not table:
            return True

        x, y = point
        x1, y1, x2, y2 = table

        return x1 <= x <= x2 and y1 <= y <= y2
