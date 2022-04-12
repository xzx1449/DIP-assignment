import cv2

def hello(img,a):
    print('收到的参数列表：',a)
    cv2.threshold(img,140,255,0,img)
    return img
    # return 'hello'