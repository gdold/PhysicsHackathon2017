#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def main():
    til = Image.open("forest.jpeg")
    im = Image.open("frog.jpeg") 
    num_pixels1=40;   #this sets how many pixels should the new image have
    num_pixels2=40;
    im = im.resize((num_pixels1,num_pixels2), Image.BILINEAR)

    background_pixels=til.load()
    print(background_pixels)


    background_pixels=np.ones((til.size[0],til.size[1],3))
    for i in range(til.size[0]):
        for j in range(til.size[1]):
                r,g,b=til.getpixel((i, j))
                background_pixels[i,j,0]=r
                background_pixels[i,j,1]=g
                background_pixels[i,j,2]=b

    size1=background_pixels.shape[0]   #image length in pixels
    size2=background_pixels.shape[1]   #image width in pixels
    size3=background_pixels.shape[2]   #this should be 3 (r,g,b)

    background=background_pixels.reshape(1,size1*size2*size3)
    background=background[0]
    print type(background)
    print np.size(background)
    #!!!!!! this is the vector that contains the data about the background image

    #this creates a randomly coloured square

    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            colour1=np.random.randint(0,256)
            colour2=np.random.randint(0,256)
            colour3=np.random.randint(0,256)
            pixels[i,j] = (colour1,colour2,colour3) # set the colour accordingly

    pixels = im.load()
    foreground_pixels=np.ones((im.size[0],im.size[1],3))
    for i in range(im.size[0]):
        for j in range(im.size[1]):
                r,g,b=til.getpixel((i, j))
                foreground_pixels[i,j,0]=r
                foreground_pixels[i,j,1]=g
                foreground_pixels[i,j,2]=b

    size2=foreground_pixels.shape[1]   #image width in pixels
    size1=foreground_pixels.shape[0]   #image length in pixels
    size3=foreground_pixels.shape[2]   #this should be 3 (r,g,b)

    foreground=foreground_pixels.reshape(1,size1*size2*size3)
    foreground=foreground[0]
           


    pos1=int(til.size[0]/4)
    pos2=int(til.size[1]/4)
    til.paste(im,(pos1,pos2))
    plt.imshow(til)

if __name__ == "__main__":
    main()


