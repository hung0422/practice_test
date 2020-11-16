'''
影片OR攝影機 -> yolo辨識 -> 傳到kafka
'''


import cv2 , imutils , time , sys
import numpy as np
from confluent_kafka import Producer

# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)

# 步驟1. 設定要連線到Kafka集群的相關設定
props = {
    # Kafka集群在那裡?
    'bootstrap.servers': '192.168.1.170:9092',          # <-- 置換成要連接的Kafka集群
    'error_cb': error_cb                            # 設定接收error訊息的callback函數
}
# 步驟2. 產生一個Kafka的Producer的實例
producer = Producer(props)
# 步驟3. 指定想要發佈訊息的topic名稱
topicName = 'ak03.four_partition'

# 使用yolov4設定檔及訓練好的模型
net = cv2.dnn.readNetFromDarknet("../../Pyai0815/yolo/test2/testtest000/yolov4.cfg", "../../Pyai0815/yolo/test2/testtest000/weights/yolov4_last.weights")

# net中所有層的資訊
layer_names = net.getLayerNames()
# 輸出層資訊
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# 讀取類別名稱
classes = [line.strip() for line in open("../../Pyai0815/yolo/test2/testtest000/obj.names")]
# 設定類別顏色
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]
# colors = [(0, 0, 255)]


def kafkasend1(list):
    '''
    把哪一種類別的物品被取走的訊息傳給kafka
    :param list: 被取走的類別
    '''
    try:
        # 傳到kafka的值
        producer.produce(topicName, key=str(1), value=list)
        producer.poll(0)  # <-- (重要) 呼叫poll來讓client程式去檢查內部的Buffer
        print('key={}, value={} '.format(1, (list, '被取走了')))
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write(
            '%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                .format(len(producer)))
    except Exception as e:
        print(e)

def kafkasend2(list):
    '''
    把哪一種類別的物品被放回來的訊息傳給kafka
    :param list: 被放回來的類別
    '''
    try:
        # 傳到kafka的值
        producer.produce(topicName, key=str(2), value=list)
        producer.poll(0)  # <-- (重要) 呼叫poll來讓client程式去檢查內部的Buffer
        print('key={}, value={} '.format(2, (list, '放回來了')))
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write(
            '%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                .format(len(producer)))
    except Exception as e:
        print(e)

# 計數器(辨識完一輪會加1)
accum = 1

list1 = []
list2 = []
tem_list = []
# FPS
frame_count = 0
FPS = "0"
# 要開啟的影片或攝影機
cap = cv2.VideoCapture('../../Pyai0815/yolo/test2/VIDEO0014.mp4')

if __name__ == '__main__':
    while (cap.isOpened()):
        # 讀取攝影機的一張畫面frame
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
        # 初始化邊界框，信心度以及類別
        class_ids = []
        confidences = []
        boxes = []
        # 暫時的計數器(辨識完一個類別就會加1,每辨識完一輪會重置到1)
        tem_accum = 1

        for out in outs:
            for detection in out:
                # 取得坐標及信心度
                tx, ty, tw, th, confidence = detection[0:5]
                # 辨識到的類別的分數
                scores = detection[5:]
                # 將分數最大的ID取出來
                class_id = np.argmax(scores)
                # 只保留信心度大於某值的邊界框
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

                # 奇數輪
                if accum % 2 != 0:
                    # 在第一輪的時候
                    if accum == 1:
                        # 辨識完成的類別會存到一個暫時的list
                        tem_list.append(label)
                        # 在每一輪辨識完最後一個類別時
                        if tem_accum == len(indexes):
                            for eee in range(0, len(tem_list)):
                                # 把辨識完的結果存到list1
                                list1.append(tem_list[0])
                                # 清空暫時的list
                                tem_list.remove(tem_list[0])
                    elif accum != 1:
                        # 辨識完成的類別會存到一個暫時的list
                        tem_list.append(label)
                        # 在每一輪辨識完最後一個類別時
                        if tem_accum == len(indexes):
                            for www in range(0, len(list1)):
                                # 先清空list1
                                list1.remove(list1[0])
                            for eee in range(0, len(tem_list)):
                                # 把辨識完的結果存到list1
                                list1.append(tem_list[0])
                                # 清空暫時的list
                                tem_list.remove(tem_list[0])
                # 偶數輪
                elif accum % 2 == 0:
                    # 在第二輪的時候
                    if accum == 2:
                        tem_list.append(label)
                        if tem_accum == len(indexes):
                            for eee in range(0, len(tem_list)):
                                # 把辨識完的結果存到list2
                                list2.append(tem_list[0])
                                tem_list.remove(tem_list[0])
                    elif accum != 2:
                        tem_list.append(label)
                        if tem_accum == len(indexes):
                            for www in range(0, len(list2)):
                                # 先清空list2
                                list2.remove(list2[0])
                            for eee in range(0, len(tem_list)):
                                list2.append(tem_list[0])
                                tem_list.remove(tem_list[0])

                # 在每一輪辨識完最後一個類別時
                if tem_accum == len(indexes):
                    #print('list1:', list1)
                    #print('list2:', list2)

                    if accum != 1:
                        # 偶數輪
                        if accum % 2 == 0:
                            #print(accum)
                            # 如果這一輪少物品就檢查有甚麼物品被取走
                            if len(list1) > len(list2):
                                for i in range(len(list1)):
                                    if list1[i] not in list2:
                                        #print(list1[i], '被取走了')
                                        kafkasend1(list1[i])
                            # 如果這一輪多物品就檢查有甚麼物品被放回來
                            elif len(list1) < len(list2):
                                for i in range(len(list2)):
                                    if list2[i] not in list1:
                                        #print(list2[i], '放回來了')
                                        kafkasend2(list2[i])
                        # 奇數輪
                        elif accum % 2 != 0:
                            #print(accum)
                            if len(list1) < len(list2):
                                for ii in range(len(list2)):
                                    if list2[ii] not in list1:
                                        #print(list2[ii], '被取走了')
                                        kafkasend1(list2[ii])

                            elif len(list1) > len(list2):
                                for ii in range(len(list1)):
                                    if list1[ii] not in list2:
                                        #print(list1[ii], '放回來了')
                                        kafkasend2(list1[ii])
                # 每辨識完一個類別加一
                tem_accum += 1
                #print('===========')
            # 步驟5. 確認所有在Buffer裡的訊息都己經送出去給Kafka了
            producer.flush(10)
        # 每辨識完一輪加一
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
        # 顯示攝影機的一張畫面frame
        cv2.imshow("Frame", imutils.resize(img, width=850))

        # 按'q'關掉
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()