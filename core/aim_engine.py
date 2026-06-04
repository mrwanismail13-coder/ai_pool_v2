import math


class AimEngine:

    def __init__(self):
        self.ball_radius = 16

    def normalize(self, dx, dy):
        d = math.sqrt(dx * dx + dy * dy)
        if d == 0:
            return 0, 0
        return dx / d, dy / d

    # =========================
    # 🔥 NEW SAFE GHOST CALC
    # =========================
    def compute_ghost(self, target, pocket):

        dx = pocket[0] - target[0]
        dy = pocket[1] - target[1]

        nx, ny = self.normalize(dx, dy)

        ghost_x = target[0] - nx * self.ball_radius * 2
        ghost_y = target[1] - ny * self.ball_radius * 2

        return (ghost_x, ghost_y)

    # =========================
    # 🔒 CLAMP TO SCREEN
    # =========================
    def clamp(self, point, bounds=None):

        x, y = point

        if bounds:
            x_min, y_min, x_max, y_max = bounds
            x = max(x_min, min(x, x_max))
            y = max(y_min, min(y, y_max))

        return (x, y)

    # =========================
    # 🎯 MAIN SOLVER FIXED
    # =========================
    def solve(self, cue_ball, target_ball, pockets, table_bounds=None):

        if not cue_ball or not target_ball or len(pockets) == 0:
            return None

        # 🎯 choose best pocket (nearest)
        best = min(
            pockets,
            key=lambda p: math.dist(target_ball, p)
        )

        ghost = self.compute_ghost(target_ball, best)

        # 🔒 safety clamp (important fix)
        if table_bounds:
            ghost = self.clamp(ghost, table_bounds)
            target_ball = self.clamp(target_ball, table_bounds)

        return {
            "cue_ball": cue_ball,
            "target_ball": target_ball,
            "ghost_ball": ghost,
            "pocket": best
        }
