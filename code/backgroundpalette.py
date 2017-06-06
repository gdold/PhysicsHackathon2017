#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:45:43 2017

@author: gavin
"""

import numpy as np
import cv2
from PIL import Image
from colorthief import ColorThief

#pilimg = Image.open('dog.jpg')
#rect = (50,60,450,390)

def removeForeground(image,rect,transparent=True):
    '''
    Return a PIL RGBA image object with the foreground object inside the
    rectangle 'rect' removed from the PIL image object 'image'
    '''
    img=np.array(pilimg)
    mask = np.zeros(img.shape[:2],np.uint8)
    
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    
    
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask==2)|(mask==0),1,0).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    
    outputimg = Image.fromarray(img)
    
    if transparent:
        outputimg = outputimg.convert('RGBA')
        datas = outputimg.getdata()
        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)

    outputimg.putdata(newData)
    
    return outputimg

def getBackgroundPalette(image,rect,color_count=5,transparent=True):
    '''
    Return the background palette from the PIL image 'image', with the
    foreground object specified by 'rect' removed
    '''
    img = ColorThief(removeForeground(image,rect,transparent))
    palette = img.get_palette(color_count=5)
    return palette