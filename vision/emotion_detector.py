from fer import FER
from fer.utils import draw_annotations
import cv2
import cvzone


class EmotionSmoothing:
    def __init__(self, buffer_size=3) -> None:
        self.buffer_size = buffer_size
        self.emotion_buffer = []
    
    def add_emotion(self, emotion):
        self.emotion_buffer.append(emotion)
        if len(self.emotion_buffer) > self.buffer_size:
            self.emotion_buffer.pop(0)
    
    def get_smoothed_emotion(self):
        emotion_counts = {}
        for emotion in self.emotion_buffer:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        max_counts_emotion = max(emotion_counts, key=emotion_counts.get)
        return max_counts_emotion


class EmotionDetector:
    def __init__(self) -> None:
        self.detetor = FER(mtcnn='mtcnn')
        self.emotion_smoothing = EmotionSmoothing()
        self.enable_smoothing = False
        self.emotion_hints = {
            'Happy': "Nice to see you happy!",
            'Sad': "Why sad? Be Happy",
            'Angry': "Don't be mad; be glad!",
            'Fear': "What's scaring you?",
            'Surprise': "You're full of surprises!",
            'Neutral': "You're keeping it cool today!",
            'None': "Emotion detection? I'm on vacation!"
        }

    
    def predict_emotions(self, frame):
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
                emotion_name = f"{name.capitalize()}"

            if self.enable_smoothing:
                self.emotion_smoothing.add_emotion(emotion_name)
                emotion_name = self.emotion_smoothing.get_smoothed_emotion()

            emotion_hint = self.emotion_hints[emotion_name]
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(frame, emotion_hint, (left + 6, bottom + 26), font, 1.0, (0, 255, 0), 1)
            cvzone.putTextRect(frame, emotion_hint, (left + 6, bottom + 26), scale=1, thickness=1, colorR=(255, 0, 255),)
            index += 1
    
