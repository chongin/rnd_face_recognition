import numpy as np
import cv2
import sklearn
import pickle

# face detection
face_detector_model = cv2.dnn.readNetFromCaffe('./models/deploy.prototxt.txt',
                                               './models/res10_300x300_ssd_iter_140000.caffemodel')
# feature extraction
face_feature_model = cv2.dnn.readNetFromTorch('./models/openface.nn4.small2.v1.t7')
# face recognition
face_recognition_model = pickle.load(open('./models/machinelearning_face_person_identity.pkl',
                                          mode='rb'))
# emotion recognition model
#emotion_recognition_model = pickle.load(open('./models/machinelearning_face_emotion.pkl',mode='rb'))



img = cv2.imread("./images/Cheick Maiga/rd.jpg")
img = cv2.imread("1200px-Sen._Barack_Obama_smiles.jpg")
image = img.copy()
h,w = img.shape[:2]
# face detection
img_blob = cv2.dnn.blobFromImage(img,1,(300,300),(104,177,123),swapRB=False,crop=False)
face_detector_model.setInput(img_blob)
detections = face_detector_model.forward()
#print(f"detections: {detections}")
if len(detections) > 0:
    for i , confidence in enumerate(detections[0,0,:,2]):
        if confidence > 0.99:
            box = detections[0,0,i,3:7]*np.array([w,h,w,h])
            startx,starty,endx,endy = box.astype(int)

            cv2.rectangle(image,(startx,starty),(endx,endy),(0,255,0))
            # feature extraction
            face_roi = img[starty:endy,startx:endx]
            face_blob = cv2.dnn.blobFromImage(face_roi,1/255,(96,96),(0,0,0),swapRB=True,crop=True)
            face_feature_model.setInput(face_blob)
            vectors = face_feature_model.forward()

            # predict with machine learning
            face_name = face_recognition_model.predict(vectors)[0]
            face_score = face_recognition_model.predict_proba(vectors).max()

            text_face = '{} : {:.0f} %'.format(face_name,100*face_score)
            cv2.putText(image,text_face,(startx,starty),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)

cv2.imshow('detection',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
