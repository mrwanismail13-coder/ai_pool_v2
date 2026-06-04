from PyQt6 import QtWidgets, QtGui, QtCore
import sys


class OverlayWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Overlay")

        # =========================
        # WINDOW FLAGS (IMPORTANT)
        # =========================
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Full screen overlay
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.result = None
        self.pockets = []

        self.show()

    # =========================
    # UPDATE DATA
    # =========================
    def update_data(self, result, pockets):
        self.result = result
        self.pockets = pockets
        self.update()

    # =========================
    # DRAW EVENT
    # =========================
    def paintEvent(self, event):

        if self.result is None:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # =========================
        # COLORS
        # =========================
        cue_color = QtGui.QColor(255, 255, 255)
        target_color = QtGui.QColor(0, 255, 255)
        line_color = QtGui.QColor(255, 255, 0)
        pocket_color = QtGui.QColor(255, 0, 0)

        pen = QtGui.QPen()
        pen.setWidth(3)

        # =========================
        # DRAW POCKETS
        # =========================
        pen.setColor(pocket_color)
        painter.setPen(pen)

        for p in self.pockets:
            painter.drawEllipse(QtCore.QPoint(*map(int, p)), 10, 10)

        # =========================
        # DRAW BALLS
        # =========================
        cue = self.result.get("cue_ball")
        target = self.result.get("target_ball")
        ghost = self.result.get("ghost_ball")
        pocket = self.result.get("pocket")

        # cue -> ghost line
        if cue and ghost:
            pen.setColor(line_color)
            painter.setPen(pen)
            painter.drawLine(
                cue[0], cue[1],
                int(ghost[0]), int(ghost[1])
            )

        # ghost -> pocket line
        if ghost and pocket:
            painter.drawLine(
                int(ghost[0]), int(ghost[1]),
                int(pocket[0]), int(pocket[1])
            )

        # cue ball
        if cue:
            pen.setColor(cue_color)
            painter.setPen(pen)
            painter.drawEllipse(QtCore.QPoint(*cue), 8, 8)

        # target ball
        if target:
            pen.setColor(target_color)
            painter.setPen(pen)
            painter.drawEllipse(QtCore.QPoint(*target), 8, 8)
