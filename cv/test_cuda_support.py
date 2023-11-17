import torch
from ultralytics import YOLO

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
print("Before device type:", model.device.type)
result = model("/home/jetson/rnd_face_recognition/cv/selfie.jpg")
print("result:", result)
print("After device type:", model.device.type)