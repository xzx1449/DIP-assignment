# -*- coding: utf-8 -*
"""
图像几何变换
作者: qiaopengju
实现功能：
1.平移:     translate(img, tx, ty)
2.旋转:     rotate(img, theta)
3.缩放:     scale(img, sx, sy)
4.错切:     miscut(img, mx, my)
5.仿射变换: affine(img, tx=0, ty=0, sx=1, sy=1, mx=0, my=0):
"""
import numpy as np
import math

# 得到变换后的图像，T是变换矩阵，sx，sy为在x, y轴的缩放因子
def transform(img, T, sx, sy):
    invT = np.linalg.inv(T)
    rows, cols = img.shape[:2]
    new_r = int(sy * rows)
    new_c = int(sx * cols)
    img_result = np.zeros((new_r, new_c, 3))
    for i in range(new_r):
        for j in range(new_c):
            # 得到平移后的position，
            # T * pos_old = pos_new
            pos_new = np.array([[i], [j], [1]])
            pos_old = np.dot(invT, pos_new)
            if pos_old[0][0] >= 0 and pos_old[0][0] < rows and pos_old[1][0] >= 0 and pos_old[1][0] < cols:
                img_result[i, j, :] = img[int(pos_old[0][0]), int(pos_old[1][0]), :]
    return img_result

# 1.平移(tx,ty)
def translate(img, par):
    tx = int(par[0])
    ty = int(par[1])
    print(tx, ty, "\n")
    T = np.array([[1,0,ty],
				  [0,1,tx],
				  [0,0,1]])
    return transform(img, T, 1, 1)

# 2.旋转，顺时针旋转theta度(角度)
def rotate(img, par):
    theta = int(par[0] * 0.9)
    theta = math.radians(theta)
    T = np.array([[math.cos(theta),math.sin(theta),0],
	              [-math.sin(theta),math.cos(theta),0],
	              [0,0,1]])
    return transform(img, T, 1, 1)

# 3.缩放，分别将x，y方向缩放为sx，sy倍
def scale(img, par):
    sx = (par[0]+100)/100
    sy = (par[1]+100)/100
    T = np.array([[sy,0,0],
                  [0,sx,0],
                  [0,0,1]])
    return transform(img, T, sx, sy)

# 4.错切
def miscut(img, par):
    mx = int(par[0]/20)
    my = int(par[1]/20)
    T = np.array([[1,my,0],
				  [mx,1,0],
				  [0,0,1]])
    return transform(img, T, 1, 1)

# 5.仿射变换
def affine(img, par):
    tx=int(par[0])
    ty=int(par[1])
    sx=(par[2]+100)/100
    sy=(par[3]+100)/100
    mx=int(par[4]/20)
    my=int(par[5]/20)
    T = np.array([[sy,my,ty],
				  [mx,sx,tx],
				  [0,0,1]])
    return transform(img, T, sx, sy)