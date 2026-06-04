import numpy as np


class TableFilter:
    """
    Simple heuristic filter to remove UI noise and outside-table detections
    """

    def __init__(self):
        self.table_box = None  # (x1, y1, x2, y2)

    # =========================
    # STEP 1: estimate table area
    # =========================
    def estimate_table(self, detections):
        object_balls = [
            d["center"] for d in detections
            if d["class_name"] == "object_ball"
        ]

        if len(object_balls) < 3:
            return None

        xs = [p[0] for p in object_balls]
        ys = [p[1] for p in object_balls]

        margin = 80

        self.table_box = (
            max(min(xs) - margin, 0),
            max(min(ys) - margin, 0),
            max(xs) + margin,
            max(ys) + margin
        )

        return self.table_box

    # =========================
    # STEP 2: filter detections
    # =========================
    def filter(self, detections):

        if not self.table_box:
            return detections

        x1, y1, x2, y2 = self.table_box

        filtered = []

        for d in detections:
            cx, cy = d["center"]

            # inside table only
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                filtered.append(d)

        return filtered
