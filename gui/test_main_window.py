import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from video_widget import VideoWidget
from action_checkbox import ActionCheckBox
# from voice_widget import VoiceWidget
from snapshot_widget import  SnapshotWidget


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("QtPySide 6 Example")
        self.setGeometry(100, 100, 600, 400)

        self.video_widget = VideoWidget()

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(self.video_widget)
        self.video_widget.start()
        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Add a label to the layout
        label = QLabel("Hello, QtPySide 6!", self)
        layout.addWidget(label)

        # Add a button to the layout
        button = QPushButton("Click me!", self)
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)

    def on_button_click(self):
        print("Button clicked!")

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    width, height = app.primaryScreen().size().toTuple()
    #window.resize(width, height)
    window.resize(1440, 900)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

