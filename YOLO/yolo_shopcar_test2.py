import cv2
import numpy as np
import imutils
import time

accum = 1
list1 = []
list2 = []
tem_list = []

net = cv2.dnn.readNetFromDarknet("./testtest000/yolov4.cfg", "./testtest000/weights/yolov4_last.weights")

# net中所有層的資訊
layer_names = net.getLayerNames()
# 輸出層資訊
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# 讀取類別名稱
classes = [line.strip() for line in open("./testtest000/obj.names")]
# 設定類別顏色
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]
# colors = [(0, 0, 255)]


cap = cv2.VideoCapture('VIDEO0014.mp4')

frame_count = 0
FPS = "0"
# zzz = 2
while (cap.isOpened()):
    hasFrame, frame = cap.read()

    # forward propogation
    # 影像縮放
    img = cv2.resize(frame, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    # (影像,輸入資料尺度,輸出影像尺寸,從各通道減均值,R、B通道是否交換,影像是否截切)
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), (0, 0, 0), True, crop=False)
    # 設定網路
    net.setInput(blob)

    # 輸出結果陣列大小
    outs = net.forward(output_layers)

    # get detection boxes
    class_ids = []
    confidences = []
    boxes = []

    tem_accum = 1

    for out in outs:
        for detection in out:
            # 取得坐標及信心度
            tx, ty, tw, th, confidence = detection[0:5]
            # 辨識到的類別的分數
            scores = detection[5:]
            # 將分數最大的ID取出來
            class_id = np.argmax(scores)
            if confidence > 0.3:
                center_x = int(tx * width)
                center_y = int(ty * height)
                w = int(tw * width)
                h = int(th * height)

                # 取得箱子方框座標
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # draw boxes
    # 去除多餘重疊且信心度低的區域
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN

    # 框住偵測物件區域
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            # 取出對應到的類別
            label = str(classes[class_ids[i]])
            # 取出對應到的顏色
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 3, color, 3)

            # loc_time = time.localtime()
            # loc_time_str = time.strftime('%Y/%m/%d %X', loc_time)

            # print(label , (x, y), (x + w, y + h) , loc_time_str ,pp)

            if accum % 2 != 0:
                if accum == 1:
                    tem_list.append(label)
                    if tem_accum == len(indexes):
                        for eee in range(0, len(tem_list)):
                            list1.append(tem_list[0])
                            tem_list.remove(tem_list[0])
                elif accum != 1:
                    tem_list.append(label)
                    if tem_accum == len(indexes):
                        for www in range(0, len(list1)):
                            list1.remove(list1[0])
                        for eee in range(0, len(tem_list)):
                            list1.append(tem_list[0])
                            tem_list.remove(tem_list[0])

            elif accum % 2 == 0:
                if accum == 2:
                    tem_list.append(label)
                    if tem_accum == len(indexes):
                        for eee in range(0, len(tem_list)):
                            list2.append(tem_list[0])
                            tem_list.remove(tem_list[0])
                elif accum != 2:
                    tem_list.append(label)
                    if tem_accum == len(indexes):
                        for www in range(0, len(list2)):
                            list2.remove(list2[0])
                        for eee in range(0, len(tem_list)):
                            list2.append(tem_list[0])
                            tem_list.remove(tem_list[0])
            if tem_accum == len(indexes):
                print('list1:', list1)
                print('list2:', list2)

                if accum != 1:
                    if accum % 2 == 0:
                        print(accum)
                        if len(list1) > len(list2):
                            for i in range(len(list1)):
                                if list1[i] not in list2:
                                    print(list1[i], '被取走了')
                        elif len(list1) < len(list2):
                            for i in range(len(list2)):
                                if list2[i] not in list1:
                                    print(list2[i], '放回來了')
                    elif accum % 2 != 0:
                        print(accum)
                        if len(list1) < len(list2):
                            for ii in range(len(list2)):
                                if list2[ii] not in list1:
                                    print(list2[ii], '被取走了')
                        elif len(list1) > len(list2):
                            for ii in range(len(list1)):
                                if list1[ii] not in list2:
                                    print(list1[ii], '放回來了')
            tem_accum += 1
            print('===========')
    accum += 1

    # 取得FPS
    if frame_count == 0:
        d_t = time.time()
    frame_count += 1
    if frame_count >= 10:
        d_t = time.time() - d_t
        FPS = "FPS=%1f" % (10 / d_t)
        frame_count = 0

    # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
    cv2.putText(img, FPS, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Frame", imutils.resize(img, width=850))
    # cv2.imwrite('./picture/{}.jpg'.format(str(zzz)),img)
    # print(zzz)
    # zzz += 1
    # 按'q'關掉
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()