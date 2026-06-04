import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QTimer


class OverlayWindow(QWidget):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW FLAGS (IMPORTANT FOR OVERLAY)
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

        # Full screen overlay
        self.showFullScreen()

        # =========================
        # DRAW DATA
        # =========================
        self.lines = []     # [(x1,y1,x2,y2)]
        self.points = []    # [(x,y)]

        # =========================
        # FPS TIMER
        # =========================
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    # =========================
    # UPDATE FROM ENGINE
    # =========================
    def set_data(self, lines=None, points=None):
        self.lines = lines or []
        self.points = points or []

    # =========================
    # DRAW LOOP
    # =========================
    def paintEvent(self, event):

        painter = QPainter(self)

        # =========================
        # AIM LINES (RED / YELLOW STYLE LIKE VIDEO)
        # =========================
        pen_line = QPen(Qt.GlobalColor.red, 3)
        painter.setPen(pen_line)

        for line in self.lines:
            x1, y1, x2, y2 = line
            painter.drawLine(x1, y1, x2, y2)

        # =========================
        # POINTS (WHITE / DEBUG NODES)
        # =========================
        pen_point = QPen(Qt.GlobalColor.yellow, 6)
        painter.setPen(pen_point)

        for x, y in self.points:
            painter.drawPoint(x, y)
