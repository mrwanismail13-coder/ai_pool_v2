import math


class AimEngine:

    def __init__(self):
        self.ball_radius = 16

    # =========================
    # VECTOR HELPERS
    # =========================
    def dist(self, a, b):
        return math.dist(a, b)

    def normalize(self, dx, dy):
        d = math.sqrt(dx * dx + dy * dy)
        if d == 0:
            return 0, 0
        return dx / d, dy / d

    def angle_score(self, cue, target, pocket):

        # vectors
        v1 = (target[0] - cue[0], target[1] - cue[1])
        v2 = (pocket[0] - target[0], pocket[1] - target[1])

        # normalize
        n1 = self.normalize(*v1)
        n2 = self.normalize(*v2)

        # dot product = alignment
        dot = n1[0] * n2[0] + n1[1] * n2[1]

        # closer to 1 = better
        return dot

    # =========================
    # IMPROVED GHOST BALL
    # =========================
    def compute_ghost(self, target, pocket):

        dx = pocket[0] - target[0]
        dy = pocket[1] - target[1]

        nx, ny = self.normalize(dx, dy)

        return (
            target[0] - nx * self.ball_radius * 2,
            target[1] - ny * self.ball_radius * 2
        )

    # =========================
    # BEST POCKET SELECTION
    # =========================
    def choose_best_pocket(self, cue, target, pockets):

        best_pocket = None
        best_score = -999

        for p in pockets:

            distance_score = -self.dist(target, p)

            angle_score = self.angle_score(cue, target, p)

            total_score = angle_score * 2 + distance_score * 0.01

            if total_score > best_score:
                best_score = total_score
                best_pocket = p

        return best_pocket

    # =========================
    # MAIN SOLVER
    # =========================
    def solve(self, cue_ball, target_ball, pockets):

        if not cue_ball or not target_ball or len(pockets) == 0:
            return None

        best_pocket = self.choose_best_pocket(
            cue_ball,
            target_ball,
            pockets
        )

        ghost = self.compute_ghost(target_ball, best_pocket)

        return {
            "cue_ball": cue_ball,
            "target_ball": target_ball,
            "ghost_ball": ghost,
            "pocket": best_pocket
        }
