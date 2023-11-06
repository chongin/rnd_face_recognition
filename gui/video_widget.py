from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import cv2

import sys
import os
import  time
import  datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../vision')))
from vision_manager import VisionManager

class VideoThread(QThread):
    image_updated_signal = Signal(QImage)

    def set_vision_manager(self, vision_manger):
        self.vision_manager = vision_manger

    def run(self):
        self.thread_active = True
        self.video_capture = cv2.VideoCapture(0)
        while self.thread_active:
            ret, frame = self.video_capture.read()
            flip_frame = cv2.flip(frame, 1)
            if self.vision_manager:
                self.vision_manager.excute_frame(flip_frame)

            q_image = self.convert_cv_qt(flip_frame)
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
    image_updated_signal = Signal(QImage)
    def __init__(self) -> None:
        super().__init__()
        self.vision_manager = VisionManager()
        self.video_thread = VideoThread()
        self.video_thread.set_vision_manager(self.vision_manager)

        self.video_thread.image_updated_signal.connect(self.update_image)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.last_time = datetime.datetime.now()
    def start(self):
        self.video_thread.start()

    def stop(self):
        self.video_thread.stop()

    def enable_emotion_dectection(self, flag: bool) -> None:
        self.vision_manager.enable_emotion_dectection(flag)

    def enable_face_dectection(self, flag: bool) -> None:
        self.vision_manager.enable_face_dectection(flag)

    def enable_object_dectection(self, flag: bool) -> None:
        self.vision_manager.enable_object_dectection(flag)

    @Slot(QImage)
    def update_image(self, image):
        scaled_image = image.scaled(self.size(), Qt.KeepAspectRatio)
        #scaled_image = self.scale_image(image, self.size(), self.max_scale_factor)
        self.setPixmap(QPixmap.fromImage(image))

        current_time = datetime.datetime.now()
        if (current_time - self.last_time).total_seconds() >= 5:
        #if self.last_time:
            self.image_updated_signal.emit(image)
            self.last_time = current_time

    def scale_image(self, image, target_size, max_scale_factor):
        width_ratio = target_size.width() / image.width()
        height_ratio = target_size.height() / image.height()
        scale_factor = min(width_ratio, height_ratio, max_scale_factor)
        return image.scaled(image.width() * scale_factor, image.height() * scale_factor, Qt.KeepAspectRatio)