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
    
    b_height=til.size[0]   #the height and width of the background
    b_width=til.size[1]
    background_pixels=til.load()
    #print(background_pixels)


    background_pixels=np.ones((til.size[0],til.size[1],3))
    red=np.ones([b_height,b_width])        #red, green and blue are the three vectors with the rgb values for
    green=np.ones([b_height,b_width])      #the background
    blue=np.ones([b_height,b_width])
    
    for i in range(b_height):
        for j in range(b_width):
                r,g,b=til.getpixel((i, j))
                background_pixels[i,j,0]=r
                red[i,j]=r
                background_pixels[i,j,1]=g
                green[i,j]=g
                background_pixels[i,j,2]=b
                blue[i,j]=b
    
    size1=background_pixels.shape[0]   #image length in pixels
    size2=background_pixels.shape[1]   #image width in pixels
    size3=background_pixels.shape[2]   #this should be 3 (r,g,b)
    
    background=background_pixels.reshape(1,size1*size2*size3)
    background=background[0]
    red.reshape(1,size1*size2)
    red=np.reshape(red,size1*size2)
    green=np.reshape(green,size1*size2)
    blue=np.reshape(blue,size1*size2)

    #!!!!!! this is the vector that contains the data about the background image

    #this creates a randomly coloured square

    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            colour1=np.random.randint(0,256)
            colour2=np.random.randint(0,256)
            colour3=np.random.randint(0,256)
            pixels[i,j] = (colour1,colour2,colour3) # set the colour accordingly

    #pixels = im.load()
    foreground_pixels=np.ones((im.size[0],im.size[1],3))
    
    im_height=im.size[0]
    im_width=im.size[1]
    red_target=np.ones([im_height,im_width])        #red, green and blue are the three vectors with the rgb values for
    green_target=np.ones([im_height,im_width])      #the foreground
    blue_target=np.ones([im_height,im_width])
    
    
    for i in range(im_height):
        for j in range(im_width):
                r,g,b=im.getpixel((i, j))
                foreground_pixels[i,j,0]=r
                red_target[i,j]=r
                foreground_pixels[i,j,1]=g
                green_target[i,j]=g
                foreground_pixels[i,j,2]=b
                blue_target[i,j]=b
    print(green_target)


    size1=foreground_pixels.shape[0]   #image heigth in pixels
    size2=foreground_pixels.shape[1]   #image width in pixels
    size3=foreground_pixels.shape[2]   #this should be 3 (r,g,b)

    foreground=foreground_pixels.reshape(1,size1*size2*size3)
    foreground=foreground[0]
    red_target=np.reshape(red_target,size1*size2)
    green_target=np.reshape(green_target,size1*size2)
    blue_target=np.reshape(blue_target,size1*size2)


    pos1=int(til.size[0]/4)
    pos2=int(til.size[1]/4)

    
    red_output=red_target
    green_output=green_target
    blue_output=blue_target
    

    
    #we need to generate the new r g b vectors here from the genetic algorithm
    #basically the input should be red, green and blue which contain the background image
    #and we can start with red_target,blue_target and green_target for the image

    
    
    
    
    
    
    
    red_output=np.reshape(red_output,(size1,size2))
    blue_output=np.reshape(blue_output,(size1,size2))
    green_output=np.reshape(green_output,(size1,size2))
    print (green_output.shape)
    
    
    
    for i in range(im_height):
        for j in range(im_width):
            colour1=red_output[i,j]
            colour2=green_output[i,j]
            colour3=blue_output[i,j]
            pixels[i,j] = (int(colour1),int(colour2),int(colour3))
            #print(pixels[i,j])
    print np.shape(im)
    print type(im)
    til.paste(im,(pos1,pos2))
    plt.imshow(til)

if __name__ == "__main__":
    main()
    
    


