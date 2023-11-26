import torch
from ultralytics import YOLO
import cv2
import cvzone
import math

print(f"torch version: {torch.__version__}, cuda version: {torch.version.cuda}")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}, device: {torch.cuda.current_device()}")

num_devices = torch.cuda.device_count()
print(f"Total number of GPU devices: {num_devices}")

for device_index in range(num_devices):
    device_name = torch.cuda.get_device_name(device_index)
    print(f"GPU device {device_index}: {device_name}")


if device == 'cuda':
    torch.cuda.set_device(0)

model_directory = '/home/jetson/rnd_face_recognition/vision'
model = YOLO(f"{model_directory}/yolo_weights/yolov8n.pt")
class_names = model.names
print("Before device type:", model.device.type)
# result = model("/home/jetson/rnd_face_recognition/cv/selfie.jpg")
# print("result:", result)
# print("After device type:", model.device.type)


img = cv2.imread("/home/jetson/fer/justin.jpg")



video_capture = cv2.VideoCapture(0)


running = True
while running:
    ret, frame = video_capture.read()
    print("Width: %d, Height: %d, FPS: %d" % (video_capture.get(3), video_capture.get(4), video_capture.get(5)))
    detector = FER()
    print(detector.detect_emotions(img))
    if ret:
        flip_frame = cv2.flip(frame, 1)
        results = model(flip_frame, stream=True)
        print("After device type:", model.device.type)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w = x2 - x1
                h = y2 - y1
                cvzone.cornerRect(flip_frame, (x1, y1, w, h))

                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                cvzone.putTextRect(flip_frame, f'{class_names[cls]} {conf}', (max(0, x1), max(35, y1)),
                                scale=0.7, thickness=1, offset=3)

        # Display the resulting image
        cv2.imshow('Video', flip_frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Click q to quit")
            break

video_capture.release()
cv2.destroyAllWindows()