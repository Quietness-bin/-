#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2 as cv
import os

# 图片放大倍数
n = 5

# 预处理填充图片：把所有填充图片reshape到固定大小
def before_handle_imgs():
    print("正在预处理填充图片：")
    readPath = "D:\\imgs"
    savePath = "D:\\data1"

    files = os.listdir(readPath)

    for file in files:
        imgPath = readPath + "\\" + file
        img = cv.imread(imgPath)
        img = cv.resize(img, (100, 75))
        cv.imwrite(savePath + "\\" + file, img)
    print("预处理填充图片已完成！")


# 预处理待填充图片：把待填充图片reshape到一个超大分辨率图片
def before_handle_img():
    print("正在预处理待填充图片：")
    width, height = 1000*n, 750*n
    readPath = "D:\\img\\img1.jpg"
    savePath = "D:\\img\\img2.jpg"
    img = cv.imread(readPath)
    img = cv.resize(img, (width, height))
    cv.imwrite(savePath, img)
    print("预处理待填充图片已完成！")


# 用字典存储每一图及其直方图
def build_index():
    print("正在计算各图片直方图：")
    readPath = "D:\\data1"
    files = os.listdir(readPath)
    dist = {}

    for file in files:
        imgPath = readPath + "\\" + file
        img = cv.imread(imgPath)
        hist = []
        for i in range(3):
            ht = cv.calcHist([img], [i], None, [256], [0, 256])
            hist.append(ht)
        dist[file] = hist

    print("各图片直方图计算已完成！")
    return dist


# 用最相近的图代替原图
def match_replace(dist):
    print("正在替换图片：")
    width, height = 1000*n, 750*n
    image = cv.imread("D:\\img\\img2.jpg")

    for i in range(0, height, 75):
        for j in range(0, width, 100):
            img = image[i:i+75, j:j+100, 0:3]

            hist = []
            for k in range(3):
                ht = cv.calcHist([img], [k], None, [256], [0, 256])
                hist.append(ht)

            sim = 0.0
            for key in dist:
                match0 = cv.compareHist(hist[0], dist[key][0], cv.HISTCMP_CORREL)
                match1 = cv.compareHist(hist[1], dist[key][1], cv.HISTCMP_CORREL)
                match2 = cv.compareHist(hist[2], dist[key][2], cv.HISTCMP_CORREL)
                match = match0 + match1 + match2

                if match > sim:
                    sim = match
                    rename = key
            image[i:i+75, j:j+100, 0:3] = cv.imread("D:\\data1\\" + rename)

    cv.imwrite("D:\\img\\img3.jpg", image)
    print("图片替换已完成！")


# 混合图片：融合填充图片和原图
def mix_image():
    print("正在融合图片：")
    image1 = cv.imread("D:\\img\\img3.jpg")
    image2 = cv.imread("D:\\img\\img2.jpg")
    dst = cv.addWeighted(image1, 0.2, image2, 0.6, 3)
    cv.imwrite("D:\\img\\img4.jpg", dst)
    print("图片融合已完成！")

if __name__ == "__main__":
    before_handle_imgs()
    before_handle_img()
    dist = build_index()
    match_replace(dist)
    mix_image()