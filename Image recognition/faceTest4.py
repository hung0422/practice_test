import sys, os, dlib, glob, numpy , time
from skimage import io
import cv2

# 人臉68特徵點模型路徑
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 人臉辨識模型路徑
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# 比對人臉圖片資料夾名稱
faces_folder_path = './image'

# 載入人臉檢測器
detector = dlib.get_frontal_face_detector()

# 比對人臉描述子列表
descriptors = []

# 比對人臉名稱列表
candidate = []

# 針對比對資料夾裡每張圖片做比對:
# 1.人臉偵測
# 2.特徵點偵測
# 3.取得描述子
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    base = os.path.basename(f)
    # 依序取得圖片檔案人名
    candidate.append(os.path.splitext(base)[0])
    img = cv2.imread(f)

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1.人臉偵測
    dets = detector(grey, 0)

    for k, d in enumerate(dets):
        # 2.特徵點偵測
        shape = shape_predictor(img, d)

        # 3.取得描述子，128維特徵向量
        face_descriptor = face_rec_model.compute_face_descriptor(img, shape)
        # 轉換numpy array格式
        v = numpy.array(face_descriptor)
        descriptors.append(v)

# 針對需要辨識的人臉同樣進行處理
img = cv2.VideoCapture('789.mp4')

frame_count = 0
FPS = "0"

while (img.isOpened()):
    ret, frame = img.read()

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    dets = detector(grey, 0)

    distance = []
    for k, d in enumerate(dets):
        try:
            shape = shape_predictor(frame, d)

            face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)
            d_test = numpy.array(face_descriptor)
        except:
            pass

        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()
        # 以方框標示偵測的人臉

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4, cv2.LINE_AA)

        # 計算歐式距離
        try:
            for i in descriptors:
                dist_ = numpy.linalg.norm(i - d_test)
                distance.append(dist_)
        except NameError:
            pass

    # 將比對人名和比對出來的歐式距離組成一個dict
    c_d = dict(zip(candidate, distance))

    # 根據歐式距離由小到大排序
    cd_sorted = sorted(c_d.items(), key=lambda d:d[1])
    # 取得最短距離就為辨識出的人名
    try:
        rec_name = cd_sorted[0][0]
        if cd_sorted[0][1] < 0.47:
            # 將辨識出的人名印到圖片上面
            cv2.putText(frame, rec_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'unknown', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    except IndexError:
        pass

    # 取得FPS
    if frame_count == 0:
        d_t = time.time()
    frame_count += 1
    if frame_count >= 10:
        d_t = time.time() - d_t
        FPS = "FPS=%1f" % (10 / d_t)
        frame_count = 0

    # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
    cv2.putText(frame, FPS, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


    cv2.imshow('test', frame)
    # 按'esc'可以關閉視窗
    if cv2.waitKey(1) == 27:
        break
img.release()
cv2.destroyAllWindows()