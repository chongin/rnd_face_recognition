from ultralytics import YOLO
import cv2
import cvzone
import math
from logger import  Logger
from utils.util import Util


class YoloDetector:
    def __init__(self):
        current_directory = Util.get_current_directory_of_file(__file__)
        self.model = YOLO(f"{current_directory}/yolo_weights/yolov8l.pt")
        self.class_names = self.model.names

    def detect_objects(self, frame):
        results = self.model(frame, stream=True)
        print(f"detect objects by Yolo: {results}")
        return results

    def draw_objects(self, frame, results):
        for r in results:
            self._handle_result(r, frame)

    def _handle_result(self, result, frame):
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w = x2 - x1
            h = y2 - y1
            cvzone.cornerRect(frame, (x1, y1, w, h))

            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            cvzone.putTextRect(frame, f'{self.class_names[cls]} {conf}', (max(0, x1), max(35, y1)),
                               scale=0.7, thickness=1, offset=3)
