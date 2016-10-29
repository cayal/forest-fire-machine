import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label

# Landscape size
l = 1000

# Test count
N_tests = 10

# Tree occupation probability
p = 0.58 + ((1 - 0.58) / 2)

S_avg = {}

def generate_forest(l, p):
    pre = np.random.random((l, l))
    return np.asarray([[1 if x < p else 0 for x in row] for row in pre])

s = []
avg_size_freq = []

for nt in range(N_tests): 
    forest = generate_forest(l, p)
    print("generating forest " + str(nt) + " at " + str(p) + " for L=" + str(l))
    labeled, n = label(forest)
    forest_sizes = np.bincount(labeled.flatten())
    size_freq = np.bincount(forest_sizes)
    avg_size_freq = avg_size_freq if len(avg_size_freq) > 0 else np.zeros(forest_sizes.max()+1)
    avg_size_freq = [sum(x) for x in zip(size_freq/N_tests, avg_size_freq)]

del avg_size_freq[0]

plt.plot(np.log10(range(len(avg_size_freq))), np.log10(avg_size_freq), "b.", markersize=3.7)



# plt.matshow(labeled, cmap='gist_earth')
# plt.axis('off')
plt.title( 'Forest size frequency distribution for L = ' + str(l))
plt.xlabel("log10 forest size")
plt.ylabel("log10 relative frequency")
plt.legend()
plt.show()