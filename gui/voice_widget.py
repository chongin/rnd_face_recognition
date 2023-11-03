from PySide6.QtWidgets import *
from PySide6.QtCore import *

import sys
import os
import threading


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../voice')))
from voice_detector import VoiceDetector


class VoiceThread(QThread):
    text_updated_signal = Signal(str)

    def init(self):
        self.voice_detector = VoiceDetector()
        self.voice_detector.set_callback(self.handle_text)

    def run(self):
        self.thread_active = True
        while self.thread_active:
            self.voice_detector._run_in_event_loop()

        print("33333333333333333")
       # self.voice_detector.stop()
        print("444444444444")

    def stop(self):
        self.voice_detector.stop()
        print("5555555555555")
        self.thread_active = False
        self.quit()

    def handle_text(self, text: str) -> None:
        self.text_updated_signal.emit("text")


class VoiceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.text_edit = QTextEdit()
        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(self.text_edit)
        self.setLayout(vlayout)

        self.speech_thread = VoiceThread()
        self.speech_thread.init()
        self.speech_thread.text_updated_signal.connect(self.update_text)
    
    def start(self):
        self.speech_thread.start()
        print("11111111111")

    def stop(self):
        self.speech_thread.stop()
        print("22222222222")

    def update_text(self, text):
        self.text_edit.append(text)