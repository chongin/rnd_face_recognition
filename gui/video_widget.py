from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import cv2

import sys
import os

# Add the parent directory (src) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../vision')))

from vision_manager import VisionManager

class VideoThread(QThread):
    image_updated_signal = Signal(QImage)


    def run(self):
        self.thread_active = True
        self.video_capture = cv2.VideoCapture(0)

        self.vision_manager = VisionManager()

        while self.thread_active:
            ret, frame = self.video_capture.read()
            self.vision_manager.excute_frame(frame)
            q_image = self.convert_cv_qt(frame)

            self.image_updated_signal.emit(q_image)

        self.video_capture.release()
    
    def convert_cv_qt(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    
    def stop(self):
        self.thread_active = False
        self.quit()


class VideoWidget(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.video_thread = VideoThread()
        self.video_thread.image_updated_signal.connect(self.update_image)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.max_scale_factor = 1.0
        # self.setAlignment(Qt.AlignCenter)
  

    def start(self):
        self.video_thread.start()

    def stop(self):
        self.video_thread.stop()

    @Slot(QImage)
    def update_image(self, image):
        scaled_image = image.scaled(self.size(), Qt.KeepAspectRatio)
        #scaled_image = self.scale_image(image, self.size(), self.max_scale_factor)
        self.setPixmap(QPixmap.fromImage(scaled_image))

    def scale_image(self, image, target_size, max_scale_factor):
        width_ratio = target_size.width() / image.width()
        height_ratio = target_size.height() / image.height()
        scale_factor = min(width_ratio, height_ratio, max_scale_factor)
        return image.scaled(image.width() * scale_factor, image.height() * scale_factor, Qt.KeepAspectRatio)