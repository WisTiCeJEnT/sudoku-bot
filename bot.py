import cv2
import time
import pyautogui
import numpy as np

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



time.sleep(1)
font = cv2.FONT_HERSHEY_COMPLEX
#img = pyautogui.screenshot('sceenshot.png')
img = cv2.imread('sceenshot.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(int(img.shape[1]/3),int(img.shape[0]/3)))
ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
thresh[100,201] = 255
x = 0
y = int(img.shape[0]/2)
while(thresh[y,x] < 128):
    x += 1
print(x,y)
fill(thresh, x, y, 128)

print("done")

cv2.imshow('display', thresh)
cv2.waitKey(0)

cv2.destroyAllWindows()
