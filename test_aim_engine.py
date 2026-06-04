import cv2
import numpy as np
from core.aim_engine import AimEngine


def run_test():

    print("\n==============================")
    print("AIM ENGINE TEST START")
    print("==============================\n")

    # =========================
    # 🖼️ Create blank table image
    # =========================
    img = np.zeros((600, 1000, 3), dtype=np.uint8)

    # =========================
    # 🎯 Test Data
    # =========================
    cue_ball = (300, 500)
    target_ball = (600, 400)
    pockets = [(50, 50), (960, 50), (50, 540), (960, 540), (500, 50), (500, 540)]

    print("Cue Ball:", cue_ball)
    print("Target Ball:", target_ball)
    print("Pockets:", pockets)
    print("\n------------------------------\n")

    # =========================
    # 🧠 Engine
    # =========================
    engine = AimEngine()

    result = engine.solve(
        cue_ball=cue_ball,
        target_ball=target_ball,
        pockets=pockets,
        table_bounds=(0, 0, img.shape[1], img.shape[0])
    )

    if not result:
        print("NO RESULT")
        return

    cue = result["cue_ball"]
    target = result["target_ball"]
    ghost = result["ghost_ball"]
    pocket = result["pocket"]

    print("==============================")
    print("RESULT")
    print("==============================")
    print("Cue Ball:", cue)
    print("Target Ball:", target)
    print("Ghost Ball:", ghost)
    print("Pocket:", pocket)
    print("\n==============================")

    # =========================
    # 🎨 DRAWING
    # =========================

    # cue
    cv2.circle(img, cue, 8, (255, 255, 255), -1)

    # target
    cv2.circle(img, target, 8, (0, 255, 0), -1)

    # ghost
    ghost_pt = (int(ghost[0]), int(ghost[1]))
    cv2.circle(img, ghost_pt, 8, (255, 255, 0), -1)

    # pocket
    cv2.circle(img, pocket, 8, (0, 0, 255), -1)

    # lines
    cv2.line(img, cue, target, (0, 255, 0), 2)
    cv2.line(img, target, pocket, (0, 0, 255), 2)

    # =========================
    # 💾 SAVE IMAGE
    # =========================
    output_path = "aim_result.jpg"
    cv2.imwrite(output_path, img)

    print("RESULT IMAGE SAVED:", output_path)

    print("\n==============================")
    print("AIM TEST FINISHED")
    print("==============================\n")


if __name__ == "__main__":
    run_test()
