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

    app = QApplication(sys.argv)

    overlay = OverlayWindow()

    camera = dxcam.create(output_idx=0)
    camera.start(target_fps=60)

    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()

    while True:

        frame = camera.get_latest_frame()

        if frame is None:
            continue

        detections = detector.detect(frame)
        manager.update(detections)

        cue = manager.get_cue_ball()
        balls = manager.get_object_balls()
        pockets = manager.get_pockets()

        if cue and balls and pockets:

            result = engine.solve(
                cue_ball=cue,
                target_ball=balls[0],
                pockets=pockets
            )

            if result:
                overlay.set_data(result)

        # 🔥 مهم جدًا: يمنع القفل
        app.processEvents()
        time.sleep(0.01)


if __name__ == "__main__":
    run()
