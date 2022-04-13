from func import*
img = cv2.imread('/Users/chenlingzi/Desktop/lena.jpeg')
#传入3通道图像
img_0 = img_equalize_hist(img)#直方图均衡
#打印直方图
title = 'hist'
show_hist(img,title)#title默认为hist，可不传

img_1 = local_enhance(img)#对比度增强
img_2 = change_contrast(img,1.2)#可调节，0-1减弱，1-2增强

img_2 = img_2[:, :, (2, 1, 0)]#若要用plt打印彩色图，调换以下顺序
plt.imshow(img_2)
plt.show()