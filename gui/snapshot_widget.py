from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class ImageListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.images = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.images)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DecorationRole:
            return self.images[index.row()]

        return None

    def add_image(self, image):
        self.images.append(image)
        self.dataChanged.emit(self.index(0), self.index(len(self.images)))

class ImageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        image = index.model().data(index, Qt.DecorationRole)
        if image is not None:
            pixmap = QPixmap.fromImage(image)
            painter.drawPixmap(option.rect, pixmap)

class ImageListView(QListView):
    def __init__(self, model, delegate) -> None:
        super().__init__()
        self.setModel(model)
        self.setItemDelegate(delegate)
        self.setResizeMode(QListView.Adjust)

class SnapshotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.model = ImageListModel()
        self.delegate = ImageDelegate()
        self.image_list_view = ImageListView(self.model, self.delegate)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.image_list_view)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        self.setLayout(vlayout)

    @Slot(QImage)
    def add_image(self, image):
        desired_size = QSize(200, 120)
        scaled_image = image.scaled(desired_size, Qt.KeepAspectRatio)
        self.model.add_image(scaled_image)
