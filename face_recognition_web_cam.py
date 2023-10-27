import face_recognition
import cv2
import numpy as np
from recognition_knn import RecognitionKNN

class FaceRecognitionWebCam:
    def __init__(self) -> None:
        self.device_index = 0
        self.video_capture = cv2.VideoCapture(self.device_index)

    def run(self):
        process_this_frame = True
        predict_result = [] # name and location (name, ())
        while True:
            ret, frame = self.video_capture.read()

            if process_this_frame:
                predict_result = self._predict_by_KNN(frame)

            process_this_frame = not process_this_frame

            self._draw_face_rectangle(frame=frame, predict_result=predict_result)
            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop(self):
        pass

    def _predict_by_KNN(self, frame):
         # Resize frame of video to 1/4 size for faster face recognition processing
        
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
    
    def _draw_face_rectangle(self, frame, predict_result) -> None:
        for name, (top, right, bottom, left) in predict_result:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)