from utils.util import Util
import numpy as np
import cv2
import pandas as pd
import os
import pickle
import cvzone

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV

class EmotionDetectorMachineLearning:
    def __init__(self):
        current_directory = Util.get_current_directory_of_file(__file__)
        self.train_dir = f"{current_directory}/emotion_data"
        self.emotion_feature_model_path = f"{current_directory}/trained_models/data_face_features_emotion.pickle"
        self.emotion_machine_learning_model_path = f"{current_directory}/trained_models/machinelearning_face_emotion.pkl"

        self.face_detector_model = None
        self.face_feature_model = None
        self.emotion_recognition_model = None

        self.emotion_hints = {
            'Happy': "Nice to see you happy!",
            'Sad': "Why sad? Be Happy",
            'Angry': "Don't be mad; be glad!",
            'Fear': "What's scaring you?",
            'Surprise': "You're full of surprises!",
            'Neutral': "You're keeping it cool today!",
            'None': "Emotion detection? I'm on vacation!"
        }
        self.drawing_rectange = False

    def enable_rectangle(self, flag: bool) -> None:
        self.drawing_rectange = flag

    def init_algorithm_models(self):
        current_directory = Util.get_current_directory_of_file(__file__)
        face_detection_model = f"{current_directory}/models/res10_300x300_ssd_iter_140000.caffemodel"
        face_detection_proto = f"{current_directory}/models/deploy.prototxt.txt"
        face_descriptor = f"{current_directory}/models/openface.nn4.small2.v1.t7"
        # load models using cv2 dnn
        self.face_detector_model = cv2.dnn.readNetFromCaffe(face_detection_proto,face_detection_model)
        self.face_feature_model = cv2.dnn.readNetFromTorch(face_descriptor)

    def init_machine_learning_model(self):
        self.emotion_recognition_model = pickle.load(open(self.emotion_machine_learning_model_path, mode='rb'))

    def extract_feature_model(self):
        data = dict(data=[],label=[])
        folders = os.listdir(self.train_dir)
        for folder in folders:
            filenames = os.listdir(f"{self.train_dir}/{folder}")
            for filename in filenames:
                try:
                    vector = self.helper(f"{self.train_dir}/{folder}/{filename}")
                    if vector is not None:
                        data['data'].append(vector)
                        data['label'].append(folder)
                        print('Feature Extracted Sucessfully')
                        
                except:
                    pass
        
        print(data.keys())
        print(pd.Series(data['label']).value_counts())
        model_path = self.emotion_feature_model_path
        pickle.dump(data,open(model_path, mode='wb'))

    def train_model(self):
        data = pickle.load(open(self.emotion_feature_model_path, mode='rb'))
        X = np.array(data['data']) # indendepent variable
        y = np.array(data['label']) # dependent variable
        X = X.reshape(-1,128)
        x_train,x_test,y_train,y_test = train_test_split(X,y,train_size=0.8,random_state=0)

        # Logistic Regression
        model_logistic = LogisticRegression()
        model_logistic.fit(x_train,y_train) # training logistic regression

        self.get_report(model_logistic,x_train,y_train,x_test,y_test)

        # Vector Machines
        model_svc = SVC(probability=True)
        model_svc.fit(x_train,y_train)

        self.get_report(model_svc,x_train,y_train,x_test,y_test)

        # Random Forest
        model_rf = RandomForestClassifier(n_estimators=10,)
        model_rf.fit(x_train,y_train)

        self.get_report(model_rf,x_train,y_train,x_test,y_test)

        model_voting = VotingClassifier(estimators=[
            ('logistic',LogisticRegression()),
            ('svm',SVC(probability=True)),
            ('rf',RandomForestClassifier())
        ], voting='soft',weights=[2,3,1])

        model_voting.fit(x_train,y_train)

        self.get_report(model_voting,x_train,y_train,x_test,y_test)

        model_grid = GridSearchCV(
            model_voting,
            param_grid={
                'svm__C':[3,5,7,10],
                'svm__gamma':[0.1,0.3,0.5],
                'rf__n_estimators':[5,10,20],
                'rf__max_depth':[3,5,7],
                'voting':['soft','hard']
            },
            scoring='accuracy',cv=3,n_jobs=1,verbose=2
        )

        model_grid.fit(x_train,y_train)

        model_best_estimator = model_grid.best_estimator_
        print(model_grid.best_score_)

        current_directory = Util.get_current_directory_of_file(__file__)
        pickle.dump(model_best_estimator,open(self.emotion_machine_learning_model_path, mode='wb'))

    def get_report(self, model, x_train,y_train,x_test,y_test):
        y_pred_train = model.predict(x_train)
        y_pred_test = model.predict(x_test)

        # accuracy score
        acc_train = accuracy_score(y_train,y_pred_train)
        acc_test = accuracy_score(y_test,y_pred_test)

        # f1 score
        f1_score_train = f1_score(y_train,y_pred_train,average='macro')
        f1_score_test = f1_score(y_test,y_pred_test,average='macro')


        print('Accuracy Train = %0.2f'%acc_train)
        print('Accuracy Test = %0.2f'%acc_test)
        print('F1 Score Train = %0.2f'%f1_score_train)
        print('F1 Score Test = %0.2f'%f1_score_test)

    def helper(self, image_path):
        img = cv2.imread(image_path)
        # step-1: face detection
        image = img.copy()
        h,w = image.shape[:2]
        img_blob = cv2.dnn.blobFromImage(image,1,(300,300),(104,177,123),swapRB=False,crop=False)
        # set the input
        self.face_detector_model.setInput(img_blob)
        detections = self.face_detector_model.forward()

        if len(detections) > 0:
            # consider the face with max confidence score
            i = np.argmax(detections[0,0,:,2])
            confidence = detections[0,0,i,2]
            if confidence > 0.5:
                box = detections[0,0,i,3:7]*np.array([w,h,w,h])
                (startx,starty,endx,endy) = box.astype('int')
                # step-2: Feature Extraction
                roi = image[starty:endy,startx:endx].copy()
                # get the face descriptors
                faceblob = cv2.dnn.blobFromImage(roi,1/255,(96,96),(0,0,0),swapRB=True,crop=True)
                self.face_feature_model.setInput(faceblob)
                vectors = self.face_feature_model.forward()
                return vectors

        return None


    def predict_emotions(self, image):
        h,w = image.shape[:2]
        # face detection
        img_blob = cv2.dnn.blobFromImage(image,1,(300,300),(104,177,123),swapRB=False,crop=False)
        self.face_detector_model.setInput(img_blob)
        detections = self.face_detector_model.forward()
        
        result = []
        if len(detections) > 0:
            for i , confidence in enumerate(detections[0,0,:,2]):
                if confidence > 0.5:
                    box = detections[0,0,i,3:7]*np.array([w,h,w,h])
                    startx,starty,endx,endy = box.astype(int)
                    rectangle_box = (startx, starty, endx, endy)
                 
                    # feature extraction
                    face_roi = image[starty:endy, startx:endx]
                    face_blob = cv2.dnn.blobFromImage(face_roi, 1/255,(96,96), (0,0,0), swapRB=True, crop=True)
                    self.face_feature_model.setInput(face_blob)
                    vectors = self.face_feature_model.forward()

                    emotion_name = self.emotion_recognition_model.predict(vectors)[0]
                    # print(f"names: {self.emotion_recognition_model.predict(vectors)}")
                    emotion_score = self.emotion_recognition_model.predict_proba(vectors).max()
                    # print(f"scores: {self.emotion_recognition_model.predict_proba(vectors)}")

                    result.append({
                        'box': rectangle_box,
                        'emotion_name': emotion_name,
                        'emotion_score': emotion_score
                    })

                    self.draw_emotion_rectangle(image, rectangle_box, emotion_name, emotion_score)
         
        return result

    def draw_emotion_rectangle(self, image, box, emotion_name, emotion_score) -> None:
        startx, starty, endx, endy = box
        x = startx
        y = starty
        w = endx - startx
        h = endy - starty
        if self.drawing_rectange:
            cvzone.cornerRect(image, (x,y, w, h))

        emotion_name = emotion_name.capitalize()
        # emotion_hint = f"{emotion_name}: {round(emotion_score, 2)}"
        emotion_hint = self.emotion_hints[emotion_name]
        cvzone.putTextRect(
            image,
            emotion_hint,
            (x + 2, y + h + 25),
            scale=1,
            thickness=1,
            colorT=(255, 255, 255),
            colorR=(255, 0, 255),
        )
           

# emotion_detector = EmotionDetectorMachineLearning()
# emotion_detector.init_algorithm_models()
# emotion_detector.init_machine_learning_model()
# # emotion_detector.extract_feature_model()
# # emotion_detector.train_model()

# video_capture = cv2.VideoCapture(0)

# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         break
    
#     flip_frame = cv2.flip(frame, 1)
#     results = emotion_detector.predict_emotions(flip_frame)

#     cv2.imshow('detection', flip_frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# video_capture.release()
# cv2.destroyAllWindows()