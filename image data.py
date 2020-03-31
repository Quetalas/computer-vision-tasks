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
        self.photoImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img))
        self.copyImage = np.copy(image)

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

        if self.mouseArea:
            self.canvas.delete(self.mouseArea)
        self.mouseArea = self.canvas.create_rectangle(x-5, y-5, x+5, y+5, width=1, outline='red')
        # if event == cv2.EVENT_MOUSEMOVE:
        #     self.copyImage = np.copy(self.originalImage)
        #     self.copyImage = cv2.rectangle(self.copyImage, (x,y), (x+10, y+10), color=(0,0,255))
        #     ProgramManager.activeWindowData = {''}


class ProgramManager:

    activeWindowData = {'Type': '', 'data': ''}

    def __init__(self):
        self.lastKey = "q"
        self.windowName = 'program'
        self.windowSize = '400x250'
        self.window = tk.Tk()
        self.window.geometry(self.windowSize)
        self.window.title(self.windowName)

    def start(self):
        self.window.mainloop()


if __name__ == '__main__':
    program = ProgramManager()

    image = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\1.jpg')
    image = Image(image, "image 1", size=(640, 480))
    image2 = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\2.jpg')
    image2 = Image(image2, "image 2", size=(640, 480))

    image.show()
    image2.show()
    program.start()

