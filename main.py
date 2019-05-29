#!/usr/bin/env python3

import os
import tkinter as tk
import tkinter.messagebox as msgBox
from PIL import Image, ImageTk


class simpleGui:
    # Window size
    wid = 800
    heig = 600
    # Image/Canvas height
    canvHeight = 400
    # Shown imageID
    imageNo = 0
    labels = ['AirConditioner', 'BlackPanel', 'Bookshelf', 'Box', 'Building',
              'Car', 'Ceiling', 'CentralHeating', 'Chair', 'ComputerCase',
              'Couch', 'Curtain', 'Cylinder', 'Door', 'Drawer',
              'DressingFrame', 'Floor', 'Fuse Box', 'Hanger', 'Jaguar Robot',
              'LightFixture', 'Monitor', 'Person', 'Phone', 'Plastic Bag',
              'Poster', 'Road', 'SideWalk', 'SwitchBox', 'Tree', 'Umbrella',
              'Wall', 'Wardrobe', 'WaterFountain', 'WhiteBoard', 'Window']

    def __init__(self, tk_root, imToLabel):
        self.root = tk_root
        self.imlist = imToLabel
        # Create a folder for each label
        createFolders(self.labels)
        # Title
        self.root.title("Labeling Script")
        # Window Size
        self.root.geometry('{}x{}'.format(self.wid, self.heig))
        self.root.resizable(0, 0)
        # Window Position
        posRight = int(self.root.winfo_screenwidth()/2 - self.wid/2)
        posDown = int(self.root.winfo_screenheight()/3 - self.heig/2)
        self.root.geometry("+{}+{}".format(posRight, posDown))

        # GRID LAYOUT

        nextRowPos = 0
        numOfColm = 6

        # Canvas for image
        self.canvs = tk.Canvas(self.root, back='white', width=self.wid,
                               height=self.canvHeight)
        self.canvs.grid(row=nextRowPos, columnspan=numOfColm)
        nextRowPos += 1

        # Initial Image
        self.currentPhoto = self.getIm()
        self.imOnCanvas = self.canvs.create_image(self.wid/2, 0,
                                                  image=self.currentPhoto,
                                                  anchor='n')

        # Adding Buttons
        self.buttons = [None]*(len(self.labels)+1)
        i = 0
        for l in self.labels:
            self.buttons[i] = tk.Button(self.root, text=l, command=lambda
                                        l=l: self.buttonCallBack(l), width=10)
            self.buttons[i].grid(row=nextRowPos + int(i/numOfColm),
                                 column=i % numOfColm)
            i += 1
        nextRowPos = nextRowPos + int(i/numOfColm) + 1
        self.buttons[i] = tk.Button(self.root, text='Other / Unclassified',
                                    command=lambda:
                                    self.buttonCallBack('Other'), width=40)
        self.buttons[i].grid(row=nextRowPos, column=0, columnspan=6)

    def buttonCallBack(self, targetFolder):
        im = os.path.basename(self.imlist[self.imageNo])
        os.rename(im, targetFolder+"/"+im)
        self.imageNo += 1
        if self.imageNo >= len(self.imlist):
            msgBox.showinfo("Information", "All images labeled")
            self.lockButtons()
        else:
            self.nextImage()

    def nextImage(self):
        self.currentPhoto = self.getIm()
        self.canvs.itemconfig(self.imOnCanvas, image=self.currentPhoto)

    def getIm(self):
        # Fitting image to defined canvas
        image = Image.open(self.imlist[self.imageNo])
        imWid, imHeig = image.size
        # Resize Image
        image = image.resize((int(self.canvHeight*imWid/imHeig),
                              self.canvHeight), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        return photo

    def lockButtons(self):
        for b in self.buttons:
            b.config(state="disabled")


def getImageList():
    # Reading images in same folder exiting if there is none.
    imlist = []
    thisdir = os.getcwd()
    for file in os.listdir(thisdir):
        if ".jpg" in file:
            imlist.append(os.path.join(thisdir, file))
    if len(imlist) == 0:
        print("There are no image to label")
        exit()
    return imlist


def createFolders(labels):
    for l in labels:
        try:
            os.mkdir(l)
        except Exception:
            pass   # folder exists
    try:
        os.mkdir('Other')
    except Exception:
        pass   # folder exists

if __name__ == "__main__":
    # Is there any image to label ?
    imList = getImageList()
    # GUI
    root = tk.Tk()
    gui = simpleGui(root, imList)
    root.mainloop()
