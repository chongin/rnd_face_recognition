from PySide6.QtWidgets import QCheckBox

class ActionCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        mini_height = 60
        font_size = 12
        font_color = "#FFFFFF"

        self.setMinimumHeight(mini_height)
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
        self.setStyleSheet(f"QCheckBox {{ color: {font_color}; }}")
