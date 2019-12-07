import numpy as np
import cv2
import matplotlib.pyplot as plt

class Clicker:
    clickedCoords = []
    @staticmethod
    def leftClick(event, x, y, flags, img):
        if event == cv2.EVENT_LBUTTONDOWN:
            try:
                id = Clicker.clickedCoords.index((x, y))
                pass
            except ValueError:
                Clicker.drawRectangle(img, (x, y))
                Clicker.clickedCoords.append((x, y))

    @staticmethod
    def drawRectangle(img, xy, dx=5, dy = 5):
        global image
        image = cv2.rectangle(img, (xy[0]-dx, xy[1]-dy), (xy[0]+dx, xy[1]+dy), (0, 0, 255))


image = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\1.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image', Clicker.leftClick, image)
while True:
    cv2.imshow('image', image)
    key = cv2.waitKey(1)
    if key == ord('c'):
        break

