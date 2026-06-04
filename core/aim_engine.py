import math


class AimEngine:

    def __init__(self):
        pass

    # =========================
    # DISTANCE
    # =========================
    def distance(self, a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    # =========================
    # NORMALIZE VECTOR
    # =========================
    def normalize(self, dx, dy):
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return 0, 0
        return dx/length, dy/length

    # =========================
    # GHOST BALL CALCULATION
    # =========================
    def compute_ghost_ball(self, cue, target, pocket):

        # direction target -> pocket
        dx = pocket[0] - target[0]
        dy = pocket[1] - target[1]

        nx, ny = self.normalize(dx, dy)

        # ghost ball position (behind target)
        radius = 16  # ball radius approx

        ghost_x = target[0] - nx * radius * 2
        ghost_y = target[1] - ny * radius * 2

        return (ghost_x, ghost_y)

    # =========================
    # MAIN SOLVER
    # =========================
    def solve(self, cue_ball, target_ball, pocket):

        if not cue_ball or not target_ball or not pocket:
            return None

        ghost = self.compute_ghost_ball(cue_ball, target_ball, pocket)

        return {
            "cue_ball": cue_ball,
            "target_ball": target_ball,
            "ghost_ball": ghost,
            "pocket": pocket
        }
