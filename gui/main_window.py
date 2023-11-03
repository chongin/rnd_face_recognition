import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from video_widget import VideoWidget
from action_checkbox import ActionCheckBox

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_menu()
        self.create_toolbar()

        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(5)

        self.video_widget = VideoWidget()
        self.video_widget.setStyleSheet("background-color: black;")
        vlayout.addWidget(self.video_widget, 1)
        control_widget = self.create_control_widget()
        control_widget.setStyleSheet("background-color: #2E2E2E;")
        vlayout.addWidget(control_widget, 0)

        central_widget = QWidget()
        central_widget.setLayout(vlayout)
        self.setCentralWidget(central_widget)

        self.dock_widget = QDockWidget("Snapshot View", self)
        dock_text_edit = QTextEdit()
        self.dock_widget.setWidget(dock_text_edit)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu("View")
        snapshot_action = QAction("Toggle Snapshot", self)
        snapshot_action.triggered.connect(self.toggle_snapshot_dock)
        view_menu.addAction(snapshot_action)

    def create_toolbar(self):
        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)

        start_action = QAction("Start", self)
        start_action.triggered.connect(self.start_clicked)
        toolbar.addAction(start_action)

        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.stop_clicked)
        toolbar.addAction(stop_action)

    def create_control_widget(self):
        self.face_cb = ActionCheckBox("Face Detection")
        self.emotion_cb = ActionCheckBox("Emotion Detection")
        self.object_cb = ActionCheckBox("Object Detection")
        self.voice_cb = ActionCheckBox("Voice Detection")
        self.all_cb = ActionCheckBox("All Detections")
        
        self.face_cb.toggled.connect(self.face_detection_toggle)
        self.emotion_cb.toggled.connect(self.emotion_detection_toggle)
        self.object_cb.toggled.connect(self.object_detection_toggle)
        self.voice_cb.toggled.connect(self.voice_detection_toggle)
        self.all_cb.toggled.connect(self.all_detection_toggle)

        hlayout = QHBoxLayout()

        hlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hlayout.addWidget(self.face_cb)
        hlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hlayout.addWidget(self.emotion_cb)
        hlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hlayout.addWidget(self.object_cb)
        hlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hlayout.addWidget(self.voice_cb)
        hlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hlayout.addWidget(self.all_cb)
        hlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        widget = QWidget()
        widget.setLayout(hlayout)
        return widget

    def toggle_snapshot_dock(self):
        self.dock_widget.setHidden(not self.dock_widget.isHidden())

    def start_clicked(self):
        self.video_widget.start()

    def stop_clicked(self):
        self.video_widget.stop()

    def face_detection_toggle(self):
        print("face_detection_toggle")
        self.video_widget.enable_face_dectection(self.face_cb.isChecked())
        self.update_all_checkbox_state()

    def emotion_detection_toggle(self):
        print("emotion_detection_toggle")
        self.video_widget.enable_emotion_dectection(self.emotion_cb.isChecked())
        self.update_all_checkbox_state()

    def object_detection_toggle(self):
        print("object_detection_toggle")
        self.video_widget.enable_object_dectection(self.object_cb.isChecked())
        self.update_all_checkbox_state()

    def voice_detection_toggle(self):
        print("voice_detection_toggle")
        self.update_all_checkbox_state()

    def all_detection_toggle(self):
        all_checked = self.all_cb.isChecked()
        self.face_cb.setChecked(all_checked)
        self.emotion_cb.setChecked(all_checked)
        self.object_cb.setChecked(all_checked)
        self.voice_cb.setChecked(all_checked)

    def update_all_checkbox_state(self):
        # Check the states of all other checkboxes
        face_checked = self.face_cb.isChecked()
        emotion_checked = self.emotion_cb.isChecked()
        object_checked = self.object_cb.isChecked()
        voice_checked = self.voice_cb.isChecked()

        self.all_cb.blockSignals(True)

        if face_checked and emotion_checked and object_checked and voice_checked:
            self.all_cb.setChecked(True)
        elif not face_checked and not emotion_checked and not object_checked and not voice_checked:
            self.all_cb.setChecked(False)
        else:
            self.all_cb.setCheckState(Qt.PartiallyChecked)

        self.all_cb.update()
        self.all_cb.blockSignals(False)


def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    width, height = app.primaryScreen().size().toTuple()
    window.resize(width, height)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
