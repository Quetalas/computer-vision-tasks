import numpy as np
import cv2
import tkinter as tk
import PIL.Image, PIL.ImageTk

class Image:
    def __init__(self, image, name, size=None):
        self.originalImage = np.copy(image)
        self.name = name

        if size:
            self.originalImage = cv2.resize(self.originalImage, size)
        self.height, self.width, self.channels = self.originalImage.shape

        img = cv2.cvtColor(self.originalImage, cv2.COLOR_BGR2RGB)
        self.pillowImageCopy =PIL.Image.fromarray(img)
        self.photoImage = PIL.ImageTk.PhotoImage(self.pillowImageCopy)

        self.mouseArea = None


    def show(self):
        self.window = tk.Toplevel()

        self.canvas = tk.Canvas(self.window, height=self.height, width=self.width)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photoImage, anchor=tk.NW)
        self.canvas.bind('<Motion>', self.mouseMove)

        self.window.title(self.name)

    def mouseMove(self, event):
        x = event.x
        y = event.y
        dx = 100
        dy = 100
        area = (x-dx,y-dy,x+dx,y+dy)
        if self.mouseArea:
            self.canvas.coords(self.mouseArea, area)

        else:
            self.mouseArea = self.canvas.create_rectangle(area, width=1, outline='red')
        program.showImage(self.pillowImageCopy.crop(area), scalor=1)
        # if event == cv2.EVENT_MOUSEMOVE:
        #     self.copyImage = np.copy(self.originalImage)
        #     self.copyImage = cv2.rectangle(self.copyImage, (x,y), (x+10, y+10), color=(0,0,255))
        #     ProgramManager.activeWindowData = {''}


class ProgramManager:

    activeWindowData = {'Type': '', 'data': ''}

    def __init__(self):
        self.lastKey = "q"
        self.windowName = 'program'
        self.windowHeight = 400
        self.windowWidth = 250
        self.windowSize = '{0}x{1}'.format(self.windowHeight, self.windowWidth)
        self.window = tk.Tk()
        self.window.geometry(self.windowSize)
        self.window.title(self.windowName)

        self.canvas = tk.Canvas(self.window, height=self.windowHeight, width=self.windowWidth)
        self.canvas.pack()

    def start(self):
        self.window.mainloop()

    def updateWindowCanvasSize(self):
        self.windowSize = '{0}x{1}'.format(self.windowHeight, self.windowWidth)
        self.window.geometry(self.windowSize)
        self.canvas['height'] = self.windowHeight
        self.canvas['width'] = self.windowWidth

    def showImage(self, image, scalor=1):
        self.canvas.delete('all')
        self.pillowImageCopy = image
        self.pillowImageCopy = self.pillowImageCopy.resize((self.pillowImageCopy.size[0]*scalor,self.pillowImageCopy.size[1]*scalor))
        self.windowHeight, self.windowWidth = self.pillowImageCopy.size
        self.updateWindowCanvasSize()
        self.photoImage = PIL.ImageTk.PhotoImage(self.pillowImageCopy)
        self.canvas.create_image(0, 0, image=self.photoImage, anchor=tk.NW)


program = ProgramManager()

if __name__ == '__main__':


    image = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\1.jpg')
    image = Image(image, "image 1", size=(640, 480))
    image2 = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\2.jpg')
    image2 = Image(image2, "image 2", size=(640, 480))

    image.show()
    image2.show()

    program.start()

