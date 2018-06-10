import pydicom
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from random import randint
from PIL import ImageTk, Image
from tkinter import filedialog
import scipy.misc
import scipy.signal
import math
import cv2

rescale_slope=1 
rescale_intercept=-32
level=200
window=800


class Application(Frame):
        
    def __init__(self, master):
        super().__init__(master)
        self.radiobuttonValue = IntVar()
        self.radiobuttonValue.set(1)
        self.toolsThickness = 2
        self.rgb = "#%02x%02x%02x" % (0, 0, 0)
        
         
        self.pack()
        self.createWidgets()
         
        master.bind('a', self.thicknessPlus)
        master.bind('s', self.thicknessMinus)
        
         
    def createWidgets(self):
        rowIndex = 0
        tk_rgb = "#%02x%02x%02x" % (128, 192, 200)        

        
        # =================== Left Frame Setup =====================
        self.leftFrame = Frame(self, bg = tk_rgb)
        self.leftFrame.pack(side = LEFT, fill = Y)
        
        #-----------------------------------------------
        
        self.entryFrame = Frame(self.leftFrame)
        self.entryFrame.pack(fill=X, side = TOP, expand=True)
        
        self.labelFrame = Frame(self.entryFrame)
        self.labelFrame.pack(fill=Y, side = TOP, expand =True)
        
        self.label = Label(self.labelFrame, text = "RGB color: ")
        self.label.pack(fill=X, side = LEFT)
        
        self.colorLabel = Label(self.labelFrame, bg = self.rgb, width=2)
        self.colorLabel.pack(fill=X, side =RIGHT)
        
        self.rScale = Scale(self.entryFrame, from_ = 0, to = 255,
                            orient = HORIZONTAL,
                            command = self.setColor)
        self.rScale.pack(fill=X, side = TOP, expand=True)
        
        self.gScale = Scale(self.entryFrame, from_ = 0, to = 255,
                            orient = HORIZONTAL,
                            command = self.setColor)
        self.gScale.pack(fill=X, side = TOP, expand=True)
        
        self.bScale = Scale(self.entryFrame, from_ = 0, to = 255,
                            orient = HORIZONTAL,
                            command = self.setColor)
        self.bScale.pack(fill=X, side = TOP, expand=True)
        
        #----------------------------------------------
        
        self.thicknessFrame = Frame(self.leftFrame)
        self.thicknessFrame.pack(fill=X, side = TOP, expand=True)
        
        self.labelThickness = Label(self.thicknessFrame,
                            text = "drawing tools' thickness:")
        self.labelThickness.pack(fill = X, side = TOP, expand = True)
        
        self.myScale = Scale(self.thicknessFrame, from_ = 1, to = 25,
                            orient = HORIZONTAL,
                            command = self.setThickness)
        self.myScale.set(2)
        self.toolsThickness = 2
        self.myScale.pack(fill=X, side = TOP, expand=True)
        
        self.toolsFrame = Frame(self.leftFrame)
        self.toolsFrame.pack(fill=X, side=TOP, expand=True)
        
        self.labelTools = Label(self.toolsFrame,
                                text = "chose a drawing tool:")
        self.labelTools.pack(fill=X, side = TOP, expand = True)
        
        # Radio Buttons setup
        
        Radiobutton(self.toolsFrame,
                    text = "Line",
                    variable = self.radiobuttonValue,
                    value = 2).pack(fill=X,side=TOP,expand=True)
 
        Radiobutton(self.toolsFrame,
                    text = "Rectangle",
                    variable = self.radiobuttonValue,
                    value = 3).pack()
        
        Radiobutton(self.toolsFrame,
                    text = "Oval",
                    variable = self.radiobuttonValue,
                    value = 4).pack()
        
        # Function Buttons setup
        
            # Import Image
                # Button function setup
        self.importButton = Button(self.leftFrame, text = "Import",command = self.importImage)
                # Put the button on Canvas
        self.importButton.pack(fill = X, expand=True)
            
            # Clear
                # Button function setup
        self.buttonDeleteAll = Button(self.leftFrame, text = "Clear",command = self.delteAll)
                # Put the button on Canvas
        self.buttonDeleteAll.pack(fill=X, expand=True)
        
            # Gaussian Blur Filter
                # Button function setup
        self.buttonGaussianBlur = Button(self.leftFrame, text = "Gaussian Blur",command = self.Gaussian_Blur)
                # Put the button on Canvas
        self.buttonGaussianBlur.pack(fill=X, expand=True)
        
            # Enhancement Filter - TODO
                # Button function setup
        self.buttonEnhancement = Button(self.leftFrame, text = "Enhancement",command = self.Enhancement)
                # Put the button on Canvas
        self.buttonEnhancement.pack(fill=X, expand=True)
      
            # Edge Detection Filter - TODO
                # Button function setup
        self.buttonEdge_Detection = Button(self.leftFrame, text = "Edge_Detection",command = self.Edge_Detection)
                # Put the button on Canvas
        self.buttonEdge_Detection.pack(fill=X, expand=True)
      
            # Thresholding
                # Button function setup
        self.buttonThresholding = Button(self.leftFrame, text = "Thresholding",command = self.Thresholding)
                # Put the button on Canvas
        self.buttonThresholding.pack(fill=X, expand=True)
        
#----------------------------------------------------------------------
        # =================== Canvas Setup =====================
        self.myCanvas = Canvas(self, width = 800,height = 500, relief=RAISED, borderwidth=5)
        self.myCanvas.pack(side = RIGHT)
        self.myCanvas.bind("<B1-Motion>", self.onPressed)
        self.myCanvas.bind("<Button-1>", self.onClicked)
        self.myCanvas.bind("<ButtonRelease-1>", self.onReleased)
         
#----------------------------------------------------------------------

#==================== Dicom to Canvas Tools (for show & importImage) ===================

    def get_LUT_value(self, data, window, level):

        return np.piecewise(data, 
            [data <= (level - 0.5 - (window-1)/2),
                data > (level - 0.5 + (window-1)/2)],
                [0, 255, lambda data: ((data - (level - 0.5))/(window-1) + 0.5)*(255-0)])

    # rescale the dicom value to jpeg value
    def translate(self,value,rescale_slope,rescale_intercept):
        return (value*rescale_slope)+rescale_intercept 

    # convert the value of each pixel in a dicom image
    def convertDCM(self, pixelarray):
        img_array = []
        
        for eachRow in pixelarray:
            for eachPix in eachRow:
                img_array.append(self.translate(eachPix,rescale_slope,rescale_intercept))
        img_array = np.array(img_array)
        img_array = img_array.reshape(self.data.Rows,self.data.Columns)  
        return img_array
    
    def fitCanvas(self, img):
        canvas_width = self.myCanvas.winfo_width()
        canvas_height = self.myCanvas.winfo_height()
        
        img_width, img_height = img.size
        
        # resize
        if(img_width >= canvas_width or img_height >= canvas_height):
            
            if(img_height/canvas_height >= img_width/canvas_width):
                resize_width = img_width*((canvas_height)/img_height)
                resize_height = canvas_height
            else:
                resize_width = canvas_width
                resize_height = img_height*((canvas_width)/img_width)    
            resize_width = int(round(resize_width))
            resize_height = int(round(resize_height))
            print(resize_width)
            print(resize_height)
            img = img.resize((resize_width, resize_height), Image.ANTIALIAS)
    
        return img

    def convert2image(self, pixelarray):
        # convert DCM to byte array
        img = self.convertDCM(pixelarray)
        
        # Use window level and width information from the image header to display in the proper range
        img = self.get_LUT_value(img,window,level)
        
        # scaling, taking an absolute value, conversion to an unsigned 8-bit type
        img = cv2.convertScaleAbs(img)
        
        # convert byte array to Image object
        img_new = Image.frombytes('L', (img.shape[1],img.shape[0]), img.astype('b').tostring())
        
        # resize image object to fit canvas
        img_new = self.fitCanvas(img_new)
        
        return img_new
        
        
    def importDCM(self): 
        # path of the DCM
        path = filedialog.askopenfilename()
        
        # for filter use
        self.data = pydicom.dcmread(path)
        
        img = self.convert2image(self.data.pixel_array)
        
        return img
        
# =====================================================================================

    # Button Functions
    
    def setThickness(self, event):      
        self.toolsThickness = self.myScale.get()
         
    def setColor(self, event):
        try:
            val1 = int(self.rScale.get())
            val2 = int(self.gScale.get())
            val3 = int(self.bScale.get())
            if 0 <=(val1 and val2 and val3) <= 255:              
                self.rgb = "#%02x%02x%02x" % (val1, val2, val3)
                self.colorLabel.configure(bg=self.rgb)
            
         
        except ValueError:
            print("That's not an int!")
        # set focus to something else, not to mess with pressing keys: a,s
        self.focus()
        
    def onClicked(self, event):
        self.isReleased = False
        self.isClicked = True
        self.isDraw = False
        self.startX = event.x
        self.startY = event.y
        self.tmpX = event.x
        self.tmpY = event.y
            
    def onReleased(self, event):
        self.isClicked = False
        self.isReleased = True
        self.endX = event.x
        self.endY = event.y
        
        # line
        if self.radiobuttonValue.get() == 2:
            self.step = self.myCanvas.create_line(self.startX, self.startY,
                                      self.endX, self.endY,
                                      width = self.toolsThickness,
                                      fill = self.rgb)
            self.myCanvas.delete(self.step-1)
            
        # rectangle - TODO        
        elif self.radiobuttonValue.get() == 3:
            self.step = self.myCanvas.create_rectangle(self.startX, self.startY,
                                      self.endX, self.endY,
                                      width = self.toolsThickness,
                                      outline = self.rgb)
            self.myCanvas.delete(self.step-1)
        
            
        # oval - TODO
        elif self.radiobuttonValue.get() == 4:
            self.step = self.myCanvas.create_oval(self.startX, self.startY,
                                      self.endX, self.endY,
                                      width = self.toolsThickness,
                                      outline = self.rgb)
            self.myCanvas.delete(self.step-1)

             
    def onPressed(self, event):
        # line
        if self.radiobuttonValue.get() == 2:
            if self.isClicked:
                index = self.myCanvas.create_line(self.startX, self.startY,
                                      event.x, event.y,
                                      width = self.toolsThickness,
                                      fill = self.rgb)
                self.myCanvas.update()
                if((self.tmpX != event.x or self.tmpY != event.y) and self.isDraw == True):
                    self.myCanvas.delete(index-1)
                    self.preIndex = index
                    self.tmpX = event.x
                    self.tmpY = event.y
                self.isDraw = True 
                
        # rectangle - TODO        
        elif self.radiobuttonValue.get() == 3:
            if self.isClicked:
                index = self.myCanvas.create_rectangle(self.startX, self.startY,
                                      event.x, event.y,
                                      width = self.toolsThickness,
                                      outline = self.rgb)
                self.myCanvas.update()
                if((self.tmpX != event.x or self.tmpY != event.y) and self.isDraw == True):
                    self.myCanvas.delete(index-1)
                    self.preIndex = index
                    self.tmpX = event.x
                    self.tmpY = event.y
                self.isDraw = True 

            
        # oval - TODO
        elif self.radiobuttonValue.get() == 4:
            if self.isClicked:
                index = self.myCanvas.create_oval(self.startX, self.startY,
                                      event.x, event.y,
                                      width = self.toolsThickness,
                                      outline = self.rgb)
                self.myCanvas.update()
                if((self.tmpX != event.x or self.tmpY != event.y) and self.isDraw == True):
                    self.myCanvas.delete(index-1)
                    self.preIndex = index
                    self.tmpX = event.x
                    self.tmpY = event.y
                self.isDraw = True 

                      
    def importImage(self):
        img= self.importDCM()
        
        photo = ImageTk.PhotoImage(master=self.myCanvas, image=img)
        self.img = photo
        
        self.step = self.myCanvas.create_image(0,0,image=photo, anchor=NW)
        
    def delteAll(self):
        self.myCanvas.delete("all")
         
    def thicknessPlus(self, event):
        if self.toolsThickness < 25:
            self.toolsThickness += 1
            self.myScale.set(self.toolsThickness)
 
    def thicknessMinus(self, event):
        if 1 < self.toolsThickness:
            self.toolsThickness -= 1
            self.myScale.set(self.toolsThickness)
    
    
#=========================== Filters Part Start ===================================
    # Show the filtering result on Canvas
    def show(self, out_array):
        # show byte array on canvas
        # convert byte array to Image object
        img = self.convert2image(out_array)
        
        photo = ImageTk.PhotoImage(master=self.myCanvas, image=img)
        self.img = photo
        self.step = self.myCanvas.create_image(0,0,image=photo, anchor=NW)
        
    # Enhancement filter tools - gaussian & clip
    def gaussian(self, sig):
        k = int(math.ceil(3 * sig))
        fil = np.empty((2 * k + 1, 2 * k + 1))
        for i in range(fil.shape[0]):
            for j in range(fil.shape[1]):
                fil[i][j] = (1 / (2 * math.pi * pow(sig, 2))) * math.exp(
                    -(pow(i - k, 2) + pow(j - k, 2)) / (2 * pow(sig, 2)))
        return fil
    
    def clip(self,input):
        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                if (input[i][j] < 0):
                    input[i][j] = 0
                if (input[i][j] > 255):
                    input[i][j] = 255
        return input
    
    # Edge detection filter tools - norm & threshold
    def norm(self, in_x, in_y):
        out_imarr = np.zeros(in_x.shape,dtype=float)
        for i in range(in_x.shape[0]):
            for j in range(in_x.shape[1]):
                out_imarr[i][j] = math.sqrt(in_x[i][j]**2 + in_y[i][j]**2)+0.000001
        return out_imarr
    
    def threshold(self, input, value):
        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                if(input[i][j]>value):
                    input[i][j]=255
                else:
                    input[i][j]=0
        
        return input
    
    # Common Filter tools - 2D convolution
    def conv2(self, input, filter):
        output = np.array(input, copy=True, dtype=int)
        k = filter.shape[0]//2
    
        for i in range(k,input.shape[0]-k):
            for j in range(k,input.shape[1]-k):
                sum = 0
                for x in range(i - k, i + k+1):
                    for y in range(j - k, j + k+1):
                        sum += input[x][y] * filter[x - i + k][y - j + k]  # 0~2K
                output[i][j] = int(sum)
        return output

    # Gaussian Blur - Main
    def Gaussian_Blur(self):
        sig = 1
        in_imarr = self.data.pixel_array
        in_imarr = np.array(in_imarr, copy=True,dtype=float)
    
        k = int(3 * sig)
        filter = np.empty((2 * k + 1, 2 * k + 1))
        for i in range(len(filter)):
            for j in range(len(filter)):
                filter[i][j] = (1 / (2 * math.pi * pow(sig, 2))) * math.exp(
                    -(pow(i - k, 2) + pow(j - k, 2)) / (2 * pow(sig, 2)))
    
        out_imarr = self.conv2(in_imarr, filter)
        self.show(out_imarr)
        
    # Thresholding - Main
    def Thresholding(self):
        pixel = self.data.pixel_array
        in_imarr = np.array(pixel, copy=True)
        maximum = 0
        minimum = 99999
        for _ in pixel:
            for p in _:
                if p > maximum:
                    maximum = p
                if p < minimum:
                    minimum = p
                
        # Calculate the threshold
        threshold = (maximum + minimum) / 2
    
        # Do transformation
        for (i, _) in enumerate(in_imarr):
            for (j, p) in enumerate(_):
                if p>=threshold:
                    in_imarr[i][j] = maximum
                else:
                    in_imarr[i][j] = minimum
                    
        out_imarr = np.array(in_imarr, copy=True)
        self.show(out_imarr)
        
    # Edge Detection - Main (TODO)
    def Edge_Detection(self):
        in_imarr = self.data.pixel_array
        in_imarr = np.array(in_imarr, copy=True, dtype=float)

        # Modify
        g_max = in_imarr.max();
        g_min = in_imarr.min();
        g_th = (g_max + g_min) / 2;
        in_imarr[in_imarr > g_th] = g_max;
        in_imarr[in_imarr <= g_th] = g_min; 
        gray = in_imarr
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)

        sobelx = np.uint8(np.absolute(sobelx))
        sobely = np.uint8(np.absolute(sobely))
        out_imarr = cv2.bitwise_or(sobelx,sobely)
        #

        self.show(out_imarr)
    
    # Enhancement - Main (TODO)
    def Enhancement(self):
        in_imarr = self.data.pixel_array
        in_imarr = np.array(in_imarr, copy=True, dtype=float)

        # Modify
        g_max = in_imarr.max();
        g_min = in_imarr.min();
        g_th = (g_max + g_min) / 2;
        in_imarr[in_imarr > g_th] *= 1.5;
        in_imarr[in_imarr <= g_th] *= 0.5;
        out_imarr = in_imarr 
        #
        
        self.show(out_imarr)
 
#=========================== Filters Part End ===================================
    
    
root = Tk()
root.title("Final Project")
app = Application(root)
root.mainloop() 
