from recognition_knn import RecognitionKNN
from face_recognition_web_cam import FaceRecognitionWebCam
from logger import Logger
import sys
import signal
from functools import partial
import time
from datetime import datetime

def crtl_c_handler(web_cam, signal, frame):
    Logger.debug("Ctrl+C was pressed. Going to exit the face recognition program")
    web_cam.stop()
    time.sleep(1)
    Logger.debug("Handle Ctrl+C successed.")
    sys.exit(0)


if __name__ == "__main__":
    # RecognitionKNN().train_model(n_neighbors=2)

    webcam = FaceRecognitionWebCam()
    signal.signal(signal.SIGINT, partial(crtl_c_handler, webcam))
    try:
        webcam.run()
    except Exception as ex:
        Logger.error(f"Face recognition program has a unpected exception. error: {str(ex)}")

