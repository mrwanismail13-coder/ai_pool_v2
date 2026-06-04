class BallManager:

    def __init__(self):

        self.object_balls = []
        self.cue_ball = None
        self.pockets = []
        self.cushions = []

    def update(self, detections):

        self.object_balls = []
        self.cue_ball = None
        self.pockets = []
        self.cushions = []

        for det in detections:

            name = det.get("class_name")
            center = det.get("center")

            if not center:
                continue

            if name == "white_cue_ball":
                self.cue_ball = center

            elif name == "object_ball":
                self.object_balls.append(center)

            elif name == "pocket":
                self.pockets.append(center)

            elif name == "cushion":
                self.cushions.append(center)

    def get_cue_ball(self):
        return self.cue_ball

    def get_object_balls(self):
        return self.object_balls

    def get_pockets(self):
        return self.pockets
