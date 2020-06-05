from mpl_toolkits import mplot3d
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt


def kmeans_clsuster(X, n_clusters, random_state):
    z = X[:,1] / np.linalg.norm(X[:,1])
    x = X[:,2] / np.linalg.norm(X[:,2])
    y = X[:,3] / np.linalg.norm(X[:,3])     
    Xt = np.array([x,y,z], dtype=float).T
    
    kmeans = KMeans(n_clusters=n_clusters, 
                    random_state=random_state).fit(Xt)
    
    cluster_labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    max_cluster = np.argmax(kmeans.cluster_centers_[:,2])
    first_cluster_members = np.argwhere(kmeans.labels_ == max_cluster).reshape(-1)
    
    return (cluster_labels, cluster_centers, max_cluster, first_cluster_members)

def plot_2d(X):
    labels = np.array(X[:,0], dtype = int)
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(X[:,2], X[:,3], s= X[:,1]**4)
    for label, x, y in zip(labels, X[:,2], X[:,3]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-3, 3),
            textcoords='offset points', ha='right', va='bottom')
    plt.show()
    
def plot_3d(X):
    x = np.array(X[:,2], dtype=float)
    y = np.array(X[:,3], dtype=float)
    z = np.array(X[:,1], dtype=float)
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1,1,1)
    ax = plt.axes(projection='3d')

    # Data for three-dimensional scattered points
    zdata = z
    xdata = x
    ydata = y
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='viridis', linewidth=0.5)
    plt.show();