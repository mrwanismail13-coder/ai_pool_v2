import sys
import time
from overlay.overlay_window import OverlayWindow

from PyQt6.QtWidgets import QApplication


def run_overlay():

    app = QApplication(sys.argv)
    window = OverlayWindow()

    # =========================
    # FAKE TEST DATA (هنا هنربط AI بعدين)
    # =========================
    while True:

        lines = [
            (300, 400, 900, 200),  # cue → ghost
            (900, 200, 1100, 100)  # ghost → pocket
        ]

        points = [
            (300, 400),
            (900, 200),
            (1100, 100)
        ]

        window.set_data(lines, points)

        app.processEvents()
        time.sleep(0.016)


if __name__ == "__main__":
    run_overlay()
