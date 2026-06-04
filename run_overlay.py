import sys
import time
import dxcam

from PyQt6.QtWidgets import QApplication

from core.detector import BallDetector
from core.ball_manager import BallManager
from core.aim_engine import AimEngine
from core.table_detector import TableDetector
from overlay.overlay_window import OverlayWindow


def run():

    print("🚀 STARTING OVERLAY SYSTEM...")

    app = QApplication(sys.argv)
    overlay = OverlayWindow()

    camera = dxcam.create(output_idx=0, output_color="BGR")
    camera.start(target_fps=30)

    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()
    table_detector = TableDetector()

    frame_counter = 0
    last_log_time = time.time()

    while True:

        frame = camera.get_latest_frame()

        if frame is None:
            app.processEvents()
            continue

        # =========================
        # TABLE DETECTION 🔥
        # =========================
        table = table_detector.detect_table(frame)

        frame_counter += 1
        if time.time() - last_log_time >= 1:
            print("FPS:", frame_counter)
            frame_counter = 0
            last_log_time = time.time()

        # =========================
        # YOLO DETECTION
        # =========================
        detections = detector.detect(frame)

        # =========================
        # FILTER BY TABLE 🔥
        # =========================
        if table:
            filtered = []
            for d in detections:
                if table_detector.is_inside(d["center"], table):
                    filtered.append(d)
            detections = filtered

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

        app.processEvents()
        time.sleep(0.005)


if __name__ == "__main__":

    try:
        run()
    except Exception as e:
        print("FATAL ERROR:", e)
        input("Press Enter to exit...")
