import cv2
import time
import pyautogui
import numpy as np

time.sleep(1)
font = cv2.FONT_HERSHEY_COMPLEX
#img = pyautogui.screenshot('sceenshot.png')
img = cv2.imread('sceenshot.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(int(img.shape[1]/3),int(img.shape[0]/3)))
ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
thresh[100,201] = 255
for i in range(img.shape[0]-3):
    for j in range(img.shape[1]-3):
        count = 0
        for mi in range(3):
            for mj in range(3):
                if(thresh[mi+i,mj+j]==0):
                    count += 1
        if(count > 7):
            for mi in range(3):
                for mj in range(3):
                    thresh[mi+i,mj+j] = 128

print("done")

cv2.imshow('display', thresh)
cv2.waitKey(0)

cv2.destroyAllWindows()
