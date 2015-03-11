# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 18:32:34 2015

@author: nick
"""

import numpy as np
import cv2
import time
from matplotlib import pyplot as plt
import pylab as pyl
from scipy.optimize import curve_fit

cap = cv2.VideoCapture(0) #Chose capture device may need to change to 1 if using laptop with a webcam

cap.set(3,1296)#Sets image to full size
cap.set(4,964)#Sets image to full size
cap.set(15,120)# Sets exmposure time should stay fixed changed att as needed
ret, frame = cap.read()# Reads in one frame to stop crashing issues

plt.axis([0, cap.get(3), 0, 255])#sets plots axis
plt.ion()#sets iteractive plot means constant update
plt.show()# shows plotting window

def gauss_function(x, a, x0, sigma,C):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+C



while(True):
    # Capture frame-by-frame
    plt.clf() #clears plots
    ret, img = cap.read()
    #Set threshold value to make binary image so centre can be found accurately
    ret,thresh = cv2.threshold(img,80,255,0)
    #Calcualtes image moments
    M = cv2.moments(thresh)

    if M['m00'] != 0.0: #stops division by zero error
               
        cx = int(M['m10']/M['m00'])#Calculates beam center x
        cy = int(M['m01']/M['m00'])#Calculates beam center y
        linex = img[cy,:] #1D array of pixel values through x centre
        liney = img[:,cx] #1D array of pixel values through y centre
        #Fitting x direction
        plt.subplot(211)
        x = pyl.arange(len(linex)) #Creates array of x points for fit
        p0x = [max(linex),cx,np.std(linex),5] #intial values x fit
        poptx, pcovx = curve_fit(gauss_function, x, linex,p0x) #fitting algorithm
        plt.plot(linex) #plots x line plot data
        plt.plot(gauss_function(x,*poptx),color='red') #plots fit to this
        waist_x = poptx[2]*2*3.75e-6 #x width in pixel times pixel size
        plt.title(str(waist_x))
        
        #Fitting y direction
        plt.subplot(212)
        y = pyl.arange(len(liney)) #Creates array of x points for fit
        p0y = [max(liney),cy,np.std(liney),5] #intial values x fit
        popty, pcovy = curve_fit(gauss_function,y,liney,p0y) #fitting algorithm
        plt.plot(liney) #plots y line plot data
        plt.plot(gauss_function(x,*popty),color='red') #plots fit to this
        waist_y = popty[2]*2*3.75e-6 #y width in pixel times pixel size
        plt.title(str(waist_y))
        
    
        cv2.line(img,(cx+int(poptx[2]),cy),(cx-int(poptx[2]),cy),255,1)
        cv2.line(img,(cx,cy+int(popty[2])),(cx,cy-int(popty[2])),255,1)
        cv2.ellipse(img,(cx,cy),(int(poptx[2]),int(popty[2])),0,0,360,255,1) 
        plt.draw()
    cv2.imshow('img',img)
    print waist_x, waist_y
    if cv2.waitKey(10) & 0xFF == ord('q'):
       break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()