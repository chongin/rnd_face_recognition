import sys
import cv2
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class VideoThread(QThread):
    frame_updated = Signal(QImage)

    def run(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, 1980)
        self.video_capture.set(4, 1024)
        while True:
            ret, frame = self.video_capture.read()
            if ret:
            #self.vision_manager.excute_frame(frame)
        
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #flippedImage = cv2.flip(image, 1)
                print(f"shape 1: {image.shape[1]},   shape 0: {image.shape[0]}")
                q_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)

                self.frame_updated.emit(q_image)

    def set_size(self, width, height):
        self.width = width
        self.height = height


class VideoWidget(QLabel):
    def __init__(self):
        super(VideoWidget, self).__init__()
        self.video_thread = VideoThread()
        self.video_thread.frame_updated.connect(self.update_frame)
        self.video_thread.set_size(1280, 720)
        self.video_thread.start()

        # Set size policy to make the widget expand and take available space
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    @Slot(QImage)
    def update_frame(self, frame):
        self.setPixmap(QPixmap.fromImage(frame))

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        print(f"Width: {width}, Height: {height}")
        super().resizeEvent(event)
        self.video_thread.set_size(width, height)
        self.update_frame(self.pixmap().toImage())

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a layout for the central widget and set its size policy
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.video_widget = VideoWidget()
        layout.addWidget(self.video_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    width,height = app.primaryScreen().size().toTuple()
    print(width, height)
    window.resize(width, height)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
