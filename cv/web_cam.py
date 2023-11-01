import sys
import os
import time
# Add the parent directory (src) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../vision')))

import signal
from functools import partial
import traceback

import cv2
from vision_manager import VisionManager
from logger import Logger


class WebCam:
    def __init__(self) -> None:
        self.device_index = 0
        self.video_capture = cv2.VideoCapture(self.device_index)
        self.video_capture.set(3, 1280)
        self.video_capture.set(4, 720)
        self.running = True
        self.vision_manager = VisionManager()

    def run(self):
        while self.running:
            ret, frame = self.video_capture.read()
            if ret:
                self.vision_manager.excute_frame(frame)

                # Display the resulting image
                cv2.imshow('Video', frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    Logger.info("Click q to quit")
                    break
        
        self.video_capture.release()
        cv2.destroyAllWindows()
        Logger.debug("Exited face recognition program.")

    def stop(self):
        self.running = False
        Logger.debug("Set running to False.")


def crtl_c_handler(web_cam, signal, frame):
    Logger.debug("Ctrl+C was pressed. Going to exit the face recognition program")
    web_cam.stop()
    time.sleep(1)
    Logger.debug("Handle Ctrl+C successed.")
    sys.exit(0)


if __name__ == "__main__":
    webcam = WebCam()
    signal.signal(signal.SIGINT, partial(crtl_c_handler, webcam))
    try:
        webcam.run()
    except Exception as ex:
        Logger.error(f"Face recognition program has a unpected exception. error: {str(ex)}")
        traceback.print_exc()


