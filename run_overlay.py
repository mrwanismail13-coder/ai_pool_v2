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

    # =========================
    # 🎥 CAMERA INIT (SAFE MODE)
    # =========================
    try:
        camera = dxcam.create(output_idx=0, output_color="BGR")
    except Exception as e:
        print("DXCAM INIT ERROR:", e)
        return

    camera.start(target_fps=30)  # 🔥 تقليل الضغط (مهم جداً للاستقرار)

    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()

    last_frame_time = time.time()

    # =========================
    # 🔄 MAIN LOOP
    # =========================
    while True:

        frame = camera.get_latest_frame()

        # =========================
        # 🧪 TEST 1: FRAME CHECK
        # =========================
        if frame is None:
            print("FRAME: None ❌")
            app.processEvents()
            time.sleep(0.01)
            continue
        else:
            # print فقط كل ثانية (علشان ما نغرقش الكونسول)
            if time.time() - last_frame_time > 1:
                print("FRAME OK:", frame.shape)
                last_frame_time = time.time()

        # =========================
        # 🧠 YOLO DETECTION
        # =========================
        try:
            detections = detector.detect(frame)
        except Exception as e:
            print("DETECT ERROR:", e)
            detections = []

        # =========================
        # 🎯 BALL MANAGER
        # =========================
        manager.update(detections)

        cue = manager.get_cue_ball()
        balls = manager.get_object_balls()
        pockets = manager.get_pockets()

        # =========================
        # 🧪 DEBUG PRINT
        # =========================
        # print("cue:", cue, "balls:", len(balls), "pockets:", len(pockets))

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
        # 🖥️ UI UPDATE
        # =========================
        app.processEvents()
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        run()

    except Exception as e:
        print("FATAL ERROR:", e)
        input("Press Enter to exit...")
