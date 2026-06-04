import sys
import time
from PyQt6.QtWidgets import QApplication

from overlay.overlay_window import OverlayWindow


def run():

    app = QApplication(sys.argv)
    window = OverlayWindow()

    print("🚀 OVERLAY STARTED")

    while True:

        # 🔥 TEST LINE (زي الفيديو)
        lines = [
            (200, 600, 900, 200),  # cue → ghost
            (900, 200, 1200, 100)  # ghost → pocket
        ]

        window.set_data(lines=lines)

        app.processEvents()
        time.sleep(0.016)


if __name__ == "__main__":
    run()
