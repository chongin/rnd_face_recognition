from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import cv2


class ImageData:
    def __init__(self, image, name) -> None:
        self.image = image
        self.name = name
        current_date_time = QDateTime.currentDateTime()
        self.timestamp = current_date_time.toString("yyyy-MM-dd HH:mm:ss")

class ImageListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.image_datas = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.image_datas)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DecorationRole:
            return self.image_datas[index.row()]

        return None

    def add_image_data(self, image_data):
        print(f"add image data: {image_data.name}")
        self.image_datas.append(image_data)
        self.dataChanged.emit(self.index(0), self.index(len(self.image_datas)))

    def exist_name(self, name):
        for _, image_data in enumerate(self.image_datas):
            if image_data.name == name:
                return True
        
        return False

class ImageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        image_data = index.model().data(index, Qt.DecorationRole)
        if image_data is not None:
            pixmap = QPixmap.fromImage(image_data.image)
            painter.drawPixmap(option.rect, pixmap)

            font = QFont()
            font.setPointSize(14)
            painter.setFont(font)
            text_color = Qt.green

            painter.setPen(QColor(text_color))
            painter.drawText(option.rect, Qt.AlignTop | Qt.AlignHCenter, image_data.name)
            painter.drawText(option.rect, Qt.AlignBottom | Qt.AlignRight, image_data.timestamp)

    def sizeHint(self, option, index):
        return QSize(200, 120)

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
        self.image_list_view.setMinimumWidth(210)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.image_list_view)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        self.setLayout(vlayout)

    @Slot(tuple)
    def add_face_image(self, tuple):
        frame = tuple[0]
        predict_faces = tuple[1]
        for name, (top, right, bottom, left) in predict_faces:
            if self.model.exist_name(name):
                # print(f"Already add: {name}, {(top, right, bottom, left)}")
                continue

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            width = right - left
            height = bottom - top
            cropped_face_image = frame[top:top+height, left:left+width]
            q_imag = self.convert_cv_qt(cropped_face_image)
            self.model.add_image_data(ImageData(q_imag, name))

    def convert_cv_qt(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        # print(f"h:{h}, w:{w}, ch:{ch}")
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)