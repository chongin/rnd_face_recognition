import dlib

print(dlib.DLIB_USE_CUDA)

print(dlib.cuda.get_num_devices())

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor.dat")

rects = detector(gray, 0)

for rect in rects:

    shape = predictor(gray, rect)