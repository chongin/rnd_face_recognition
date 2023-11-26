import math
#from sklearn import neighbors
import os
import os.path
import pickle
import re
import face_recognition
from logger import Logger
import cv2
import numpy as np
import cvzone
from utils.util import Util

class FaceRecognitionKNN:
    def __init__(self) -> None:
        self.allowed_extenstions = {'png', 'jpg', 'jpeg'}
        current_directory = Util.get_current_directory_of_file(__file__)
        self.train_dir = f"{current_directory}/models"
        self.model_save_folder = f"{current_directory}/trained_models"
        self.model_name = 'trained_knn_model'
        self.knn_clf = None
    
    def train_model(self, n_neighbors=None, knn_algo='ball_tree'):
        Logger.info(f"Start to train model: n_neighbors: {n_neighbors}, knn_algo: {knn_algo}")
        encoding_dict = self._load_encodings()
        encodings = encoding_dict['encodings']
        names = encoding_dict['names']

        if n_neighbors is None:
            n_neighbors = int(round(math.sqrt(len(encodings))))
            Logger.info("Chose n_neighbors automatically:", n_neighbors)
                
        knn_clf = neighbors.KNeighborsClassifier(
            n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance'
        )
        knn_clf.fit(encodings, names)

        self._save_model(knn_clf=knn_clf)
        Logger.info("Finish trained model.") 
        return knn_clf

    # predict_result: [('Chong In Ng', (76, 225, 166, 135))]
    def predict_faces(self, frame):
        predict_result = []
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        if len(face_encodings) > 0:
            predict_result = self.predict_by_encodings(
                face_encodings,
                face_locations,
                distance_threshold=0.6,
                n_neighbors=1
            )
        Logger.debug(f"Predict faces, {predict_result}")
        return predict_result

    def draw_face_rectangle(self, frame, predict_result) -> None:
        for name, (top, right, bottom, left) in predict_result:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            width = right - left
            height = bottom - top
            cvzone.cornerRect(frame, (left, top, width, height))
            cvzone.putTextRect(
                frame,
                name,
                (left + 6, top - 12),
                scale=1,
                thickness=1,
                colorT=(255, 255, 255),
                colorR=(255, 0, 255),
            )
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # # cv2.rectangle(frame, (left, top - 35), (right, top), (0, 0, 255), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_PLAIN
            # cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 2)

    def predict(self, img_path, distance_threshold=0.6):
        if not os.path.isfile(img_path) or os.path.splitext(img_path)[1][1:] not in self.allowed_extenstions:
            error_message = "Invalid image path: {}".format(img_path)
            Logger.error(error_message)
            raise Exception(error_message)
        
        img = face_recognition.load_image_file(img_path)
        return self.predict_image(img, distance_threshold)
    
    def predict_image(self, img, distance_threshold=0.6):
        if self.knn_clf is None:
            self.knn_clf = self._load_model()

        face_locations = face_recognition.face_locations(img)
        if len(face_locations) == 0:
            error_message = "Cannot find any face in this image."
            Logger.error(error_message)
            raise Exception(error_message)
        
        face_encodings = face_recognition.face_encodings(img, face_locations)
        return self.predict_by_encodings(
            face_encodings, face_locations, 
            distance_threshold, n_neighbors=1
        )

    def predict_by_encodings(self, face_encodings, face_locations,
                             distance_threshold, n_neighbors):
        if self.knn_clf is None:
            self.knn_clf = self._load_model()

        closest_distances = self.knn_clf.kneighbors(
            face_encodings, n_neighbors=n_neighbors
        )
        are_matches = []
        for i in range(len(face_locations)):
            closest_distance = closest_distances[0][i][0]
            is_match = closest_distance <= distance_threshold
            are_matches.append(is_match)

        predictions = self.knn_clf.predict(face_encodings)
        
        result = []

        for pred_name, loc, rec in zip(predictions, face_locations, are_matches):
            if rec:
                result.append((pred_name, loc))
            else:
                result.append(("unknown", loc))

        return result

    def _load_encodings(self):
        encodings = []
        names = []
        for class_dir in os.listdir(self.train_dir):
            if not os.path.isdir(os.path.join(self.train_dir, class_dir)):
                continue
            
            image_folder = os.path.join(self.train_dir, class_dir)
            for img_path in self.get_image_files(image_folder):
                image = face_recognition.load_image_file(img_path)
                face_bounding_boxes = face_recognition.face_locations(image)

                if len(face_bounding_boxes) != 1:
                    Logger.warning("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                        
                else:
                    encodings.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                    names.append(class_dir)
        
        return {'encodings': encodings, 'names': names}

    def _save_model(self, knn_clf):
        model_path = self.model_save_folder + f"/{self.model_name}.clf"
        with open(model_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    def _load_model(self):
        model_path = self.model_save_folder + f"/{self.model_name}.clf"
        knn_clf = None
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
        return knn_clf
    
    def get_image_files(self, images_folder):
        image_file_paths = []
        files_in_folder = os.listdir(images_folder)
        for file_name in files_in_folder:
            if re.match(r'.*\.(jpg|jpeg|png)', file_name, flags=re.I):
                full_path = os.path.join(images_folder, file_name)
                image_file_paths.append(full_path)

        return image_file_paths