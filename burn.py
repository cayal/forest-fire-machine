
"""
In order to reduce the runtime complexity of this function,
I leveraged the fact that P(A and B) = P(A)P(B) whenever P(B) = P(B|A).
This let me use a random exponential distribution to look up the burn
index without iterating over the array (the exponential distribution has
the bonus of normalizing the distribution on each axis)
"""
def burn(labeled_forest):
	l = L / 10
	j = max(math.floor(np.random.exponential(l)), L-1)
	i = max(math.floor(np.random.exponential(l)), L-1)
	burn_target = labeled_forest[j][i]
	trees_burned = np.bincount(labeled_forest.flatten())[burn_target]
	return trees_burned
	