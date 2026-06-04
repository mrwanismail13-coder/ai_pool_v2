import sys
import time
import dxcam

from PyQt6.QtWidgets import QApplication

from core.detector import BallDetector
from core.ball_manager import BallManager
from core.aim_engine import AimEngine
from overlay.overlay_window import OverlayWindow
from core.table_filter import TableFilter


def run():

    print("🚀 STARTING OVERLAY SYSTEM...")

    app = QApplication(sys.argv)

    overlay = OverlayWindow()

    camera = dxcam.create(output_idx=0, output_color="BGR")
    camera.start(target_fps=30)

    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()
    table_filter = TableFilter()

    frame_counter = 0
    last_time = time.time()

    while True:

        frame = camera.get_latest_frame()

        if frame is None:
            app.processEvents()
            time.sleep(0.01)
            continue

        # =========================
        # DETECTION
        # =========================
        detections = detector.detect(frame)

        # =========================
        # ESTIMATE TABLE FIRST
        # =========================
        table_filter.estimate_table(detections)

        # =========================
        # FILTER NOISE
        # =========================
        detections = table_filter.filter(detections)

        # =========================
        # UPDATE BALLS
        # =========================
        manager.update(detections)

        cue = manager.get_cue_ball()
        balls = manager.get_object_balls()
        pockets = manager.get_pockets()

        # =========================
        # AIM ENGINE
        # =========================
        if cue and balls and pockets:

            result = engine.solve(
                cue_ball=cue,
                target_ball=balls[0],
                pockets=pockets
            )

            if result:
                overlay.set_data(result)

        # =========================
        # UI LOOP
        # =========================
        app.processEvents()
        time.sleep(0.01)


if __name__ == "__main__":

    try:
        run()
    except Exception as e:
        print("FATAL ERROR:", e)
        input("Press Enter...")
