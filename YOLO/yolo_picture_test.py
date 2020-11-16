import cv2
import numpy as np
import time

# 讀取類別名稱
LABELS = open('./test2/project1101/obj.names').read().strip().split("\n")
nclass = len(LABELS)

# 為每個類別隨機產生顏色
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(nclass, 3), dtype='uint8')

# 使用yolov4設定檔及訓練好的模型
net = cv2.dnn.readNetFromDarknet('./test2/project1101/yolov4.cfg', './test2/project1101/weights/yolov4_3000.weights')

# 載入圖片並獲取其維度
img = cv2.imread('./test2/IMG_7488.jpg')
(H, W) = img.shape[:2]

# 獲取YOLO輸出層的名字
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# (影像,輸入資料尺度,輸出影像尺寸,從各通道減均值,R、B通道是否交換,影像是否截切)
blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()

# 顯示預測所花費時間
print('YOLO模型花費 {:.2f} 秒來預測一張圖片'.format(end - start))

# 初始化邊界框，信心度以及類別
boxes = []
confidences = []
classIDs = []

# 迭代每個輸出層，總共三個
for output in layerOutputs:
    # 迭代每個檢測
    for detection in output:
        # 提取類別ID和信心度
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        # 只保留信心度大於某值的邊界框
        if confidence > 0.5:
            # 將邊界框的坐標還原至與原圖片相匹配，返回的是邊界框的中心坐標以及邊界框的寬度和高度
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")


            # 計算邊界框的左上角位置
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))

            # 更新邊界框，信心度以及類別
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

# 去除多餘重疊且信心度低的區域
idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

# 確保至少一個邊界框
if len(idxs) > 0:
    # 迭代每個邊界框
    for i in idxs.flatten():
        # 提取邊界框的坐標
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        # 繪製邊界框以及在左上角添加類別標籤和信心度
        color = [int(c) for c in COLORS[classIDs[i]]]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        text = '{}: {:.3f}'.format(LABELS[classIDs[i]], confidences[i])
        (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(img, (x, y-text_h-baseline), (x + text_w, y), color, -1)
        cv2.putText(img, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        print(text)
cv2.imshow('test',img)
cv2.waitKey(0)
cv2.destroyAllWindows()