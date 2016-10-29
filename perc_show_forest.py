import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label

# Landscape size
l = 1000

# Tree occupation probability
p = 0.5

def generate_forest(l, p):
    pre = np.random.random((l, l))
    return np.asarray([[1 if x < p else 0 for x in row] for row in pre])

forest = generate_forest(l, p)
labeled, n = label(forest)


plt.matshow(labeled, cmap='gist_earth')
plt.axis('off')
plt.title('L = ' + str(l) + ', p = ' + str(p))
plt.show()