import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label

# Landscape sizes
L = [20, 50, 100, 200, 500, 1000]

# Test count
N_tests = 100

# Tree occupation probabilities
P = np.linspace(0, 1, N_tests)
P = np.delete(P, 0)

print(P)

S_avg = {}

def generate_forest(l, p):
    pre = np.random.random((l, l))
    return np.asarray([[1 if x < p else 0 for x in row] for row in pre])

for l in L:
    if(l >= 200):
        N_tests = 2000//l
    s = []
    S_avg[l] = []
    for p in P:
        for nt in range(N_tests): 
            forest = generate_forest(l, p)
            print("generating forest " + str(nt) + " at " + str(p) + " for L=" + str(l))
            labeled, n = label(forest)
            zeroless = [x for x in labeled.flatten() if x > 0]
            if(len(zeroless) == 0):
                s.append(0)
                continue
            s.append( np.bincount(zeroless).max() / (l*l) )
        S_avg[l].append(sum(s) / len(s))


print(S_avg)

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
shapes = ['.', 'o', 'v', '^', 's']
c = 0
s = 0

for li in S_avg:
    plt.plot(P, S_avg[li], colors[c%7] + shapes[s%5], label="L = "+str(li), markersize=3.7)
    c+=1
    s+=1


# plt.matshow(labeled, cmap='gist_earth')
# plt.axis('off')
# plt.title('L = ' + str(L) + ', p = ' + str(p))
plt.xlabel("Tree occupation probability")
plt.ylabel("Average largest forest size")
plt.legend()
plt.show()