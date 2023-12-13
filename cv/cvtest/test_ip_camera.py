import cv2
# vid = cv2.VideoCapture(0) # For webcam
vid = cv2.VideoCapture("rtsp://192.168.0.108:554/user=admin&password=admin123&channel=1&stream=0.sdp?") # For streaming links
while True:
  _,frame = vid.read()
  print(frame)
  cv2.imshow('Video Live IP cam',frame)
  key = cv2.waitKey(1) & 0xFF
  if key ==ord('q'):
    break

vid.release()
cv2.destroyAllWindows()
