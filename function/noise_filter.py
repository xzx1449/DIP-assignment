"""
presented by LiHaoYu
噪声：
    1.椒盐噪声 salt_pepper
    2.高斯噪声 gaussian_noise
    3.随机噪声 random_noise
滤波：
    1.线性平滑滤波  smooth
    2.线性锐化滤波  sharpen_filter
    3.中值滤波     median_filter
    4.低通滤波     low_pass_filter
    5.高通滤波     high_pass_filter
    6.带通滤波     bandpass_filter
    7.带阻滤波     bandstop_filter
"""
import cv2 as cv
import numpy as np
import math


def load_in_img(img_path):
    return cv.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)


def plt_in_cv(img, title):
    cv.imshow(title, img)
    cv.waitKey(0)


def pulse_noise(img, pa, pb, va, vb):
    """
    脉冲噪声
    :param img: 输入图像
    :param pa: 脉冲一极a产生概率
    :param pb: 脉冲另一极b产生概率
    :param va: 脉冲一极值a
    :param vb: 脉冲另一极值b
    :return: 加噪结果
    """
    assert pa + pb < 1, "噪声产生概率大于1"
    # size
    h, w, c = img.shape
    # mask
    pro = np.random.rand(h, w)
    pro[pro < pa] = -2
    pro[pro >= 1 - pb] = 2
    # value
    img[np.where(pro == -2)] = va
    img[np.where(pro == 2)] = vb
    return img


def salt_pepper(img, **kwargs):
    """
    椒盐噪声
    snr : 信噪比
    """
    snr = kwargs['snr']
    prob = 1 - snr
    # opencv extend 1 dim to 3 dim
    img = pulse_noise(img, prob / 2, prob / 2,
                      (0, 0, 0),
                      (255, 255, 255))
    return img


def random_noise(img, **kwargs):
    """
    随机噪声
    :param img:
    :param snr: 信噪比
    :return:
    """
    snr = kwargs['snr']
    prob = 1 - snr
    # opencv extend 1 dim to 3 dim
    img = pulse_noise(img, 0, prob,
                      (0, 0, 0),
                      (255, 255, 255))
    return img


def gaussian_noise(img, **kwargs):
    """
    高斯噪声
    :param img: 输入图像
    :param miu: 噪声分布均值  float or tuple(3 channel)
    :param sigma: 噪声分布方差  float or tuple(3 channel)
    :return: 高斯噪声加噪结果
    """
    # check
    miu = kwargs['miu']
    sigma = kwargs['sigma']
    if isinstance(miu, float):
        miu = (miu, miu, miu)
    if isinstance(sigma, float):
        sigma = (sigma, sigma, sigma)
    # generate noise
    noise = np.zeros(img.shape, img.dtype)
    cv.randn(noise, miu, sigma)
    # add
    img = cv.add(img, noise)
    return img


def smooth(img, **kwargs):
    """
    线性平滑滤波
    :param img:
    :param size: tuple(size=2)  Kernel size
    :return:
    """
    size = kwargs['size']
    return cv.blur(img, size)


def sharpen_filter(img, **kwargs):
    """
    线性锐化滤波
    :param img:
    :return: sharpened img
    """
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]])
    if 'kernel' in kwargs:
        kernel = kwargs['kernel']
    return cv.filter2D(img, -1, kernel)


def median_filter(img, **kwargs):
    """
    中值滤波
    :param img:
    :param size: 滤波器大小 int
    :return:
    """
    size = kwargs['size']
    return cv.medianBlur(img, size)


def frequency_filter(img_c, mask):
    """
    频域滤波
    :param img: 图像
    :param mask: 频域掩码
    :return: filtered img: 滤波后图像
    """
    # Fourier trans
    fft = cv.dft(np.float32(img_c), flags=cv.DFT_COMPLEX_OUTPUT)
    fftc = np.fft.fftshift(fft)
    # filter
    fft_filtering = fftc * mask
    # Fourier invtrans
    ifft = np.fft.ifftshift(fft_filtering)
    image_filtered = cv.idft(ifft)
    image_filtered = cv.magnitude(image_filtered[:, :, 0],
                                   image_filtered[:, :, 1])
    return image_filtered


def low_pass_filter(img, **kwargs):
    """
    低通滤波器
    :param img: 输入图像
    :param radius: 通过半径
    :return: 滤波后图像
    """
    radius = kwargs['radius']
    # size
    h, w = img.shape[:2]
    # mask
    med_h = int(h / 2)
    med_w = int(w / 2)
    mask = np.zeros((h, w, 2), dtype=np.float32)
    mask[med_h - radius:med_h + radius, med_w - radius:med_w + radius] = 1
    B,G,R = cv.split(img)
    Br = frequency_filter(B, mask)
    Gr = frequency_filter(G, mask)
    Rr = frequency_filter(R, mask)
    res = cv.merge([Br, Gr, Rr])
    return res


def high_pass_filter(img, **kwargs):
    """
    高通滤波器
    :param img: 输入图像
    :param radius: 通过半径
    :param n: Butterworth filter 阶数
    :return: 滤波后图像
    """
    n = 1
    radius = kwargs['radius']
    if 'n' in kwargs:
        n = kwargs['n']
    # size
    h, w = img.shape[:2]
    # mask
    med_h = int(h / 2)
    med_w = int(w / 2)
    mask = np.zeros((h, w, 2), dtype=np.float32)

    for i in range(0, h):
        for j in range(0, w):
            d = math.sqrt(pow(i - med_h, 2) + pow(j - med_w, 2))
            try:
                mask[i, j, 0] = mask[i, j, 1] = 1 / (1 + pow(radius / d, 2 * n))
            except ZeroDivisionError:
                mask[i, j, 0] = mask[i, j, 1] = 0
    B, G, R = cv.split(img)
    Br = frequency_filter(B, mask)
    Gr = frequency_filter(G, mask)
    Rr = frequency_filter(R, mask)
    res = cv.merge([Br, Gr, Rr])
    return res


def bandpass_filter(img, **kwargs):
    """
    带通滤波器
    :param img: 输入图像
    :param radius: 通过半径
    :param f: 通过频率中心
    :return: 滤波后图像
    """
    radius = kwargs['radius']
    f = kwargs['f']
    # size
    h, w = img.shape[:2]
    # mask
    med_h = int(h / 2)
    med_w = int(w / 2)
    mask = np.zeros((h, w, 2), dtype=np.float32)
    for i in range(0, h):
        for j in range(0, w):
            d = math.sqrt(pow(i - med_h, 2) + pow(j - med_w, 2))
            if radius - f / 2 < d < radius + f / 2:
                mask[i, j, 0] = mask[i, j, 1] = 1
            else:
                mask[i, j, 0] = mask[i, j, 1] = 0
    B, G, R = cv.split(img)
    Br = frequency_filter(B, mask)
    Gr = frequency_filter(G, mask)
    Rr = frequency_filter(R, mask)
    res = cv.merge([Br, Gr, Rr])
    return res


def bandstop_filter(img, **kwargs):
    """
    带阻滤波器
    :param img: 输入图像
    :param radius: 阻断半径
    :param f: 阻断频率中心
    :return: 滤波后图像
    """
    radius = kwargs['radius']
    f = kwargs['f']
    # size
    h, w = img.shape[:2]
    # mask
    med_h = int(h / 2)
    med_w = int(w / 2)
    mask = np.zeros((h, w, 2), dtype=np.float32)
    for i in range(0, h):
        for j in range(0, w):
            d = math.sqrt(pow(i - med_h, 2) + pow(j - med_w, 2))
            if radius - f / 2 < d < radius + f / 2:
                mask[i, j, 0] = mask[i, j, 1] = 0
            else:
                mask[i, j, 0] = mask[i, j, 1] = 1
    B, G, R = cv.split(img)
    Br = frequency_filter(B, mask)
    Gr = frequency_filter(G, mask)
    Rr = frequency_filter(R, mask)
    res = cv.merge([Br, Gr, Rr])
    return res


# img_pa = "../input.png"
#
# args = {'snr': 0.8}
# imgO = salt_pepper(img=load_in_img(img_pa), **args)
# plt_in_cv(imgO, "salt pepper noise img")
#
# args = {'size': (5, 5)}
# img_s = smooth(imgO, **args)
# plt_in_cv(img_s, "smoothed")
#
# args = {'size': 5}
# img_m = median_filter(imgO, **args)
# plt_in_cv(img_m, "medianed")
#
# args = {'radius': 30, 'f': 60}
# img_bp = bandpass_filter(imgO, **args)
# plt_in_cv(img_bp, "bandpass")
#
# args = {'radius': 30, 'f': 60}
# img_bs = bandstop_filter(imgO, **args)
# plt_in_cv(img_bs, "bandstop")
#
# args = {'radius': 200}
# img_lp = low_pass_filter(load_in_img(img_pa), **args)
# plt_in_cv(img_lp, "lowpass")
# #
# args = {'radius': 200}
# img_hp = high_pass_filter(load_in_img(img_pa), **args)
# plt_in_cv(img_hp, "highpass")
#
# args = {'miu': 40.0, 'sigma': 25.0}
# plt_in_cv(gaussian_noise(img=load_in_img(img_pa), **args),
#           "Gaussian noise img")
#
# args = {'snr': 0.8}
# plt_in_cv(random_noise(img=load_in_img(img_pa), **args),
#           "Random noise img")
