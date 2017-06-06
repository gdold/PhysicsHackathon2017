import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
from colorthief import ColorThief
import genetic_rgb as gen

def main():
    # background window
    bg = Image.open("desert.jpg")
    
    # size of square window to be overlaid and camouflaged
    fg_win = 60
    # where to place the foreground
    fg_anchor = (200, 200)
    
    # extract foreground pixels
    fg = bg.copy().crop((fg_anchor[0], fg_anchor[1], fg_anchor[0] + fg_win, fg_anchor[1] + fg_win))
    # convert to numpy array
    fg = np.asarray(fg)

    fg_red = fg[:,:,0]
    fg_green = fg[:,:,1]
    fg_blue = fg[:,:,2]

    # create target for dominant color 
    t_r = np.argmax(np.bincount(fg_red[:,0]))
    t_g = np.argmax(np.bincount(fg_green[:, 0]))
    t_b = np.argmax(np.bincount(fg_blue[:, 0]))
    target_rgb = (t_r, t_g, t_b)

    # target for variance
    t_v_r = np.var(fg_red)
    t_v_g = np.var(fg_green)
    t_v_b = np.var(fg_blue)
    target_var = (t_v_r, t_v_g, t_v_b)

    # target for distributions 
    std_rgb = (np.std(fg_red), np.std(fg_green), np.std(fg_blue))
    mean_rgb = (np.mean(fg_red), np.mean(fg_green), np.mean(fg_blue))
    target_min = (mean_rgb[0] - std_rgb[0], mean_rgb[1] - std_rgb[1], mean_rgb[2] - std_rgb[2])
    target_max = (mean_rgb[0] + std_rgb[0], mean_rgb[1] + std_rgb[1], mean_rgb[2] + std_rgb[2])
     
    # population size
    p_count = 100
    # chromosome length
    i_length = fg_win**2
    
    # genetic algorithm parameters
    retain = 0.2
    random_select = 0.1
    mutate = 0.01
    p_iter = 200
    i_min = 0
    i_max = 255
    
    p = gen.population(p_count, i_length, i_min, i_max)

    # overlay initial guess
    #fg_init_r = p_init[:,0].reshape(fg_win, fg_win)
    #fg_init_g = p_init[:,1].reshape(fg_win, fg_win)
    #fg_init_b = p_init[:,2].reshape(fg_win, fg_win)
    #fg_init = np.dstack((fg_init_r, fg_init_g, fg_init_b)).astype(np.uint8)
    
    for i in xrange(p_iter):
        p = gen.evolve(p, target_rgb, target_var, target_min, target_max)
       
    p = p[0]
    index_out = (np.argmax(np.bincount(p[:,0])), 
                 np.argmax(np.bincount(p[:,1])),
                 np.argmax(np.bincount(p[:,2])))

    # reconstruct foreground from generated image
    fg_camou_r = p[:,0].reshape(fg_win, fg_win)
    fg_camou_g = p[:,1].reshape(fg_win, fg_win)
    fg_camou_b = p[:,2].reshape(fg_win, fg_win)
    fg_camou_rgb = np.dstack((fg_camou_r, fg_camou_g, fg_camou_b)).astype(np.uint8)
    
    # overlay solution
    bg.paste(Image.fromarray(fg_camou_rgb, "RGB"), (fg_anchor[0], fg_anchor[1]))
    plt.imshow(bg)
    plt.show()

if __name__ == "__main__":
    main()
    
    


