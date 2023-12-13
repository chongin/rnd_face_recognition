import cv2

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create a GPU-based MOG2 background subtractor
mog2 = cv2.cuda.createBackgroundSubtractorMOG2()

# Create a CUDA stream
stream = cv2.cuda_Stream()

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Upload the frame to GPU
    gpu_frame = cv2.cuda_GpuMat()
    gpu_frame.upload(frame)

    # Apply background subtraction on GPU with a learning rate and stream
    gpu_fgmask = mog2.apply(gpu_frame, learningRate=0.01, stream=stream)

    # Download the result from GPU to CPU
    # fgmask = gpu_fgmask.download()

    # Display the original frame and the processed frame
    cv2.imshow('Original Frame', frame)
    # cv2.imshow('Foreground Mask', fgmask)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
