import numpy as np


class TableDetector:

    def __init__(self):
        self.table_box = None  # (x1, y1, x2, y2)

    # =========================
    # SET MANUAL TABLE BOUNDS
    # =========================
    def set_table(self, frame_shape):

        h, w = frame_shape[:2]

        # افتراضي بسيط (ممكن نطوره بعدين)
        margin_x = int(w * 0.10)
        margin_y = int(h * 0.15)

        self.table_box = (
            margin_x,
            margin_y,
            w - margin_x,
            h - margin_y
        )

    # =========================
    # CHECK IF INSIDE TABLE
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
