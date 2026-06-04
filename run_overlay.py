import sys
import cv2
import dxcam
from PyQt6 import QtWidgets

from core.detector import BallDetector
from core.ball_manager import BallManager
from core.aim_engine import AimEngine
from overlay.overlay_window import OverlayWindow


def run_overlay():

    app = QtWidgets.QApplication(sys.argv)

    # =========================
    # INIT SYSTEM
    # =========================
    camera = dxcam.create()
    camera.start(target_fps=60)

    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()

    overlay = OverlayWindow()

    print("🚀 OVERLAY MODE STARTED")

    # =========================
    # MAIN LOOP
    # =========================
    while True:

        frame = camera.get_latest_frame()

        if frame is None:
            continue

        detections = detector.detect(frame)
        manager.update(detections)

        cue = manager.get_cue_ball()
        objects = manager.get_object_balls()
        pockets = manager.get_pockets()

        if cue and len(objects) > 0:

            target = objects[0]

            result = engine.solve(
                cue_ball=cue["center"],
                target_ball=target["center"],
                pockets=[p["center"] for p in pockets],
                other_balls=[b["center"] for b in objects[1:]]
            )

            if result:
                overlay.update_data(result, [p["center"] for p in pockets])

        app.processEvents()


if __name__ == "__main__":
    run_overlay()
