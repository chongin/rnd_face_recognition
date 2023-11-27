import sklearn
# import skimage
from face_recognition_knn import FaceRecognitionKNN
# from emotion_detector import EmotionDetector
from yolo_detector import  YoloDetector


class VisionManager:
    def __init__(self) -> None:
        # self.emotion_detector = EmotionDetector()
        self.yolo_detector = YoloDetector()
        self.face_detector = FaceRecognitionKNN()
        self.emotion_detection_flag = True
        self.face_detection_flag = True
        self.object_detection_flag = True

    # def enable_emotion_dectection(self, flag: bool) -> None:
    #     self.emotion_detection_flag = flag
    #     self.emotion_detector.enable_rectangle(not self.face_detection_flag)

    # def enable_face_dectection(self, flag: bool) -> None:
    #     self.face_detection_flag = flag
    #     self.emotion_detector.enable_rectangle(not self.face_detection_flag)

    def enable_object_dectection(self, flag: bool) -> None:
        self.object_detection_flag = flag

    def is_enable_emotion_detection(self) -> bool:
        return self.emotion_detection_flag
    
    def is_enable_face_dectection(self) -> bool:
        return self.face_detection_flag
    
    def is_enable_object_dectection(self) -> bool:
        return self.object_detection_flag
    
    # should return face predict result: like this [('Chong In Ng', (76, 225, 166, 135))]
    def excute_frame(self, frame) -> None:
        predict_faces = []
        if self.face_detection_flag:
            predict_faces = self.face_detector.predict_faces(frame=frame)
            self.face_detector.draw_face_rectangle(frame, predict_faces)

        # if self.emotion_detection_flag:
        #     predict_emotions = self.emotion_detector.predict_emotions(frame=frame)
        #     self.emotion_detector.draw_emotion_rectangle(frame, predict_emotions)

        # if self.object_detection_flag:
        #     detect_objects = self.yolo_detector.detect_objects(frame=frame)
        #     self.yolo_detector.draw_objects(frame, detect_objects)

        return predict_faces
         
            
            

            
            
            