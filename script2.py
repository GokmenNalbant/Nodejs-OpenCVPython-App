import cv2
import sys
import os
import numpy as np
# print('#Hello from python')
# print(sys.argv[1] , "  ///////// " , sys.argv[2],int(sys.argv[3]), int(sys.argv[4]))

def convertGray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
def noiseRemoval(img):
    noiseRemoval = cv2.fastNlMeansDenoisingColored(img, None, 7, 8, 7, 21)
    return noiseRemoval
def thresholding(img):
    return cv2.adaptiveThreshold(convertGray(img),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
def erosion(img):
    return cv2.erode(thresholding(img), (7, 7), iterations=1)
def dilation(img):
    return cv2.dilate(thresholding(img), (7, 7), iterations=1)
def opening(img):
    return cv2.morphologyEx(thresholding(img), cv2.MORPH_OPEN, (5, 5))
def closing(img):
    return cv2.morphologyEx(thresholding(img), cv2.MORPH_CLOSE, (5, 5))
def brighnessAndContrast(img, brightness=255, contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
  
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
  
    if brightness != 0:
  
        if brightness > 0:
  
            shadow = brightness
  
            max = 255
  
        else:
  
            shadow = 0
            max = 255 + brightness
  
        al_pha = (max - shadow) / 255
        ga_mma = shadow
  
      
        cal = cv2.addWeighted(img, al_pha,
                              img, 0, ga_mma)
  
    else:
        cal = img
  
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
  
        cal = cv2.addWeighted(cal, Alpha,
                              cal, 0, Gamma)
  
    
    # cv2.putText(cal, 'B:{},C:{}'.format(brightness, 
    #                                     contrast), 
    #             (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
    #             1, (0, 0, 255), 2)
  
    return cal
def generateHistogram(img):
    height, width = img.shape[0], img.shape[1]
    histogram = np.zeros([256], np.int32)

    for x in range(0, height):
        for y in range(0, width):
            histogram[img[x,y]] +=1

    return histogram


def equalizeHistogram(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = generateHistogram(img)
    Pn = np.zeros([256], np.float32)

    for i in range(0, len(Pn)):
        Pn[i] = hist[i] / (img.shape[1] * img.shape[0])

    cdf = np.zeros([256], np.float32)
    for i in range(len(Pn)):
        for j in range(i+1):
            cdf[i] += Pn[j]

    cdf_with_constant = np.zeros([256], np.int32)
    for i in range(len(cdf)):
        cdf_with_constant[i] = 255*cdf[i]


    height, width = img.shape[0], img.shape[1]
    new_Image = np.zeros_like(img)
    for i in range(0, height):
        for j in range(0, width):
            new_Image[i, j] = cdf_with_constant[img[i, j]]

    return new_Image


img = cv2.imread(os.path.join(os.path.dirname(__file__),"uploads/" + sys.argv[1]))

if sys.argv[2] == '1':
    img = convertGray(img)
elif sys.argv[2] == '2':
    img = noiseRemoval(img)
elif sys.argv[2] == '3':
    img = erosion(img)
elif sys.argv[2] == '4':
    img = dilation(img)
elif sys.argv[2] == '5':
    img = brighnessAndContrast(img, int(sys.argv[3]), int(sys.argv[4]))
elif sys.argv[2] == '6':
    img = equalizeHistogram(img)

cv2.imwrite(os.path.join(os.path.dirname(__file__),"public/images/" + sys.argv[1]), img)
cv2.waitKey(0)

