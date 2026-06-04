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
    # 🖥️ QT APP
    # =========================
    app = QApplication(sys.argv)

    # =========================
    # 🎯 OVERLAY
    # =========================
    overlay = OverlayWindow()

    # =========================
    # 🎥 CAMERA INIT (STABLE)
    # =========================
    try:
        camera = dxcam.create(output_idx=0, output_color="BGR")
        camera.start(target_fps=30)
    except Exception as e:
        print("❌ DXCAM ERROR:", e)
        return

    # =========================
    # 🧠 CORE SYSTEMS
    # =========================
    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()

    frame_counter = 0
    last_log_time = time.time()

    # =========================
    # 🔄 MAIN LOOP
    # =========================
    while True:

        frame = camera.get_latest_frame()

        # =========================
        # 🧪 FRAME CHECK
        # =========================
        if frame is None:
            print("FRAME: None ❌")
            app.processEvents()
            time.sleep(0.01)
            continue

        # =========================
        # 🧪 DEBUG FPS LOG
        # =========================
        frame_counter += 1
        if time.time() - last_log_time >= 1:
            print("FRAME OK:", frame.shape, "| FPS:", frame_counter)
            frame_counter = 0
            last_log_time = time.time()

        # =========================
        # 🎯 YOLO DETECTION
        # =========================
        try:
            detections = detector.detect(frame)
        except Exception as e:
            print("DETECT ERROR:", e)
            detections = []

        # 🧪 TEST DETECTIONS
        # print("DETECTIONS:", len(detections))

        # =========================
        # 🎱 BALL MANAGER
        # =========================
        manager.update(detections)

        cue = manager.get_cue_ball()
        balls = manager.get_object_balls()
        pockets = manager.get_pockets()

        # =========================
        # 🎯 AIM ENGINE
        # =========================
        if cue and balls and pockets:

            try:
                result = engine.solve(
                    cue_ball=cue,
                    target_ball=balls[0],
                    pockets=pockets
                )

                if result:
                    overlay.set_data(result)

            except Exception as e:
                print("ENGINE ERROR:", e)

        # =========================
        # 🖥️ UPDATE QT UI
        # =========================
        app.processEvents()

        # small delay (stability)
        time.sleep(0.005)


if __name__ == "__main__":

    try:
        run()

    except Exception as e:
        print("FATAL ERROR:", e)
        input("Press Enter to exit...")
