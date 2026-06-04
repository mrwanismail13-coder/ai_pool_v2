import math


class AimEngine:

    def __init__(self):
        self.ball_radius = 16

    def normalize(self, dx, dy):
        d = math.sqrt(dx * dx + dy * dy)
        if d == 0:
            return 0, 0
        return dx / d, dy / d

    def compute_ghost(self, target, pocket):

        dx = pocket[0] - target[0]
        dy = pocket[1] - target[1]

        nx, ny = self.normalize(dx, dy)

        return (
            target[0] - nx * self.ball_radius * 2,
            target[1] - ny * self.ball_radius * 2
        )

    def clamp(self, p, bounds):

        x, y = p
        x1, y1, x2, y2 = bounds

        x = max(x1, min(x, x2))
        y = max(y1, min(y, y2))

        return (x, y)

    def solve(self, cue_ball, target_ball, pockets, table_bounds):

        if not cue_ball or not target_ball or not pockets:
            return None

        best = min(pockets, key=lambda p: math.dist(target_ball, p))

        ghost = self.compute_ghost(target_ball, best)

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
