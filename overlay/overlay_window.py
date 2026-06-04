import sys
import cv2
import numpy as np

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QTimer


class OverlayWindow(QWidget):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW SETTINGS (TRANSPARENT OVERLAY)
        # =========================
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.showFullScreen()

        # =========================
        # DATA
        # =========================
        self.lines = []
        self.points = []

        # =========================
        # FPS TIMER
        # =========================
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    # =========================
    # UPDATE DATA FROM AI
    # =========================
    def set_data(self, lines=None, points=None):

        self.lines = lines or []
        self.points = points or []

    # =========================
    # DRAW
    # =========================
    def paintEvent(self, event):

        painter = QPainter(self)

        # 🔴 AIM LINES
        pen = QPen(Qt.GlobalColor.red, 2)
        painter.setPen(pen)

        for line in self.lines:
            x1, y1, x2, y2 = line
            painter.drawLine(x1, y1, x2, y2)

        # 🟡 POINTS
        pen = QPen(Qt.GlobalColor.yellow, 6)
        painter.setPen(pen)

        for p in self.points:
            x, y = p
            painter.drawPoint(x, y)
