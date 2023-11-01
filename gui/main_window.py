import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from video_widget import VideoWidget

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a menu bar
        menubar = self.menuBar()
        
        # Create a File menu with an "Exit" action
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Create a View menu with a "Toggle Dock" action
        view_menu = menubar.addMenu("View")
        toggle_dock_action = QAction("Toggle Dock", self)
        toggle_dock_action.triggered.connect(self.toggle_dock)
        view_menu.addAction(toggle_dock_action)

        # Create a toolbar
        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)
        
        central_widget = QWidget()
        
        layout = QVBoxLayout()
        # Create a QTextEdit widget
        self.video_widget = VideoWidget()

        self.video_widget.start()
        layout.addWidget(self.video_widget)

        central_widget.setLayout(layout)

        layout.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        layout.setSpacing(0)  # spacing between widgets in the layout

        self.setCentralWidget(central_widget)

        self.dock_widget = QDockWidget("My Dock Widget", self)
        dock_text_edit = QTextEdit()
        self.dock_widget.setWidget(dock_text_edit)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

        # hsplitter = QSplitter(Qt.Horizontal)
        # hsplitter.addWidget(central_widget)
        # Create a dock widget
        # self.dock_widget1 = QDockWidget("My Dock Widget", self)
        # dock_text_edit = QTextEdit()
        # self.dock_widget1.setWidget(dock_text_edit)
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget1)  # 1 is for right dock area

        # self.bottom_dock_widget = QDockWidget("Bottom Dock Widget", self)
        # bottom_dock_text_edit = QTextEdit()
        # self.bottom_dock_widget.setWidget(bottom_dock_text_edit)
        # self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock_widget)

        # hsplitter.addWidget(self.bottom_dock_widget)
        # hsplitter.setSizes([1, 3])

        # layout.addWidget(self.bottom_dock_widget)

        # self.setCentralWidget(hsplitter)

    def toggle_dock(self):
        print("Enter the dock")
        self.dock_widget.setHidden(not self.dock_widget.isHidden())
        # self.dock_widget1.setHidden(not self.dock_widget1.isHidden())
        self.bottom_dock_widget.setHidden(not self.bottom_dock_widget.isHidden())

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    # desktop = QApplication.desktop()
    # screen_geometry = desktop.availableGeometry()
    # window.setGeometry(screen_geometry)
    width,height = app.primaryScreen().size().toTuple()
    print(width, height)
    window.resize(width, height)
    #window.setFixedSize(1280, 720)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()