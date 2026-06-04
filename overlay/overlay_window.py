import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QTimer


class OverlayWindow(QWidget):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW FLAGS (TOP OVERLAY)
        # =========================
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # =========================
        # TRANSPARENT BACKGROUND
        # =========================
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # full screen overlay
        self.showFullScreen()

        # =========================
        # DRAW DATA
        # =========================
        self.lines = []     # [(x1,y1,x2,y2,color)]
        self.points = []    # [(x,y,color)]

        # =========================
        # FPS TIMER
        # =========================
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    # =========================
    # UPDATE DATA FROM ENGINE
    # =========================
    def set_data(self, data=None, lines=None, points=None):

        self.data = data
        self.lines = lines or []
        self.points = points or []

    # =========================
    # DRAW LINE HELPER
    # =========================
    def draw_line(self, painter, x1, y1, x2, y2, color=Qt.GlobalColor.red, width=3):

        pen = QPen(color, width)
        painter.setPen(pen)
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    # =========================
    # PAINT EVENT (MAIN OVERLAY RENDER)
    # =========================
    def paintEvent(self, event):

        painter = QPainter(self)

        # =====================================
        # MODE 1: AIM ENGINE MODE (VIDEO STYLE)
        # =====================================
        if hasattr(self, "data") and self.data:

            cue = self.data.get("cue_ball")
            ghost = self.data.get("ghost_ball")
            pocket = self.data.get("pocket")

            # safety check
            if cue and ghost and pocket:

                # Cue → Ghost (GREEN line like video)
                self.draw_line(
                    painter,
                    cue[0], cue[1],
                    ghost[0], ghost[1],
                    Qt.GlobalColor.green,
                    3
                )

                # Ghost → Pocket (RED line like video)
                self.draw_line(
                    painter,
                    ghost[0], ghost[1],
                    pocket[0], pocket[1],
                    Qt.GlobalColor.red,
                    3
                )

                # Cue point
                painter.setPen(QPen(QColor(255, 255, 255), 6))
                painter.drawPoint(int(cue[0]), int(cue[1]))

                # Ghost point
                painter.setPen(QPen(QColor(0, 255, 255), 6))
                painter.drawPoint(int(ghost[0]), int(ghost[1]))

                # Pocket point
                painter.setPen(QPen(QColor(255, 0, 0), 8))
                painter.drawPoint(int(pocket[0]), int(pocket[1]))

        # =====================================
        # MODE 2: DEBUG LINES (optional fallback)
        # =====================================
        for line in self.lines:
            if len(line) == 4:
                self.draw_line(
                    painter,
                    line[0], line[1],
                    line[2], line[3],
                    Qt.GlobalColor.yellow,
                    2
                )

        # =====================================
        # MODE 3: DEBUG POINTS
        # =====================================
        for p in self.points:
            painter.setPen(QPen(Qt.GlobalColor.blue, 5))
            painter.drawPoint(int(p[0]), int(p[1]))
