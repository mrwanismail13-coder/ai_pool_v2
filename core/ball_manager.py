class BallManager:

    def __init__(self):

        self.object_balls = []
        self.cue_ball = None

        self.pockets = []
        self.cushions = []

    # =========================
    # UPDATE FROM YOLO (FILTERED)
    # =========================
    def update(self, detections):

        self.object_balls = []
        self.cue_ball = None
        self.pockets = []
        self.cushions = []

        for det in detections:

            class_name = det.get("class_name")

            # =========================
            # CUE BALL
            # =========================
            if class_name == "white_cue_ball":
                self.cue_ball = det

            # =========================
            # OBJECT BALLS
            # =========================
            elif class_name == "object_ball":
                self.object_balls.append(det)

            # =========================
            # POCKETS
            # =========================
            elif class_name == "pocket":
                self.pockets.append(det)

            # =========================
            # CUSHIONS
            # =========================
            elif class_name == "cushion":
                self.cushions.append(det)

    # =========================
    def get_cue_ball(self):
        return self.cue_ball["center"] if self.cue_ball else None

    def get_object_balls(self):
        return [b["center"] for b in self.object_balls]

    def get_pockets(self):
        return [p["center"] for p in self.pockets]
