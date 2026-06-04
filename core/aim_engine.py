import math


class AimEngine:

    def __init__(self):
        self.ball_radius = 16

    # =========================
    # NORMALIZE VECTOR
    # =========================
    def normalize(self, dx, dy):
        d = math.sqrt(dx * dx + dy * dy)
        if d == 0:
            return 0, 0
        return dx / d, dy / d

    # =========================
    # GHOST BALL CALC
    # =========================
    def compute_ghost(self, target, pocket):

        dx = pocket[0] - target[0]
        dy = pocket[1] - target[1]

        nx, ny = self.normalize(dx, dy)

        ghost_x = target[0] - nx * self.ball_radius * 2
        ghost_y = target[1] - ny * self.ball_radius * 2

        return (ghost_x, ghost_y)

    # =========================
    # CLAMP INSIDE TABLE
    # =========================
    def clamp(self, point, bounds):

        x, y = point
        x_min, y_min, x_max, y_max = bounds

        x = max(x_min, min(x, x_max))
        y = max(y_min, min(y, y_max))

        return (x, y)

    # =========================
    # MAIN SOLVER
    # =========================
    def solve(self, cue_ball, target_ball, pockets, table_bounds):

        if not cue_ball or not target_ball or not pockets:
            return None

        # nearest pocket
        best = min(
            pockets,
            key=lambda p: math.dist(target_ball, p)
        )

        ghost = self.compute_ghost(target_ball, best)

        # IMPORTANT FIX: clamp ALL points
        cue_ball = self.clamp(cue_ball, table_bounds)
        target_ball = self.clamp(target_ball, table_bounds)
        ghost = self.clamp(ghost, table_bounds)
        best = self.clamp(best, table_bounds)

        return {
            "cue_ball": cue_ball,
            "target_ball": target_ball,
            "ghost_ball": ghost,
            "pocket": best
        }
