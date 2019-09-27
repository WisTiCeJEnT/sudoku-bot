import cv2
import time
import pyautogui
import numpy as np
import sys

def fill(img, x, y, c):
    if(x<0 or y<0):
        return False
    if(x==img.shape[1] or y==img.shape[0]):
        return False
    if(img[y,x] != c and img[y,x]>250):
        img[y,x] = c
        fill(img, x+1, y, c)
        # fill(img, x-1, y, c)
        fill(img, x, y+1, c)
        fill(img, x, y-1, c)

def crop_it(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if(img[i,j] == 128):
                img = img[i:img.shape[0], j:img.shape[1]]
                return img

def crop_it_rev(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if(img[img.shape[0]-i-1,img.shape[1]-j-1] == 128):
                img = img[0:img.shape[0]-i-1, 0:img.shape[1]-j-1]
                return img


sys.setrecursionlimit(100000)
time.sleep(1)
img = pyautogui.screenshot('sceenshot.png')
img = cv2.imread('sceenshot.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
x = 0
y = int(img.shape[0]/2)
while(thresh[y,x] < 128):
    x += 1
fill(thresh, x, y, 128)
thresh = crop_it(thresh)
thresh = crop_it_rev(thresh)
print(thresh.shape)
print("done")

cv2.imshow('display', thresh)
cv2.waitKey()

#time.sleep(5)
cv2.destroyAllWindows()
