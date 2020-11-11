def faceTest(a):
    '''
    練習使用opencv+dlib偵測人臉
    :param a: 無
    :return: 無
    '''
    import cv2
    import dlib
    #開攝影機
    camera = cv2.VideoCapture(0)
    #dlib:人臉辨識
    detector = dlib.get_frontal_face_detector()
    #迴圈讀影片
    while (camera.isOpened()):
        ret , frame = camera.read()
        #偵測人臉和分數

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face , score , idx = detector.run(grey,0)

        for i , o in enumerate(face):
            x1 = o.left()
            y1 = o.top()
            x2 = o.right()
            y2 = o.bottom()
            text = '{:.2f}({})'.format(score[i],idx[i])
            #標示偵測到的人臉框框(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
            cv2.rectangle(frame , (x1,y1) , (x2,y2) , (0,0,255) , 4)
            #標示偵測到的分數(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度)
            cv2.putText(frame , text , (x1,y1) , cv2.FONT_HERSHEY_DUPLEX , 0.7 , (255,255,255) , 1)
        #輸出畫面
        cv2.imshow('test' , frame)
        #按'esc'可以關閉視窗
        if cv2.waitKey(1) == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

def main():
    faceTest(0)

if __name__ == '__main__':
    main()