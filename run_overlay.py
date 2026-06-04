import sys
import time
from PyQt6.QtWidgets import QApplication
from overlay.overlay_window import OverlayWindow


def run():

    app = QApplication(sys.argv)
    window = OverlayWindow()

    print("🚀 OVERLAY STARTED")

    while True:

        # test lines (later AI engine)
        lines = [
            (200, 600, 900, 200),
            (900, 200, 1200, 100)
        ]

        window.set_data(lines=lines)

        app.processEvents()
        time.sleep(0.016)
