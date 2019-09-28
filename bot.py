import cv2
import time
import pyautogui
import numpy as np
import sys

sys.setrecursionlimit(100000)
num_size = 64
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

def load_number_img():
    for i in range(1, 10):
        num.append(cv2.imread(f'{i}.png', cv2.IMREAD_GRAYSCALE))
        print(num[i].shape)
        num[i] = cv2.resize(num[i], (num_size, num_size))
        num[i] = cv2.threshold(num[i], 128, 255, cv2.THRESH_BINARY)[1]

def check_num(img, x, y):
    match = [0 for i in range(10)]
    for i in range(1, 10):
        print(i, )
        for xx in range(num_size):
            for yy in range(num_size):
                if(abs(num[i][yy][xx] - img[y+yy][x+xx])<10):
                    match[i]+=1
                    # print(1,end='')
                else:
                    # print(0,end='')
                    pass
            # print()
    print(match)

time.sleep(1)
#img = pyautogui.screenshot('sceenshot.png')
img = cv2.imread('sceenshot.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(int(img.shape[1]/1),int(img.shape[0]/1)))
num = [0]   #starter
load_number_img()
ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
x = 0
y = int(img.shape[0]/2)
while(thresh[y,x] < 128):
    x += 1
fill(thresh, x, y, 128)
thresh = crop_it(thresh)
thresh = crop_it_rev(thresh)
print(thresh.shape)
#(424, 320)
check_num(thresh, 14+64+2, 156+128+4)
print("done")

cv2.imshow('display', thresh)
cv2.waitKey()

#time.sleep(5)
cv2.destroyAllWindows()
