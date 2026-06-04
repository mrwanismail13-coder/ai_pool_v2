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

    # =========================
    # QT APP
    # =========================
    app = QApplication(sys.argv)

    # =========================
    # OVERLAY WINDOW
    # =========================
    overlay = OverlayWindow()

    # =========================
    # CAMERA INIT
    # =========================
    try:
        camera = dxcam.create(output_idx=0, output_color="BGR")
        camera.start(target_fps=30)
    except Exception as e:
        print("❌ CAMERA ERROR:", e)
        return

    # =========================
    # CORE SYSTEMS
    # =========================
    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()
    table = TableDetector()

    # =========================
    # DEBUG
    # =========================
    frame_counter = 0
    last_time = time.time()

    # =========================
    # MAIN LOOP
    # =========================
    while True:

        frame = camera.get_latest_frame()

        # -------------------------
        # FRAME CHECK
        # -------------------------
        if frame is None:
            app.processEvents()
            time.sleep(0.01)
            continue

        # -------------------------
        # FPS DEBUG
        # -------------------------
        frame_counter += 1
        if time.time() - last_time >= 1:
            print("FPS:", frame_counter, "| FRAME:", frame.shape)
            frame_counter = 0
            last_time = time.time()

        # -------------------------
        # TABLE DETECTION (AUTO)
        # -------------------------
        try:
            table.detect_table(frame)
        except Exception as e:
            print("TABLE ERROR:", e)

        # -------------------------
        # YOLO DETECTION
        # -------------------------
        try:
            detections = detector.detect(frame)
        except Exception as e:
            print("YOLO ERROR:", e)
            detections = []

        # -------------------------
        # FILTER OUTSIDE TABLE
        # -------------------------
        try:
            detections = table.filter_detections(detections)
        except Exception as e:
            print("FILTER ERROR:", e)

        # -------------------------
        # BALL MANAGER
        # -------------------------
        manager.update(detections)

        cue = manager.get_cue_ball()
        balls = manager.get_object_balls()
        pockets = manager.get_pockets()

        # -------------------------
        # AIM ENGINE
        # -------------------------
        if cue and balls and pockets:

            try:
                result = engine.solve(
                    cue_ball=cue,
                    target_ball=balls[0],
                    pockets=pockets,
                    table_bounds=table.table_box
                )

                if result:
                    overlay.set_data(result)

            except Exception as e:
                print("ENGINE ERROR:", e)

        # -------------------------
        # UPDATE UI
        # -------------------------
        app.processEvents()
        time.sleep(0.005)


if __name__ == "__main__":

    try:
        run()
    except Exception as e:
        print("FATAL ERROR:", e)
        input("Press Enter to exit...")
