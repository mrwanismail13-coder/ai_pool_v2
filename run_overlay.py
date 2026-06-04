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
    table = TableDetector()

    frame_counter = 0
    last_log = time.time()

    while True:

        frame = camera.get_latest_frame()

        if frame is None:
            app.processEvents()
            time.sleep(0.01)
            continue

        # =========================
        # INIT TABLE ON FIRST FRAME
        # =========================
        if table.table_box is None:
            table.set_table(frame.shape)
            print("TABLE SET:", table.table_box)

        # FPS DEBUG
        frame_counter += 1
        if time.time() - last_log >= 1:
            print("FPS:", frame_counter, "| FRAME:", frame.shape)
            frame_counter = 0
            last_log = time.time()

        # =========================
        # YOLO
        # =========================
        detections = detector.detect(frame)

        # =========================
        # FILTER STEP 🔥
        # =========================
        detections = table.filter_detections(detections)

        # =========================
        # BALL MANAGER
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
                pockets=pockets,
                table_bounds=table.table_box
            )

            overlay.set_data(result)

        app.processEvents()
        time.sleep(0.005)


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("FATAL ERROR:", e)
        input("Press Enter to exit...")
