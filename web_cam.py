import face_recognition
import cv2
import numpy as np
from face_recognition_knn import FaceRecognitionKNN
from emotion_detector import EmotionDetector
from yolo_detector import  YoloDetector
from logger import Logger


class WebCam:
    def __init__(self) -> None:
        self.device_index = 0
        self.video_capture = cv2.VideoCapture(self.device_index)
        self.video_capture.set(3 , 1280)
        self.video_capture.set(4, 720)
        self.running = True
        self.emotion_detector = EmotionDetector()
        self.yolo_detector = YoloDetector()
        self.face_detector = FaceRecognitionKNN()

    def run(self):
        while self.running:
            ret, frame = self.video_capture.read()
            detect_objects = self.yolo_detector.detect_objects(frame=frame)
            predict_result = self.face_detector.predict_faces(frame=frame)
            predict_emotions = self.emotion_detector.predict_emotions(frame=frame)

            self.yolo_detector.draw_objects(frame, detect_objects)
            self.face_detector.draw_face_rectangle(frame, predict_result)
            self.emotion_detector.draw_emotion_rectangle(frame, predict_result, predict_emotions)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                Logger.info("Click q to quit")
                break
        
        self.video_capture.release()
        cv2.destroyAllWindows()
        Logger.debug("Exited face recognition program.")

    def stop(self):
        self.running = False
        Logger.debug("Set running to False.")



