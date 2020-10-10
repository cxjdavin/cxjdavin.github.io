import numpy as np
from itertools import cycle, islice
from matplotlib import cm
from matplotlib import pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.utils import check_random_state
from sklearn.utils.extmath import row_norms, squared_norm, stable_cumsum

# Setup
generator = np.random.RandomState(1337)
colors = np.array(plt.get_cmap("Accent").colors)

# Generate data
print("Generating data...")
centers = [(2.28,1.48), (5.92,1.38), (1.4,4.48), (8.2,3.04), (4.02,3.28), (6.32,5.06)]
std = np.array([0.60,0.55,0.50,0.65,0.70,0.60])
std = std/2
samples = [3000, 2000, 2000, 2000, 1000, 500]
n = sum(samples)
X, y = make_blobs(n_samples=samples, centers=centers, cluster_std=std, random_state=1)
c = generator.permutation(n)[:6]
c = X[c]
all_distances = euclidean_distances(c, X, squared=True)
all_distances_sorted_idx = np.argpartition(all_distances, 1, axis=0)
closest_dist_idx = all_distances_sorted_idx[0]
fig,ax = plt.subplots(1)
#ax.scatter(X[:,0], X[:,1], s=15, color=colors[closest_dist_idx])
#ax.scatter(c[:,0], c[:,1], s=70, color='#000000')
ax.scatter(X[:,0], X[:,1], s=5, color=colors[closest_dist_idx])
ax.scatter(c[:,0], c[:,1], s=50, marker='*', color=colors, edgecolors='black')
fig.patch.set_visible(False)
ax.axis('off')
#plt.show()
plt.savefig("lloyd01.png")


old_means = c
ctr = 2
while True and ctr < 50:
    print("Running Lloyd", ctr)
    means = KMeans(n_clusters=6, init=c, n_init=1, max_iter=1, tol=1e-10, random_state=generator)
    means.fit(X)
    y = means.predict(X)
    c = means.cluster_centers_
    fig,ax = plt.subplots(1)
    ax.scatter(X[:,0], X[:,1], s=5, color=colors[y])
    ax.scatter(c[:,0], c[:,1], s=50, marker='*', color=colors, edgecolors='black')
    fig.patch.set_visible(False)
    ax.axis('off')
    #plt.show()
    if ctr < 10:
        plt.savefig("lloyd0{0}.png".format(ctr))
    else:
        plt.savefig("lloyd{0}.png".format(ctr))

    means = means.cluster_centers_
    print(means)
    if np.array_equal(old_means, means):
        break
    else:
        old_means = means
        ctr += 1


