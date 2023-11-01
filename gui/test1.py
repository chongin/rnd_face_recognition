import sys
import cv2
from PySide6.QtCore import Qt, Signal, QThread, Slot
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QImage, QPixmap

class VideoThread(QThread):
    frame_updated = Signal(QImage)

    def run(self):
        self.video_capture = cv2.VideoCapture(0)
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
                self.frame_updated.emit(q_image)

class VideoWidget(QLabel):
    def __init__(self):
        super(VideoWidget, self).__init__()
        self.video_thread = VideoThread()
        self.video_thread.frame_updated.connect(self.update_frame)
        self.video_thread.start()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    @Slot(QImage)
    def update_frame(self, frame):
        scaled_frame = frame.scaled(self.size(), Qt.KeepAspectRatio)
        self.setPixmap(QPixmap.fromImage(scaled_frame))

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        print(f"Width: {width}, Height: {height}")
        super(VideoWidget, self).resizeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.video_widget = VideoWidget()
        layout.addWidget(self.video_widget)
        self.central_widget.setLayout(layout)
        self.setWindowTitle("OpenCV Video in PySide with QThread")
        self.setGeometry(100, 100, 640, 480)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
