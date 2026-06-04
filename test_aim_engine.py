from core.aim_engine import AimEngine


def run_test():

    print("\n==============================")
    print("AIM ENGINE TEST START")
    print("==============================\n")

    engine = AimEngine()

    # =========================
    # 🧪 FIXED TEST DATA
    # =========================

    cue_ball = (300, 500)

    target_ball = (600, 400)

    pockets = [
        (50, 50),      # top-left
        (960, 50),     # top-right
        (50, 540),     # bottom-left
        (960, 540),    # bottom-right
        (500, 50),     # top-middle
        (500, 540),    # bottom-middle
    ]

    print("Cue Ball:", cue_ball)
    print("Target Ball:", target_ball)
    print("Pockets:", pockets)
    print("\n------------------------------")

    result = engine.solve(
        cue_ball=cue_ball,
        target_ball=target_ball,
        pockets=pockets
    )

    if not result:
        print("❌ NO RESULT")
        return

    print("\n==============================")
    print("RESULT")
    print("==============================")

    print("Cue Ball:", result["cue_ball"])
    print("Target Ball:", result["target_ball"])
    print("Ghost Ball:", result["ghost_ball"])
    print("Pocket:", result["pocket"])

    print("\n==============================")
    print("AIM TEST FINISHED")
    print("==============================\n")


if __name__ == "__main__":
    run_test()
