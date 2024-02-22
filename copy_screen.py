import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QGuiApplication, QColor, QPen
from PyQt5.QtCore import Qt, QPoint


class ScreenshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the desired window size here (replace with your preferred values)
        self.setGeometry(0, 0, 1920, 1080)  # Example: Width=600, Height=400

        self.setWindowTitle("Выберите область для скриншота")

        self.begin = QPoint()
        self.end = QPoint()

        self.label = QLabel(self)
        self.pixmap = QPixmap("screenshot.png")
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignTop)
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseMoveEvent = self.mouseMoveEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        painter.drawRect(self.begin.x(), self.begin.y(),
                        self.end.x() - self.begin.x(), self.end.y() - self.begin.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end = event.pos()
            self.take_screenshot()
            self.close()

    def take_screenshot(self):
        rect = self.label.geometry()

        # Calculate coordinates as before
        x1 = min(self.begin.x(), self.end.x()) - rect.x()
        y1 = min(self.begin.y(), self.end.y()) - rect.y()
        x2 = max(self.begin.x(), self.end.x()) - rect.x()
        y2 = max(self.begin.y(), self.end.y()) - rect.y()

        # Capture screenshot using QApplication
        screenshot = QApplication.primaryScreen().grabWindow(
            QApplication.desktop().winId(), x1, y1, x2 - x1, y2 - y1
        )

        # Set the screenshot image to the clipboard
        QGuiApplication.clipboard().setPixmap(screenshot)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.show()
    sys.exit(app.exec_())
