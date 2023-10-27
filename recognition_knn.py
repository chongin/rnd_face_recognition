import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw, ImageFont
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder


class RecognitionKNN:
    def __init__(self) -> None:
        self.allowed_extenstions = {'png', 'jpg', 'jpeg'}
        self.train_dir = "./models"
        self.model_save_folder = './trained_models'
        self.model_name = 'trained_knn_model'
        self.knn_clf = None

    def train_model(self, n_neighbors=None, knn_algo='ball_tree'):
        encoding_dict = self._load_encodings()
        encodings = encoding_dict['encodings']
        names = encoding_dict['names']

        if n_neighbors is None:
            n_neighbors = int(round(math.sqrt(len(encodings))))
            print("Chose n_neighbors automatically:", n_neighbors)
                
        knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
        knn_clf.fit(encodings, names)

        self._save_model(knn_clf=knn_clf)
            
        return knn_clf

    def predict(self, img_path, distance_threshold=0.6):
        if not os.path.isfile(img_path) or os.path.splitext(img_path)[1][1:] not in self.allowed_extenstions:
            raise Exception("Invalid image path: {}".format(img_path))
        
        img = face_recognition.load_image_file(img_path)
        return self.predict_image(img, distance_threshold)
    
    def predict_image(self, img, distance_threshold=0.6):
        if self.knn_clf is None:
            self.knn_clf = self._load_model()

        face_locations = face_recognition.face_locations(img)
        if len(face_locations) == 0:
            raise Exception("Cannot find any face in this image.")
        
        face_encodings = face_recognition.face_encodings(img, face_locations)
        return self.predict_by_encodings(
            face_encodings, face_locations, 
            distance_threshold, n_neighbors=1
        )
    
    def predict_by_encodings(self, face_encodings, face_locations,
                             distance_threshold, n_neighbors):
        if self.knn_clf is None:
            self.knn_clf = self._load_model()

        print(f"gggggggg {face_encodings}")
        closest_distances = self.knn_clf.kneighbors(face_encodings, n_neighbors=n_neighbors)
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

            for img_path in image_files_in_folder(os.path.join(self.train_dir, class_dir)):
                image = face_recognition.load_image_file(img_path)
                face_bounding_boxes = face_recognition.face_locations(image)

                if len(face_bounding_boxes) != 1:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                        
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