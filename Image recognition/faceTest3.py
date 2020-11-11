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


camera = cv2.VideoCapture(0)

while (camera.isOpened()):
    ret, frame = camera.read()
    dets, score , idx = detector.run(frame, 0)

    distance = []

    for i , o in enumerate(dets):
        shape = shape_predictor(camera , 0)

        face_descriptor = face_rec_model.compute_face_descriptor(frame ,shape)

        d_test = np.array(face_descriptor)

        x1 = o.left()
        y1 = o.top()
        x2 = o.right()
        y2 = o.bottom()

        cv2.rectangle(frame , (x1,y1) , (x2,y2) , (0,0,255) , 4)

        for i in descriptors:
            dist_ = np.linalg.norm(i -d_test)
            distance.append(dist_)

    candidate_distance_dict = dict(zip(candidate , distance))

    print(candidate)



    candidate_distance_dict_sorted = sorted(candidate_distance_dict.items() , key=lambda d: d[1])

    print(candidate_distance_dict_sorted)

    try:
        result = candidate_distance_dict_sorted[0][0]
        cv2.putText(frame , result , (x1 , y1) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (255,255,255) , 2 , cv2.LINE_AA)
    except IndexError:
        pass
    #camera = cv2.cvtColor(camera , cv2.COLOR_BGR2RGB)
    cv2.imshow('test' , frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()
