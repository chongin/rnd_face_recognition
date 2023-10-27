from fer import FER
import cv2


class EmotionDetector:
    def __init__(self) -> None:
        self.detetor = FER(mtcnn='mtcnn')
    
    def detect_emotions(self, frame):
        flip_frame = cv2.flip(frame, 1)
        emotions = self.detetor.detect_emotions(flip_frame)
        highest_emotions = self._select_highest_emotion(emotions)
        return highest_emotions

# [{'box': [547, 103, 304, 370], 'emotions': {'angry': 0.22, 'disgust': 0.0, 'fear': 0.44, 'happy': 0.0, 'sad': 0.14, 'surprise': 0.0, 'neutral': 0.18}}]
    def _select_highest_emotion(self, detect_emotions):
        for item in detect_emotions:
            emotions = item['emotions']

            highest_emotion = max(emotions, key=emotions.get)
            item['emotions'] = {highest_emotion: emotions[highest_emotion]}
        return detect_emotions
    
