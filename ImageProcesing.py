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

    def edgeDetect(self):
        self.gausianBlur((9,9))
        self.newImage = self.image.copy()
        edge = cv2.Canny(self.greyImage, 100,100)
        _,contours,_ = cv2.findContours(edge.copy(),1,1)
        self.contours = contours
        return self

    def cropImage(self):
        maxArea = 0
        contour = 0

        for i in self.contours:
            area = cv2.contourArea(i)
            if area > maxArea:
                maxArea = area
                contour = i
        peri=cv2.arcLength(contour,True)
        approx=cv2.approxPolyDP(contour,0.02*peri,True)
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
