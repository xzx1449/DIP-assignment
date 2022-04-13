
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
# 解决中文显示问题



# 灰度转换
def img_equalize_hist(img,a):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.equalizeHist(gray)
    result = cv2.cvtColor(result,cv2.COLOR_GRAY2RGB)
    return result

#返回直方图
def show_hist( img ):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plt.hist(gray.ravel(), 256)
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        result = Image.open(buf)
        result = cv2.cvtColor(np.asarray(result),cv2.COLOR_RGBA2RGB)
        return result


def regu(num):
    if(num>255):
        return 255
    elif num < 0:
        return 0
    else :
        return num

def change_contrast(img , a):
    coefficent = a[0]
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cal = 0
    for i in range(abs(imggray.shape[0])):
        for j in range(abs(imggray.shape[1])):
           cal = cal + imggray[i,j]
    cal = cal / imggray.size
    for i in range(abs(imggray.shape[0])):
        for j in range(abs(imggray.shape[1])):
            newgray = cal + coefficent * (imggray[i,j] - cal)
            oldgray = imggray[i,j]
            if(oldgray<0.00001):
                img[i,j,0] = 0
                img[i,j,1] = 0
                img[i,j,2] = 0
            else:
                img[i, j, 0] = int(regu(img[i, j, 0] * newgray / oldgray))
                img[i, j, 1] = int(regu(img[i, j, 1] * newgray / oldgray))
                img[i, j, 2] = int(regu(img[i, j, 2] * newgray / oldgray))
    return img