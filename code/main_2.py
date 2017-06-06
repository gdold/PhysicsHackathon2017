import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
from colorthief import ColorThief
import genetic_rgb as gen

def main():
    # background window
    bg = Image.open("jungle.jpeg")
    
    # size of square window to be overlaid and camouflaged
    fg_win = 200
    # where to place the foreground
    fg_anchor = (100, 100)
    
    # extract foreground pixels
    fg = bg.copy().crop((fg_anchor[0], fg_anchor[1], fg_anchor[0] + fg_win, fg_anchor[1] + fg_win))
    # convert to numpy array
    fg = np.asarray(fg)

    fg_red = fg[:,:,0]
    fg_green = fg[:,:,1]
    fg_blue = fg[:,:,2]

    # create target for color 
    t_r = np.argmax(np.bincount(fg_red[:,0]))
    t_g = np.argmax(np.bincount(fg_green[:, 0]))
    t_b = np.argmax(np.bincount(fg_blue[:, 0]))
    target_rgb = (t_r, t_g, t_b)
    
    # population size
    p_count = 200
    # chromosome length
    i_length = fg_win**2
    i_min = 0
    i_max = 255
    p = gen.population(p_count, i_length, i_min, i_max)
    
    fitness_history = [gen.grade(p, target_rgb),]
    
    # genetic algorithm parameters
    retain = 0.2
    random_select = 0.1
    mutate = 0.008
    p_iter = 200 # 500

    for i in xrange(p_iter):
        p = gen.evolve(p, target_rgb)
        fitness_history.append(gen.grade(p, target_rgb))
        
    p = p[0]
    index_out = (np.argmax(np.bincount(p[:,0])), 
                 np.argmax(np.bincount(p[:,1])),
                 np.argmax(np.bincount(p[:,2])))
    print target_rgb
    print index_out

    # reconstruct foreground from generated image
    fg_camou_r = p[:,0].reshape(fg_win, fg_win)
    fg_camou_g = p[:,1].reshape(fg_win, fg_win)
    fg_camou_b = p[:,2].reshape(fg_win, fg_win)
    fg_camou_rgb = np.dstack((fg_camou_r, fg_camou_g, fg_camou_b)).astype(np.uint8)
    
    # overlay
    bg.paste(Image.fromarray(fg_camou_rgb, "RGB"), (fg_anchor[0], fg_anchor[1]))
    plt.imshow(bg)

    plt.show()

if __name__ == "__main__":
    main()
    
    


