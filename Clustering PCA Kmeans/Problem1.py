import numpy as np

def k_init(X, k):
    """ k-means++: initialization algorithm
    
    Parameters
    ----------
    X: array, shape(n ,d)
        Input array of n samples and d features
    
    k: int
        The number of clusters
    
    Returns
    -------
    init_centers: array (k, d)
        The initialize centers for kmeans++
    """
    centerPts = [np.random.randint(X.shape[0])]
    centers = [X[centerPts[0]]]
    for y in range(1, k):
        lengths = np.array([min([np.sum((x - c) ** 2) for c in centers]) for x in X])
        probs = lengths / np.sum(lengths)
        next_idx = np.random.choice(X.shape[0], p=probs)
        centers.append(X[next_idx])
    
    returnArr = np.array(centers)
    return returnArr


def k_means_pp(X, k, max_iter):
    """ k-means++ clustering algorithm
    
    Parameters
    ----------
    X: array, shape(n ,d)
        Input array of n samples and d features
    
    k: int
        The number of clusters
    
    max_iter: int
        Maximum number of iteration
    
    Returns
    -------
    final_centers: array, shape (k, d)
        The final cluster centers
    """
    centerPt = k_init(X, k)
    objVals = []
    
    for i in range(max_iter):
        obj = compute_objective(X, centerPt)
        objVals.append(obj)
        newCenterPt = np.zeros_like(centerPt)
        dataClusters = assign_data2clusters(X, centerPt)
        for j in range(k):
            dataMask = dataClusters[:, j] == 1
            cluster = X[dataMask]
            if len(cluster) > 0:
                newCenterPt[j] = np.mean(cluster, axis=0)
            else:
                newCenterPt[j] = centerPt[j]
        if np.allclose(centerPt, newCenterPt):
            break
            
        centerPt = newCenterPt
    
    returnArr = np.array(objVals)
    return centerPt, returnArr


def assign_data2clusters(X, C):
    """ Assignments of data to the clusters
    
    Parameters
    ----------
    X: array, shape(n ,d)
        Input array of n samples and d features
    
    C: array, shape(k ,d)
        The final cluster centers
    
    Returns
    -------
    data_map: array, shape(n, k)
        The binary matrix A which shows the assignments of data points (X) to
        the input centers (C).
    """

    length = np.zeros((X.shape[0], C.shape[0]))
    for i in range(C.shape[0]):
        length[:, i] = np.sum((X - C[i])**2, axis=1)
    assignments = np.zeros((X.shape[0], C.shape[0]))
    closest_clusters = np.argmin(length, axis=1)
    assignments[np.arange(X.shape[0]), closest_clusters] = 1
    
    return assignments


def compute_objective(X, C):
    """ Compute the clustering objective for X and C
    
    Parameters
    ----------
    X: array, shape(n ,d)
        Input array of n samples and d features
    
    C: array, shape(k ,d)
        The final cluster centers
    
    Returns
    -------
    objective: float
        The objective for the given assignments
    """
    length = np.zeros((X.shape[0], C.shape[0]))
    for i in range(C.shape[0]):
        length[:, i] = np.sum((X - C[i])**2, axis=1)
    return np.sum(np.min(length, axis=1))