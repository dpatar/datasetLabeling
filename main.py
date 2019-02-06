#!/usr/bin/env python3

import os
import tkinter as tk
import tkinter.messagebox as msgBox
from PIL import Image, ImageTk

# Window size
wid = 800
heig = 600
# Image/Canvas height
canvHeight = 400
# Shown imageID
imageNo = 0

def getImageList():
    imlist = []
    thisdir = os.getcwd()
    for file in os.listdir(thisdir):
        if ".jpg" in file:
            imlist.append(os.path.join(thisdir, file))
    return imlist

def createFolders(labels):
    for l in labels:
        try:
            os.mkdir(l)
        except Exception:
            pass   #folder exists
    try:
        os.mkdir('Other')
    except Exception:
        pass   #folder exists

def buttonCallBack(im,targetFolder,canvs,imOnCanvas):
    im = os.path.basename(im)
    os.rename(im,targetFolder+"/"+im)
    global imageNo
    imageNo += 1
    if imageNo >= len(imlist):
        msgBox.showinfo("Information","All images labeled")
        lockButtons()
    else:
        nextImage(canvs,imOnCanvas)

def getIm():
    #Fitting image to defined canvas
    image = Image.open(imlist[imageNo])
    imWid,imHeig = image.size
    # Resize Image
    image = image.resize((int(canvHeight*imWid/imHeig),canvHeight ), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    return photo

def nextImage(canvs,imOnCanvas):
    global currentPhoto
    currentPhoto = getIm()
    canvs.itemconfig(imOnCanvas, image=currentPhoto)

def lockButtons():
    for b in buttons:
        b.config(state = "disabled")

imlist = getImageList()

if __name__ == "__main__":

    if len(imlist) ==0:
        print("There are no image to label")
        exit()

    labels = ['AirConditioner','BlackPanel','Bookshelf','Box','Building','Car','Ceiling',
    	'CentralHeating','Chair','ComputerCase','Couch','Curtain','Cylinder','Door','Drawer',
    	'DressingFrame','Floor','Fuse Box','Hanger','Jaguar Robot','LightFixture','Monitor',
    	'Person','Phone','Plastic Bag','Poster','Road','SideWalk','SwitchBox','Tree','Umbrella',
    	'Wall','Wardrobe','WaterFountain','WhiteBoard','Window']

    createFolders(labels)

    #GUI
    root = tk.Tk()
    root.title("Labeling Script")

    nextRowPos = 0
    numOfColm = 6

    # Window Size
    root.geometry('{}x{}'.format(wid,heig))
    root.resizable(0, 0)
    # Window Position
    posRight = int(root.winfo_screenwidth()/2 - wid/2)
    posDown = int(root.winfo_screenheight()/3 - heig/2)
    root.geometry("+{}+{}".format(posRight, posDown))
    # Canvas for image
    canvs = tk.Canvas(root, back ='white',width = wid,height = canvHeight)
    canvs.grid(row=nextRowPos, columnspan=numOfColm)
    nextRowPos += 1

    # Initial Image
    global currentPhoto
    currentPhoto = getIm()
    imOnCanvas = canvs.create_image(wid/2, 0, image=currentPhoto, anchor='n')

    # Adding Buttons
    global buttons
    buttons =[None]*(len(labels)+1)
    rowPos = nextRowPos;
    i = 0;
    for l in labels:
        buttons[i] = tk.Button(root,text = l, command =lambda l=l: buttonCallBack(imlist[imageNo],l,canvs,imOnCanvas), width = 10)
        buttons[i].grid(row=rowPos + int(i/numOfColm),column = i % numOfColm)
        i += 1
    nextRowPos = rowPos + int(i/numOfColm) + 1

    buttons[i] = tk.Button(root,text = 'Other / Unclassified', command = lambda: buttonCallBack(imlist[imageNo],'Other',canvs,imOnCanvas), width = 40)
    buttons[i].grid(row=nextRowPos, column = 0, columnspan=6)

    root.mainloop()
