import sys
import pytesseract
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QToolTip
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QPoint
import pyperclip
import keyboard



class ScreenshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if sys.platform == "win32":
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.setGeometry(0, 0, 1920, 1080)  
        

        self.begin = QPoint()
        self.end = QPoint()

        self.label = QLabel(self)
        self.pixmap = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
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

        x1 = min(self.begin.x(), self.end.x()) - rect.x()
        y1 = min(self.begin.y(), self.end.y()) - rect.y()
        x2 = max(self.begin.x(), self.end.x()) - rect.x()
        y2 = max(self.begin.y(), self.end.y()) - rect.y()

        screenshot = self.pixmap.copy(x1, y1, x2 - x1, y2 - y1)
        screenshot.save("selected_area_screenshot.png", "png")

        image = Image.open("selected_area_screenshot.png")
        text = pytesseract.image_to_string(image, lang='eng+rus')

        pyperclip.copy(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.show()
    keyboard.add_hotkey('print screen', lambda: window.take_screenshot())
    sys.exit(app.exec_())
