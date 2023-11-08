import sys
import os

from PySide6.QtWidgets import *
from PySide6.QtCore import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../voice')))
from voice_detector import VoiceDetector


class VoiceThread(QThread):
    text_updated_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.voice_detector = None

    def set_voice_detector(self, voice_detector):
        self.voice_detector = voice_detector
        self.voice_detector.set_callback(self.handle_text)

    def run(self):
        self.thread_active = True
        self.voice_detector.run_loop()

    def stop(self):
        self.voice_detector.stop()
        print("Stop voice thread success.")
        self.thread_active = False
        self.quit()

    def handle_text(self, text: str) -> None:
        self.text_updated_signal.emit(text)


class VoiceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.voice_detector = VoiceDetector()
        self.voice_thread = VoiceThread()
        self.voice_thread.set_voice_detector(self.voice_detector)
        self.voice_thread.text_updated_signal.connect(self.update_text)

        self.text_edit = QTextEdit()
        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(self.text_edit)
        self.setLayout(vlayout)

    def is_enable_voice_detection(self):
        return self.voice_detector.is_running()

    def start(self):
        self.voice_thread.start()
        print("Started voice thread")

    def stop(self):
        self.voice_thread.stop()
        print("Stoped voice thread")

    def update_text(self, text):
        self.text_edit.append(text)