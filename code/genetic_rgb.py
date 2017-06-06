"""
Module that contains functions for genetic algorithm functionality 
called from main.py
"""


from random import randint, random
from operator import add
import numpy as np

def individual(length, min, max):
    """
    Create a member of the population from foreground 
    image selection flattened to a vector
    """
    return np.random.random_integers(min, max, (length, 3))

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values
    """

    return [ individual(length, min, max) for x in xrange(count) ]

def fitness(indiv, target_rgb, target_var, popsize):
    """
    Determine the fitness of an individual.

    individual: the individual to evaluate
    target: the target number individuals are aiming for
    """
    
    r_in = np.argmax(np.bincount(indiv[:,0]))
    b_in = np.argmax(np.bincount(indiv[:,1]))
    g_in = np.argmax(np.bincount(indiv[:,2]))
    
    # difference to dominant rgb color
    rgb_diff =  np.sqrt(((r_in - target_rgb[0])**2 + (b_in - target_rgb[1])**2 + (g_in - target_rgb[2])**2)/3.0)
    # normalise

    r_var = np.var(indiv[:,0])
    g_var = np.var(indiv[:,1])
    b_var = np.var(indiv[:,2])

    var_diff = np.sqrt(((r_var - target_var[0])**2 + (b_var - target_var[1])**2 + (g_var - target_var[2])**2)/3.0)
    # normalize variance feature
    var_diff = var_diff/float(popsize)

    return sum([rgb_diff, var_diff])

def grade(pop, target_rgb, target_var):
    """
    Find average fitness for a population.
    """

    summed = sum([fitness(i, target_rgb, target_var, len(pop)) for i in pop])
    return summed / (float(len(pop)))

def evolve(pop, target_rgb, target_var, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x, target_rgb, target_var, len(pop)), x) for x in pop]
    # sorted() increasing per default
    graded = [x[1] for x in sorted(graded, key=lambda x: x[0])]
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
            #print pos_to_mutate

            individual[pos_to_mutate] = np.array([randint(min(individual[:,0]), max(individual[:,0])), 
                                        randint(min(individual[:,1]), max(individual[:,1])), 
                                        randint(min(individual[:,2]), max(individual[:,2]))])
        
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
            child = np.vstack((male[:half], female[half:]))
            children.append(child)        
    parents.extend(children)
    return parents

if __name__ == '__main__':
    import numpy as np
    imgin = [randint(0,255) for i in range(0,10)]
    target = (220, 10, 145)
    p_count = 200
    i_length = 100
    i_min = 0
    i_max = 255
    p = population(p_count, i_length, i_min, i_max)
    fitness_history = [grade(p, target),]
    retain = 0.2
    random_select = 0.1
    mutate = 0.008
    p_iter = 500
    for i in xrange(p_iter):
        p = evolve(p, target)
        fitness_history.append(grade(p, target))
    
    for cost in fitness_history:
        print cost
    
    p = p[0]
    index_out = (np.argmax(np.bincount(p[:,0])), 
                 np.argmax(np.bincount(p[:,1])),
                 np.argmax(np.bincount(p[:,2])))
    print target
    print index_out

    
