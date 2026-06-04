import sys
import time
import dxcam

from PyQt6.QtWidgets import QApplication

from core.detector import BallDetector
from core.ball_manager import BallManager
from core.aim_engine import AimEngine
from overlay.overlay_window import OverlayWindow


def run():

    print("🚀 STARTING OVERLAY SYSTEM...")

    # =========================
    # INIT CAMERA
    # =========================
    camera = dxcam.create(output_idx=0)
    camera.start(target_fps=60)

    # =========================
    # AI MODULES
    # =========================
    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()

    # =========================
    # OVERLAY UI
    # =========================
    app = QApplication(sys.argv)
    overlay = OverlayWindow()

    print("🎯 OVERLAY RUNNING...")

    # =========================
    # MAIN LOOP
    # =========================
    while True:

        frame = camera.get_latest_frame()

        if frame is None:
            continue

        # =========================
        # DETECTION
        # =========================
        detections = detector.detect(frame)
        manager.update(detections)

        cue = manager.get_cue_ball()
        balls = manager.get_object_balls()
        pockets = manager.get_pockets()

        # =========================
        # AIM SOLVER
        # =========================
        if cue and len(balls) > 0 and len(pockets) > 0:

            result = engine.solve(
                cue_ball=cue,
                target_ball=balls[0],
                pockets=pockets
            )

            if result:
                overlay.set_data(result)

        # =========================
        # UI REFRESH
        # =========================
        app.processEvents()
        time.sleep(0.01)
