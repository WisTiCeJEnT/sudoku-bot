import cv2
import time
import pyautogui
import numpy as np
import sys
import os

sys.setrecursionlimit(100000)
num_size = 28

def sudoku_solver(problem_tbl):
    write_tbl_to_file(problem_tbl, "problem.spsv")
    os.system("./solver.cpp.out < problem.spsv > answer.spsv")
    return read_tbl_from_file("answer.spsv")
    
def read_tbl_from_file(filename):
    data_tbl = []
    f = open(filename, 'r').read()
    data = f.strip().split('\n')
    for row in data:
        data_tbl.append([int(x) for x in row.strip().split(' ')])
    return data_tbl

def write_tbl_to_file(tbl_data, filename):
    f = open(filename, 'w')
    for row in tbl_data:
        for col in row:
            f.write(f"{col} ")
        f.write("\n")
    f.close()

def fill_the_table(img):
    tbl = []
    pos_tbl = []
    for i in range(9):
        tmp = []
        tmp2 = []
        for j in range(9):
            #print(i,j)
            tmp.append(check_num(img, 14+(j*69), 156+(i*69)))
            tmp2.append(( 14+(j*69)+30, 156+(i*69)+30 ))
        tbl.append(tmp)
        pos_tbl.append(tmp2)
    return (tbl, pos_tbl)

def fill(img, x, y, new_color, old_color):
    if(x<0 or y<0):
        return False
    if(x==img.shape[1] or y==img.shape[0]):
        return False
    if(img[y,x] != new_color and abs(img[y,x]-old_color)<20):
        img[y,x] = new_color
        fill(img, x+1, y, new_color, old_color)
        # fill(img, x-1, y, c)
        fill(img, x, y+1, new_color, old_color)
        fill(img, x, y-1, new_color, old_color)

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
    for i in range(10):
        num.append(cv2.imread(f'{i}.png', cv2.IMREAD_GRAYSCALE))
        #print(num[i].shape)
        num[i] = cv2.threshold(num[i], 128, 255, cv2.THRESH_BINARY)[1]
        if(i == 0):
            num[i] = cv2.resize(num[i], (num_size, num_size))
            continue
        minx = num[i].shape[1]
        maxx = 0
        miny = num[i].shape[0]
        maxy = 0
        for j in range(num[i].shape[0]):
            for k in range(num[i].shape[1]):
                if(num[i][j, k] < 20):
                    minx = min(minx, k)
                    maxx = max(maxx, k)
                    miny = min(miny, j)
                    maxy = max(maxy, j)
        num[i] = num[i][miny:maxy, minx:maxx]
        num[i] = cv2.resize(num[i], (num_size, num_size))
        #print(minx, miny)
        #print(maxx, maxy)
        #cv2.imshow(f'{i}', num[i])

def check_num(full_img, x, y):
    img = full_img[y:y+60, x:x+60]
    #cv2.imshow(f"{x} {y}", img)
    match = [0 for i in range(10)]
    minx = img.shape[1]
    maxx = 0
    miny = img.shape[0]
    maxy = 0
    for j in range(img.shape[0]):
        for k in range(img.shape[1]):
            if(img[j, k] < 20):
                minx = min(minx, k)
                maxx = max(maxx, k)
                miny = min(miny, j)
                maxy = max(maxy, j)
    img = img[miny:maxy, minx:maxx]
    if(img.shape == (0,0)):
        return 0
    img = cv2.resize(img, (num_size, num_size))
    for i in range(10):
        for xx in range(num[i].shape[1]):
            for yy in range(num[i].shape[0]):
                if(abs(num[i][yy][xx] - img[yy][xx])<10):
                    match[i]+=1
    #print(match)
    #cv2.imshow(f"{x} {y} {match.index(max(match))}", img)
    return match.index(max(match))

def auto_answer(answer, x_start, y_start, pos_tbl, ratio, img):
    num_btn_pos = [(0,0)]
    for i in range(9):
        num_btn_pos.append(( (890*ratio)+y_start, ratio*(35+(70*i))+x_start ))
    holizon_ratio = img.shape[1]/pyautogui.size().width
    vertical_ratio = img.shape[0]/pyautogui.size().height
    for i in range(1,10):
        pyautogui.click(x=num_btn_pos[i][1]/holizon_ratio, y=num_btn_pos[i][0]/vertical_ratio)
        time.sleep(0.25)
        
    
    
time.sleep(1)
pyautogui.moveTo(1,1)
img = pyautogui.screenshot('sceenshot.png')
pyautogui.moveTo(100,100)
img = cv2.imread('sceenshot.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(int(img.shape[1]/1),int(img.shape[0]/1)))
num = []
load_number_img()
ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
x = 0
y = int(img.shape[0]/2)
while(thresh[y,x] < 128):
    x += 1
fill(thresh, x, y, 128, 255)
cut_point_y = thresh.shape[0]
cut_point_x = thresh.shape[1]
print(cut_point_x, " ", cut_point_y)
thresh = crop_it(thresh)
cut_point_y -= thresh.shape[0]
cut_point_x -= thresh.shape[1]
thresh = crop_it_rev(thresh)
print(cut_point_x, " ", cut_point_y)
tmp = img[850:-200, 389:1000]

#cv2.imshow('img', img[-400: , :])
print(thresh.shape)
x = 0
y = int(thresh.shape[0]/2)
while(thresh[y,x] > 20):
    x += 1
fill(thresh, x, y, 255, 0)
problem_tbl, position_tbl = fill_the_table(thresh)
answer_tbl = sudoku_solver(problem_tbl)
auto_answer(problem_tbl, cut_point_x, cut_point_y, position_tbl, 1, img)
#print(answer_tbl)

print("done")
#cv2.imshow("GG", img[:500 ,:])
#cv2.waitKey()
#time.sleep(5)
cv2.destroyAllWindows()
