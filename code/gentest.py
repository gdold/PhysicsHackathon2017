"""
Module that contains functions for genetic algorithm functionality 
called from main.py

Original sourced from https://lethain.com/genetic-algorithms-cool-name-damn-simple/
"""
from PIL import Image, ImageDraw
from IPython.display import display
from random import randint, random
import numpy as np
from colorthief import ColorThief
from numpy import unravel_index
from scipy import fftpack
import pylab as py
#import radialProfile
from operator import add

def individual(length, min, max):
    """
    Create a member of the population from foreground 
    image selection flattened to a vector
    """
    return [ randint(min[x],max[x]) for x in xrange(length) ]

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values
    """

    return [ individual(length, min, max) for x in xrange(count) ]

def fitness(individual, target):
    """
    Determine the fitness of an individual. Higher is better.
    individual: the individual to evaluate
    target: the target number individuals are aiming for
    """
    sum = 0.0
    for y in range(0,len(target)):
        sum += (target[y]-individual[y])**2
    return np.sqrt(sum)

def grade(pop, target):
    """
    Find average fitness for a population.
    """

#    summed = sum([sum(x) for x in pop])
    summed = sum([fitness(x,target) for x in pop])
    return summed / (float(len(pop)))

def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x, target), x) for x in pop]
    # sorted() increasing per default
    graded = [ x[1] for x in sorted(graded)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]
    # randomly add other individuals to
    # promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)
    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:

            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:half] + female[half:]
            children.append(child)        
    parents.extend(children)
    return parents

def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result)) 
    return result


def rot_ellipse(x,y,scale,colour):
        points = [(x,y)]
        ts = [t/100.0 for t in range(101)]
        xtemp = x
        ytemp = y
        pi = 3.1415926536
        theta = 2*pi*(randint(1,100))/100

        xtemp1 = xtemp + int(randint(5,scale)*np.cos(theta))
        ytemp1 = ytemp + int(randint(5,scale)*np.sin(theta))

        if(xtemp1 < xmin):
                xtemp1 = xmin
        elif(xtemp1 > xmax):
                xtemp1 = xmax
        if(ytemp1 < ymin):
                ytemp1 = ymin
        elif(ytemp1 > ymax):
                ytemp1 = ymax

        miniscale = int(scale/4)

        xtemp2 = xtemp + int(randint(5,scale)*np.cos(theta+(pi/2)))
        ytemp2 = ytemp + int(randint(5,scale)*np.sin(theta+(pi/2)))

        if(xtemp2 < xmin):
                xtemp2 = xmin 
        elif(xtemp2 > xmax):
                xtemp2 = xmax
        if(ytemp2 < ymin):
                ytemp2 = ymin

        xtemp3 = xtemp - int(randint(5,scale)*np.cos(theta))
        ytemp3 = ytemp - int(randint(5,scale)*np.sin(theta))

        if(xtemp3 < xmin):
                xtemp3 = xmin 
        elif(xtemp3 > xmax):
                xtemp3 = xmax
        if(ytemp3 < ymin):
                ytemp3 = ymin
        elif(ytemp3 > ymax):
                ytemp3 = ymax

        xtemp4 = xtemp - int(randint(5,scale)*np.cos(theta+(pi/2)))
        ytemp4 = ytemp - int(randint(5,scale)*np.sin(theta+(pi/2)))

        if(xtemp4 < xmin):
                xtemp4 = xmin 
        elif(xtemp4 > xmax):
                xtemp4 = xmax
        if(ytemp4 < ymin):
                ytemp4 = ymin
        elif(ytemp4 > ymax):
                ytemp4 = ymax

        xys = [(xtemp1,ytemp1),(xtemp2,ytemp2),(xtemp3,ytemp3),(xtemp4,ytemp4),(xtemp1+1,ytemp1+1)]
        bezier = make_bezier(xys)
        points.extend(bezier(ts))

#       draw.polygon(points, fill = colour)
#       return None
        return points

im = Image.open("desert.jpg")

draw = ImageDraw.Draw(im)
#draw.line((0, 0) + im.size, fill=128)
#draw.line((0, im.size[1], im.size[0], 0), fill=128)
#del draw

# im.size[0] --> width
# im.size[1] --> height
# foreground boundaries:

# Currently manual inputs...randomise at some point?
xmin = 200
xmax = 300
ymin = 200
ymax = 300

# WARNING: THIS WILL NOT WORK IF FORGROUND SIZE = BG SIZE, NEEDS BUFFER !!
im2 = im.crop(
        (
           xmin-20,
           ymin-20,
           xmax+20,
           ymax+20
        )
)

im2.save("temp.png")

img = ColorThief("temp.png")
palette = img.get_palette(color_count=5)                

if(float(xmax-xmin) > float(ymax-ymin)):
        scale = int((xmax-xmin)/10)
else:
        scale = int((ymax-ymin)/10)


#if __name__ == '__main__':
#    imgin = [randint(0,255) for i in range(0,10)]
from colorthief import ColorThief
img = ColorThief('frog.jpeg')
target = []
target.extend(palette[0])
target.extend(palette[1])
target.extend(palette[2])
target.extend([scale])
p_count = 1000
i_length = len(target)
i_min = [0,0,0,0,0,0,0,0,0,1]
i_max = [255,255,255,255,255,255,255,255,255,scale*10]
#    i_min = 0
#    i_max = 255
p = population(p_count, i_length, i_min, i_max)
fitness_history = [grade(p, target),]
retain = 0.4
random_select = 0.1
mutate = 0.05
p_iter = 500
gendiff = 1
genfit = 9999999

gen = 1

file = open('solutions.dat','w') 
file.close()
file = open('solutions.dat','w') 

while(gendiff > 0.01):
        p = evolve(p, target)
        gen=gen+1
        fitness_history.append([grade(p, target),p[1]])
        p = [ x for x in sorted(p)]
        gendiff = abs(1-(genfit/grade(p, target)))
        genfit = grade(p, target)
        for i in p[0]:
                file.write(str(i)+'\t') 
        file.write('\n') 

file.close() 

#    for i in fitness_history:
#        print i


print gen
print p[0]
print target

#---------------------------------------------------



