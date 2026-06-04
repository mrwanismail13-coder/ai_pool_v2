import sys
import time
import dxcam

from PyQt6.QtWidgets import QApplication

from core.detector import BallDetector
from core.ball_manager import BallManager
from core.aim_engine import AimEngine
from overlay.overlay_window import OverlayWindow


# =========================
# 🔧 DEBUG TOGGLE
# =========================
DEBUG_DETECTIONS = True   # ← خليه True للتست

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
    # CAMERA INIT (SAFE)
    # =========================
    try:
        camera = dxcam.create(output_idx=0, output_color="BGR")
        camera.start(target_fps=30)
    except Exception as e:
        print("❌ DXCAM ERROR:", e)
        return

    # =========================
    # CORE SYSTEMS
    # =========================
    detector = BallDetector()
    manager = BallManager()
    engine = AimEngine()

    frame_counter = 0
    last_time = time.time()

    # =========================
    # MAIN LOOP
    # =========================
    while True:

        frame = camera.get_latest_frame()

        if frame is None:
            app.processEvents()
            time.sleep(0.01)
            continue

        # =========================
        # FPS DEBUG
        # =========================
        frame_counter += 1
        if time.time() - last_time >= 1:
            print(f"FPS: {frame_counter} | FRAME: {frame.shape}")
            frame_counter = 0
            last_time = time.time()

        # =========================
        # YOLO DETECTION
        # =========================
        try:
            detections = detector.detect(frame)
        except Exception as e:
            print("❌ DETECT ERROR:", e)
            detections = []

        # =========================
        # 🔥 TEST MODE PRINT
        # =========================
        if DEBUG_DETECTIONS:
            print("DETECTIONS COUNT:", len(detections))
            for d in detections[:3]:   # نعرض أول 3 فقط
                print(" ->", d)

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

            try:
                result = engine.solve(
                    cue_ball=cue,
                    target_ball=balls[0],
                    pockets=pockets,
                    table_bounds=(0, 0, frame.shape[1], frame.shape[0])
                )

                if result:
                    overlay.set_data(result)

            except Exception as e:
                print("❌ ENGINE ERROR:", e)

        # =========================
        # QT UPDATE
        # =========================
        app.processEvents()
        time.sleep(0.01)


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":

    try:
        run()

    except Exception as e:
        print("FATAL ERROR:", e)
        input("Press Enter to exit...")
