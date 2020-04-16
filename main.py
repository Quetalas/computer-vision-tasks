import numpy as np
import cv2
import tkinter as tk
import PIL.Image, PIL.ImageTk
from matplotlib import pyplot as plt
class Image:
    def __init__(self, image, name, size=None):
        self.originalImage = np.copy(image)
        self.name = name

        if size:
            self.originalImage = cv2.resize(self.originalImage, size)
        self.height, self.width, self.channels = self.originalImage.shape

        self.originalRGB = cv2.cvtColor(self.originalImage, cv2.COLOR_BGR2RGB)
        self.pillowImageCopy =PIL.Image.fromarray(self.originalRGB)
        self.photoImage = PIL.ImageTk.PhotoImage(self.pillowImageCopy)

        self.mouseArea = None


    def show(self):
        self.window = tk.Toplevel()

        self.canvas = tk.Canvas(self.window, height=self.height, width=self.width)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photoImage, anchor=tk.NW)

        self.infoVar = tk.StringVar()
        self.infoLabel = tk.Label(self.window, text="", textvariable=self.infoVar)
        self.infoLabel.pack(side=tk.BOTTOM)
        self.canvas.bind('<Motion>', self.mouseMove)

        self.window.title(self.name)

    def mouseMove(self, event):
        x = event.x
        y = event.y
        dx = 50
        dy = 50
        area = [x-dx,y-dy,x+dx,y+dy]
        # Рисует прямоугольник
        if self.mouseArea:
            self.canvas.coords(self.mouseArea, area)

        else:
            self.mouseArea = self.canvas.create_rectangle(area, width=1, outline='red')
        # Дальнейшие действия с выделенной областью
        cropImage = self.cropImage(self.originalImage, area)
        cropImage = cv2.cvtColor(cropImage, cv2.COLOR_BGR2RGB)

        program.showImage(PIL.Image.fromarray(cropImage), scalor=1)
        self.infoVar.set(self.computeStatistics(cropImage, (x, y)))

    def cropImage(self, image, roi):
        if roi[0] < 0:
            roi[0] = 0
        if roi[1] < 0:
            roi[1] = 0
        if roi[2] > self.width:
            roi[2] = self.width
        if roi[3] > self.height:
            roi[3] = self.height
        return image[roi[1] : roi[3], roi[0] : roi[2]]

    def computeStatistics(self, image, pixel):
        "Expect RGB format"
        average = np.average(image)
        std = np.std(image)
        x, y = pixel
        pointAverage = np.average(self.originalRGB[y, x])
        return "x,y: ({}, {})={:.1f} average: {:.1f}    std: {:.1f}".format(x, y, pointAverage, average, std)


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


def task1():
    program = ProgramManager()
    image = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\1.jpg')
    image = Image(image, "image 1", size=(640, 480))
    image2 = cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\2.jpg')
    image2 = Image(image2, "image 2", size=(640, 480))

    image.show()
    image2.show()

    program.start()


def readImages():
    image1 = cv2.resize(cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\1.jpg'), (640, 480))
    image2 = cv2.resize(cv2.imread(r'C:\Users\Evgen\Documents\My\Projects\computer vision\images\2.jpg'), (640, 480))
    return [image1, image2]


def RGBToComplex(images_list, show=True):
    out = []
    i = 0
    for image in images_list:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        out.append(dft_shift)
        if show:
            magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
            plt.figure(i)
            plt.plot()
            plt.imshow(magnitude_spectrum, cmap='gray')
            plt.title('Magnitude of {} image'.format(i + 1)), plt.xticks([]), plt.yticks([])
            i = i + 1
    plt.show()
    return out

def ComplexToGrey(images_list):
    out = []
    for image in images_list:
        f_ishift = np.fft.ifftshift(image)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
        out.append(img_back)
    return out

def showImages(images_list):
    i = 0
    for image in images_list:
        plt.figure(i)
        plt.plot()
        plt.imshow(image, cmap='gray')
        plt.title('{} image'.format(i + 1)), plt.xticks([]), plt.yticks([])
        i = i + 1
    plt.show()

def task2():
    images_list = readImages()
    complex_images = RGBToComplex(images_list)
    pass
    new_images = ComplexToGrey(complex_images)
    showImages(new_images)



if __name__ == '__main__':
    task2()