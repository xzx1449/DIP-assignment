import imp
from function.example import hello
from function.geometryTrans import *
from function.func import*
from function.noise_filter import *
fun = [
    #图像处理函数列表,函数名任意。GUI通过此列表的顺序访问功能函数，如：
    #   第 一 个界面的第 一 个功能“均衡灰度直方图”，对应的功能函数因该放在此列表fun[0][0]位置处。
    #感觉说不太清楚，直接看例子hello函数的调用方式吧
    # （函数的第一个参数为输入图像，第二个参数为额外的参数列表）
    #灰度图
    [img_equalize_hist,change_contrast,show_hist],
    #几何变换
    [scale, translate, rotate, miscut, affine],
    #添加噪声
    [salt_pepper,gaussian_noise,random_noise],
    #滤波变换
    [smooth,sharpen_filter,median_filter,low_pass_filter,high_pass_filter,bandpass_filter,bandstop_filter],
    #例子
    [hello]
]