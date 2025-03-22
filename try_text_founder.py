import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('expression.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#Преобразовываем изображение в оттенки серого
_, img_black_white = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) #Преобразовываем изображение в черно-белое

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
config = r'--oem 3 --psm 6' 

cv2.imshow('Result', img_black_white)
cv2.waitKey(0)