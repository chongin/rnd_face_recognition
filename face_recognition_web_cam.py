import face_recognition
import cv2
import numpy as np
from recognition_knn import RecognitionKNN
from emotion_detector import EmotionDetector
from logger import Logger


class FaceRecognitionWebCam:
    def __init__(self) -> None:
        self.device_index = 0
        self.video_capture = cv2.VideoCapture(self.device_index)
        self.emotion_detector = EmotionDetector()
        self.running = True

    def run(self):
        process_this_frame = True
        predict_result = []  # name and location (name, ())
        predict_emotions = []
        while self.running:
            ret, frame = self.video_capture.read()

            if process_this_frame:
                predict_result = self._predict_by_KNN(frame)
                predict_emotions = self.emotion_detector.detect_emotions(frame)
                Logger.debug(f"Predict emotinos: {predict_emotions}")
                Logger.debug(f"Prefict faces, {predict_result}")

            process_this_frame = not process_this_frame

            self._draw_face_rectangle(frame, predict_result)
            self.draw_emotion_rectangle(frame, predict_result, predict_emotions)
            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                Logger.info("Click q to quit")
                break
        
        self.video_capture.release()
        cv2.destoryAllWindows()
        Logger.debug("Exited face recognition program.")

    def stop(self):
        self.running = False
        Logger.debug("Set running to False.")
  
# [('Chong In Ng', (76, 225, 166, 135))]
    def _predict_by_KNN(self, frame):
        predict_result = []
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        if len(face_encodings) > 0:
            predict_result = RecognitionKNN().predict_by_encodings(
                face_encodings,
                face_locations,
                distance_threshold=0.6,
                n_neighbors=1
            )
      
        return predict_result
    
# [('Chong In Ng', (76, 225, 166, 135))]
    def _draw_face_rectangle(self, frame, predict_result) -> None:
        for name, (top, right, bottom, left) in predict_result:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, top - 35), (right, top), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)

# [{'box': [547, 103, 304, 370], 'emotions': {'angry': 0.22, 'disgust': 0.0, 'fear': 0.44, 'happy': 0.0, 'sad': 0.14, 'surprise': 0.0, 'neutral': 0.18}}]
    def draw_emotion_rectangle(self, frame, predict_result, predict_emotions) -> None:
        index = 0
        for name, (top, right, bottom, left) in predict_result:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            emotion_name = 'None'
            if len(predict_emotions) <= index:
                emotion_name = 'None'
            else:
                emotion_data = predict_emotions[index]['emotions']
                name, score = list(emotion_data.items())[0]
                emotion_name = f"{name.capitalize()}: {score}"
            
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, emotion_name, (left + 6, bottom + 26), font, 1.0, (0, 255, 0), 1)
            index += 1
