import numpy as np
import cv2
import tkinter as tk

class Image:
    def __init__(self, image, name):
        self.originalImage = image
        self.copyImage = np.copy(image)
        self.name = name
        self.callbacksSet = False

    def Show(self):
        cv2.imshow(self.name, self.copyImage)
        if not self.callbacksSet:

            cv2.setMouseCallback(self.name, self.MouseCallback, self.copyImage)
            self.callbacksSet = True



    def MouseCallback(self, event, x, y, flags, img):
        print(event)
        if event == cv2.EVENT_MOUSEMOVE:
            self.copyImage = np.copy(self.originalImage)
            self.copyImage = cv2.rectangle(self.copyImage, (x,y), (x+10, y+10), color=(0,0,255))
            ProgramManager.activeWindowData = {''}



class ProgramManager:
    keys = dict.fromkeys(['h', 'q'], False)
    activeWindowData = {'Type': '', 'data': ''}

    def __init__(self):
        self.lastKey = "q"
        self.windowName = 'program'
        cv2.namedWindow(self.windowName)

    def start(self):
        self.doKeyboardCallbacks()

    def doKeyboardCallbacks(self):
        ProgramManager.keys[self.lastKey] = False
        key = cv2.waitKey(1)
        key = int(str(key), 0)
        try:
            key = chr(key)
            self.lastKey = key
            ProgramManager.keys[key] = True
        except:
            pass




if __name__ == '__main__':

    image = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\1.jpg')
    image = Image(image, "image 1")
    image2 = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\2.jpg')
    image2 = Image(image2, "image 2")

    program = ProgramManager()
    while True:
        image.Show()
        image2.Show()
        program.start()
        if ProgramManager.keys['q']:
            break

