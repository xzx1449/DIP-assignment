
import cv2
import numpy as np
import matplotlib.pyplot as plt
# 解决中文显示问题


# 读取图片

# 灰度转换
def img_equalize_hist(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.equalizeHist(gray)
    return result

#显示直方图
def show_hist( img , title = 'hist'):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.hist(img.ravel(), 256), plt.title(title)
    plt.show()



def _location_transform(c_position: int, total: int) -> int:
    """位置转换，返回正确位置"""
    if c_position < 0:
        return 0
    elif c_position > total:
        return total - 1
    else:
        return c_position


def _is_shadow(local_mean, local_std, global_mean, global_std, k0, k1, k2):
    """检测是否是阴影"""
    tmp1 = local_mean < k0 * global_mean
    tmp2 = (global_std * k1 <= local_std <= global_std * k2)
    return tmp1 and tmp2


def get_dead_area(img: np.ndarray, local_size=3, k0=0.4, k1=0.02, k2=0.4):
    """返回暗色区域"""
    """全局均值和标准差"""
    global_mean = np.mean(img.flatten())
    global_std = np.std(img.flatten())

    """"""
    shadow_matrix = np.zeros_like(img)

    """比较"""
    h, w, _ = img.shape
    local_part_size = np.floor(local_size / 2.)
    local_part_size = local_part_size.astype(int)
    for i, row in enumerate(img):
        for j, pix in enumerate(row):
            """局部位置坐标"""
            start_i = _location_transform(i - local_part_size, h)
            end_i = _location_transform(i + local_part_size, h)
            start_j = _location_transform(j - local_part_size, w)
            end_j = _location_transform(j + local_part_size, w)

            """局部位置统计数据"""
            local_mean = np.mean(img[start_i:end_i, start_j:end_j].flatten())
            local_std = np.std(img[start_i:end_i, start_j:end_j].flatten())

            """"""
            shadow_matrix[i][j] = _is_shadow(
                local_mean, local_std, global_mean, global_std, k0, k1, k2)
    return shadow_matrix


def local_enhance(img: np.ndarray, local_size=3, k0=0.4, k1=0.02, k2=0.4):
    """"""
    """获取暗色区域"""
    shadow_matrix = get_dead_area(img, local_size, k0, k1, k2)

    """暗色增强"""
    tmp1 = img * shadow_matrix * 3
    tmp2 = np.logical_not(shadow_matrix)
    tmp2 = tmp2.astype(int)
    tmp2 = img * tmp2
    result = tmp1 + tmp2
    return result

def regu(num):
    if(num>255):
        return 255
    elif num < 0:
        return 0
    else :
        return num

def change_contrast(img , coefficent):
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