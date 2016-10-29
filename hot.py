import matplotlib.pyplot as plt
import numpy as np
import math
from operator import itemgetter
from scipy.ndimage import label

# Landscape size
L = 8

D = 10

# Test count
N_tests = 2

# Tree occupation probability
p = 0.58

S_avg = {}

def generate_forest(l):
    # print   ("gafs:" + str(type(labeled_forest)))
    pre = np.zeros((l, l))
    return np.asarray([[1 if x < p else 0 for x in row] for row in pre])

def place_tree(labeled_forest, x, y):
    # print   ("  pt:" + str(type(labeled_forest)))
    # print(labeled_forest[y][x])
    # print(labeled_forest)
    labeled_forest = np.clip(labeled_forest, 0, 1) # unlabel the forest groups
    labeled_forest[y][x] = 1 # add our new tree
    # print(str(x) + "," + str(y))
    # print("\n")
    labeled_forest = label(labeled_forest) # recalculate groups
    return labeled_forest[0]

def get_spark_distribution(L):
    l = L/10
    out = np.zeros((L,L))
    for j in range(L):
        for i in range(L):
            out[j][i] = math.exp(-i/l)*math.exp(-j/l)
    norm = 1 / sum(sum(out))
    out = norm * out
    return out

spark_dist = get_spark_distribution(L)

def get_forest_size(labeled_forest, i, j):
    # print   (" gfs:" + str(type(labeled_forest)))
    target = labeled_forest[j][i]
    if(target == 0):
        return 0
    else:
        return np.bincount(labeled_forest.flatten())[target]

"""
Compute the average fire size for a test tree at i, j
"""
def get_average_fire_size(labeled_forest):
    # print   ("gafs:" + str(type(labeled_forest)))
    sum = 0
    for j in range(L):
        for i in range(L):
            sum += spark_dist[j][i] * get_forest_size(labeled_forest, i, j)
    return sum

    
"""
Look at a forest and step the simulation (make the best move possible for a given D)
@param {2darray} forest The input forest to step 
@param {number} D The number of candidates to evaluate
@returns {(2darray, float)} A tuple of the new forest with another tree and its average fire size
"""
def step(labeled_forest, D):
    # print   ("step:" + str(type(labeled_forest)))
    candidates = []
    field_positions = [(row_ind, col_ind) for row_ind, row in enumerate(labeled_forest) for col_ind, val in enumerate(labeled_forest[row_ind]) if val ==0]
    # print(field_positions)
    # print(labeled_forest)
    # print("\n")
    for d in range(D):
        choice = np.random.randint(0, len(field_positions))
        x, y = field_positions[choice]
        print(str(len(field_positions)) + " " + str(labeled_forest[y][x]))
        del field_positions[choice]
        hyp = place_tree(labeled_forest, x, y)
        cost = get_average_fire_size(hyp)
        fyield = sum(sum(1 for i in row if i) for row in hyp)/(L*L) - cost
        candidates.append((hyp, fyield))
    print("\n\n\n")
    return max(candidates, key=itemgetter(1))

    
s = []
avg_size_freq = []

forest = np.zeros((L, L))
print("generating forest...")
labeled, n = label(forest)
fyield = 0
forest_and_fs = (labeled, 0)
codod = 0
# print   ("root:" + str(type(forest_and_fs[0])))
while(codod < 90):
    forest_and_fs = step(forest_and_fs[0], D)
    # yield = computed density - average forest fire size
    codod+=1

plt.matshow(forest_and_fs[0], cmap='gist_earth')
#plt.axis('off')
#plt.title( 'Forest size frequency distribution for L = ' + str(l))
#plt.xlabel("log10 forest size")
#plt.ylabel("log10 relative frequency")
plt.legend()
plt.show()