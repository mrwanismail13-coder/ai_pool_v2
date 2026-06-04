import sys
import time
import traceback
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
    camera.start(target_fps=30)

    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()

    frame_count = 0

    while True:
        try:

            frame = camera.get_latest_frame()

            if frame is None:
                continue

            detections = detector.detect(frame)
            manager.update(detections)

            cue = manager.get_cue_ball()
            balls = manager.get_object_balls()
            pockets = manager.get_pockets()

            # debug مهم جدًا
            frame_count += 1
            if frame_count % 60 == 0:
                print("FRAME OK:", frame_count, "detections:", len(detections))

            if cue and balls and pockets:

                result = engine.solve(
                    cue_ball=cue,
                    target_ball=balls[0],
                    pockets=pockets
                )

                if result:
                    overlay.set_data(result)

            app.processEvents()
            time.sleep(0.01)

        except Exception as e:
            print("❌ ERROR LOOP:")
            print(traceback.format_exc())
            time.sleep(1)


if __name__ == "__main__":
    run()
