
from web_cam import WebCam
from logger import Logger
import sys
import signal
from functools import partial
import time
import traceback
from datetime import datetime
from ultralytics import  YOLO
import  cv2



def crtl_c_handler(web_cam, signal, frame):
    Logger.debug("Ctrl+C was pressed. Going to exit the face recognition program")
    web_cam.stop()
    time.sleep(1)
    Logger.debug("Handle Ctrl+C successed.")
    sys.exit(0)


if __name__ == "__main__":
    # model = YOLO('yolo_weights/yolov8l.pt')
    # results = model("./models/Chong In Ng/selfie.jpg", show=True)
    # cv2.waitKey(0)
    # RecognitionKNN().train_model(n_neighbors=2)

    webcam = WebCam()
    signal.signal(signal.SIGINT, partial(crtl_c_handler, webcam))
    try:
        webcam.run()
    except Exception as ex:
        Logger.error(f"Face recognition program has a unpected exception. error: {str(ex)}")
        traceback.print_exc()

