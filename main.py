from recognition_knn import RecognitionKNN
from face_recognition_web_cam import FaceRecognitionWebCam

if __name__ == "__main__":
    #RecognitionKNN().train_model(n_neighbors=2)
    FaceRecognitionWebCam().run()

    #res = RecognitionKNN().predict("./models/Chong In Ng/selfie.jpg")
    #print(f"rrrrr {res}")

