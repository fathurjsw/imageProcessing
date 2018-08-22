import cv2
import numpy as np 
from transfrom import transform

class ImageTransform  :
    def __init__(self, url):
        self.image = cv2.imread(url)
        self.shape = ""

    def resize(self, newWidth, interpolationMethod):
        interpolationAlgoritma={
            "area": cv2.INTER_AREA,
            "nearest": cv2.INTER_NEAREST,
            "linear":cv2.INTER_LINEAR,
            "cubic":cv2.INTER_CUBIC,
            "lanczos4": cv2.INTER_LANCZOS4,
        }
        image = self.image
        heigth, width,_ = image.shape
        imageRatio = newWidth / width
        newDimention = (newWidth, int(heigth * imageRatio))
        self.image = cv2.resize(image, newDimention,interpolationAlgoritma[interpolationMethod] )
        return self

    def gausianBlur(self,matrixSize):
        greyImage = cv2.cvtColor(self.image.copy(),cv2.COLOR_BGR2GRAY)
        self.greyImage =  cv2.GaussianBlur(greyImage, matrixSize, 0)
        return self

    def edgeDetect(self, method = 'canny'):
        self.gausianBlur((7,7))
        self.newImage = self.image.copy()
       
        edge = cv2.Canny(self.greyImage, 100,100)
        if method == 'laplace' : edge = cv2.Laplacian(self.greyImage,cv2.CV_8UC1)
        _,contours,_ = cv2.findContours(edge.copy(),1,1)
        self.contours = contours
        maxArea = 0
        maxPeri = 0
        maxCountour = 0

        for i in contours:
            area = cv2.contourArea(i)
            if area > maxArea:
                maxArea = area
                maxCountour = i
        # for i in contours : 
        #     peri = cv2.arcLength(i, True)
        #     if peri > maxPeri:
        #        maxPeri = peri
        #        maxCountour = i
        

        self.maxCountour = maxCountour
        return self

    def applyContour(self):
        newImage = cv2.drawContours(self.image, self.contours,-1,(0,0,255), 1)
        return newImage

    def getRectangle(self):
        rect= cv2.minAreaRect(self.maxCountour)
        box = cv2.boxPoints(rect)
        box = np.intc(box)
        peri=cv2.arcLength(box,True)
        approx=cv2.approxPolyDP(box,0.02*peri,True)
        w,h,arr = transform(approx)

        pts2=np.float32([[0,0],[w,0],[0,h],[w,h]])
        pts1=np.float32(arr)
        M=cv2.getPerspectiveTransform(pts1,pts2)
        newImage=cv2.warpPerspective(self.image, M,(w,h))
        ratio = newImage.size / self.image.size
        print(ratio)
        if ratio > 0.2 and ratio < 1: self.image = newImage
        h,w,_ = self.image.shape
        print(w,h)
        if w > h : self.rotate(90)
        return self


    def cropImage(self):
        contour = self.maxCountour
        peri=cv2.arcLength(contour,True)
        approx=cv2.approxPolyDP(contour,0.02*peri,True)
        print(approx)
        w,h,arr = transform(approx)
        pts2=np.float32([[0,0],[w,0],[0,h],[w,h]])
        pts1=np.float32(arr)
        M=cv2.getPerspectiveTransform(pts1,pts2)
        newImage=cv2.warpPerspective(self.image, M,(w,h))
        self.image = newImage
        return self

    def rotate(self, degre):
        heigth,width,_ = self.image.shape

        rotationMatrix = cv2.getRotationMatrix2D((width/2, heigth/2), degre,1)

        cos = np.abs(rotationMatrix[0, 0])
        sin = np.abs(rotationMatrix[0, 1])

        nW = int((heigth * sin) + (width * cos))
        nH = int((heigth * cos) + (width * sin))

        rotationMatrix[0, 2] += (nW / 2) - width/2
        rotationMatrix[1, 2] += (nH / 2) - heigth/2

        image = cv2.warpAffine(self.image,rotationMatrix,(heigth, width))
        self.image = image
        return self

    def write(self, name):
        cv2.imwrite(name, self.image)

        return self
