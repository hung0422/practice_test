'''
將影片OR攝影機畫面定時拍照 -> JPG轉binary -> 傳到kafka
'''

import cv2 ,imutils , sys
import numpy as np
from confluent_kafka import Producer

# 要開啟的影片或攝影機
cap = cv2.VideoCapture('../../Pyai0815/yolo/test2/VIDEO0014.mp4')
# 計數器
accum = 1

# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 主程式進入點
if __name__ == '__main__':
    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群在那裡?
        'bootstrap.servers': '192.168.1.81:9092',          # <-- 置換成要連接的Kafka集群
        'error_cb': error_cb                            # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(props)
    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'ak03.four_partition'
    try:
        print('Start sending messages ...')
        while (cap.isOpened()):
            # 讀取攝影機的一張畫面frame
            ret, frame = cap.read()
            # 顯示攝影機的一張畫面frame
            cv2.imshow('frame', imutils.resize(frame, width=850))
            # 實測大約是每2秒多拍一張照片並傳到kafka(為了要配合從kafka讀取出來並辨識的時間)
            if accum % 130 == 0:
                # 拍下螢幕當時畫面並存檔
                cv2.imwrite("jpg_to_kafka.jpg", frame)
                # 讀取剛剛拍下的照片
                img = cv2.imread('jpg_to_kafka.jpg')
                # 把jpg轉成binary
                img_encode = cv2.imencode('.jpg', img)[1]
                # data_encode = np.array(img_encode)  # <-- 這一行應該可以不用
                str_encode = img_encode.tostring()
                #print(str_encode)
                # 將轉換完的binary傳到kafka
                producer.produce(topicName, key=str(1), value=str_encode)
            accum += 1

            # 按'q'關掉
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)
    # 步驟5. 確認所有在Buffer裡的訊息都己經送出去給Kafka了
    producer.flush(10)
    print('Message sending completed!')
