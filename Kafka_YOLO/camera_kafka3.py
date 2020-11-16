'''
從kafka取出binary -> 轉回JPG -> yolo辨識 -> (傳到kafka(redis))
'''


from confluent_kafka import Consumer, KafkaException, KafkaError
import sys , cv2 , time
import numpy as np

# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)

# 轉換msgKey或msgValue成為utf-8的字串
def try_decode_utf8(data):
    if data:
        return data.decode('utf-8')
    else:
        return None

# 當發生Re-balance時, 如果有partition被assign時被呼叫
def print_assignment(consumer, partitions):
    result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
    print('Setting newly assigned partitions:', result)


# 當發生Re-balance時, 之前被assigned的partition會被移除
def print_revoke(consumer, partitions):
    result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
    print('Revoking previously assigned partitions: ' + result)

# 讀取類別名稱
classes = open('../../Pyai0815/yolo/test2/testtest000/obj.names').read().strip().split("\n")
nclass = len(classes)

# 為每個類別隨機產生顏色
np.random.seed(123)
COLORS = np.random.randint(0, 255, size=(nclass, 3), dtype='uint8')

# 使用yolov4設定檔及訓練好的模型
net = cv2.dnn.readNetFromDarknet('../../Pyai0815/yolo/test2/testtest000/yolov4.cfg', '../../Pyai0815/yolo/test2/testtest000/weights/yolov4_last.weights')

# 獲取YOLO輸出層的名字
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# 計數器(辨識完一輪會加1)
accum = 1
list1 = []
list2 = []
tem_list = []

if __name__ == '__main__':
    # 步驟1.設定要連線到Kafka集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    props = {
        'bootstrap.servers': '192.168.1.81:9092',         # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'group.id': 'iii',                             # ConsumerGroup的名稱 (置換成你/妳的學員ID)
        'auto.offset.reset': 'earliest',               # Offset從最前面開始
        'error_cb': error_cb                           # 設定接收error訊息的callback函數
    }

    # 步驟2. 產生一個Kafka的Consumer的實例
    consumer = Consumer(props)
    # 步驟3. 指定想要訂閱訊息的topic名稱
    topicName = 'ak03.four_partition'
    # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe([topicName], on_assign=print_assignment, on_revoke=print_revoke)

    # 步驟5. 持續的拉取Kafka有進來的訊息
    try:
        while True:
            # 請求Kafka把新的訊息吐出來
            records = consumer.consume(num_messages=500, timeout=1.0)  # 批次讀取
            if records is None:
                continue

            for record in records:
                # 檢查是否有錯誤
                if record is None:
                    continue
                if record.error():
                    # Error or event
                    if record.error().code() == KafkaError._PARTITION_EOF:
                        print('')
                        # End of partition event
                        # sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                        #                 (record.topic(), record.partition(), record.offset()))
                    else:
                        # Error
                        raise KafkaException(record.error())
                else:
                    # ** 在這裡進行商業邏輯與訊息處理 **
                    # 取出相關的metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()
                    # 取出msgKey與msgValue
                    msgKey = try_decode_utf8(record.key())
                    msgValue = record.value()

                    # 秀出metadata與msgKey & msgValue訊息
                    print('%s-%d-%d : (%s , %s)' % (topic, partition, offset, msgKey, msgValue))
                    # 讀取從kafka傳回來的照片
                    with open('kafka_to_jpg.jpg', 'wb') as f:
                        f.write(msgValue)

                    try:
                        # 載入圖片並獲取其維度
                        img = cv2.imread('kafka_to_jpg.jpg')
                        (H, W) = img.shape[:2]

                        # (影像,輸入資料尺度,輸出影像尺寸,從各通道減均值,R、B通道是否交換,影像是否截切)
                        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                        # 設定網路
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

                        # 暫時的計數器(辨識完一個類別就會加1,每辨識完一輪會重置到1)
                        tem_accum = 1

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
                                text = '{}: {:.3f}'.format(classes[classIDs[i]], confidences[i])
                                (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                                cv2.rectangle(img, (x, y - text_h - baseline), (x + text_w, y), color, -1)
                                cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                                text2 = text.split(':')[0]
                                # print(text)
                                # 奇數輪
                                if accum % 2 != 0:
                                    # 在第一輪的時候
                                    if accum == 1:
                                        # 辨識完成的類別會存到一個暫時的list
                                        tem_list.append(text2)
                                        # 在每一輪辨識完最後一個類別時
                                        if tem_accum == len(idxs):
                                            for eee in range(0, len(tem_list)):
                                                # 把辨識完的結果存到list1
                                                list1.append(tem_list[0])
                                                # 清空暫時的list
                                                tem_list.remove(tem_list[0])
                                    elif accum != 1:
                                        # 辨識完成的類別會存到一個暫時的list
                                        tem_list.append(text2)
                                        # 在每一輪辨識完最後一個類別時
                                        if tem_accum == len(idxs):
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
                                        tem_list.append(text2)
                                        if tem_accum == len(idxs):
                                            for eee in range(0, len(tem_list)):
                                                # 把辨識完的結果存到list2
                                                list2.append(tem_list[0])
                                                tem_list.remove(tem_list[0])
                                    elif accum != 2:
                                        tem_list.append(text2)
                                        if tem_accum == len(idxs):
                                            for www in range(0, len(list2)):
                                                # 先清空list2
                                                list2.remove(list2[0])
                                            for eee in range(0, len(tem_list)):
                                                list2.append(tem_list[0])
                                                tem_list.remove(tem_list[0])
                                # 在每一輪辨識完最後一個類別時
                                if tem_accum == len(idxs):
                                    #print('list1:', list1)
                                    #print('list2:', list2)

                                    if accum != 1:
                                        # 偶數輪
                                        if accum % 2 == 0:
                                            print(accum)
                                            # 如果這一輪少物品就檢查有甚麼物品被取走
                                            if len(list1) > len(list2):
                                                for i in range(len(list1)):
                                                    if list1[i] not in list2:
                                                        print(list1[i], '被取走了')
                                            # 如果這一輪多物品就檢查有甚麼物品被放回來
                                            elif len(list1) < len(list2):
                                                for i in range(len(list2)):
                                                    if list2[i] not in list1:
                                                        print(list2[i], '放回來了')
                                        # 奇數輪
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
                                # 每辨識完一個類別加一
                                tem_accum += 1
                                #print('===========')
                        # 每辨識完一輪加一
                        accum += 1
                        #cv2.imshow('test', img)
                        #cv2.waitKey(0)
                        #cv2.destroyAllWindows()
                    except AttributeError:
                        pass

    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except Exception as e:
        sys.stderr.write(e)

    finally:
        # 步驟6.關掉Consumer實例的連線
        consumer.close()


