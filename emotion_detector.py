from fer import FER
import cv2


class EmotionDetector:
    def __init__(self) -> None:
        self.detetor = FER(mtcnn='mtcnn')
    
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
                emotion_name = f"{name.capitalize()}: {score}"

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, emotion_name, (left + 6, bottom + 26), font, 1.0, (0, 255, 0), 1)
                index += 1
    
