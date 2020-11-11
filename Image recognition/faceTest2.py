import sys , os , dlib , glob
import numpy as np
from skimage import io
import cv2

faces_data_path = './image'

detector = dlib.get_frontal_face_detector()

shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

descriptors = []

candidate = []

for file in glob.glob(os.path.join(faces_data_path,'*.jpg')):
    base = os.path.basename(file)
    candidate.append(os.path.splitext(base)[0])

    img = io.imread(file)

    dets = detector(img , 1)

    for i , o in enumerate(dets):
        shape = shape_predictor(img , o)

        face_descriptor = face_rec_model.compute_face_descriptor(img , shape)

        v = np.array(face_descriptor)
        descriptors.append(v)


img = io.imread('123.jpg')

dets = detector(img , 1)

distance = []

for i , o in enumerate(dets):
    shape = shape_predictor(img , o)

    face_descriptor = face_rec_model.compute_face_descriptor(img ,shape)

    d_test = np.array(face_descriptor)

    x1 = o.left()
    y1 = o.top()
    x2 = o.right()
    y2 = o.bottom()

    cv2.rectangle(img , (x1,y1) , (x2,y2) , (0,0,255) , 4)

    for i in descriptors:
        dist_ = np.linalg.norm(i -d_test)
        distance.append(dist_)

candidate_distance_dict = dict(zip(candidate , distance))

candidate_distance_dict_sorted = sorted(candidate_distance_dict.items() , key=lambda d: d[1])
result = candidate_distance_dict_sorted[0][0]

cv2.putText(img , result , (x1 , y1) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (255,255,255) , 2 , cv2.LINE_AA)

img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
cv2.imshow('test' , img)

cv2.waitKey(0)
cv2.destroyAllWindows()
