import random
import numpy as np
import matplotlib.pyplot as plt

from Problem5 import bgd_l2, sgd_l2

def fetchData():
    data_raw = np.load("data.npy")
    
    ones = np.ones((data_raw.shape[0], 1))
    data = np.hstack((ones, data_raw))
    
    y = data[:, -1]
    meanY = np.mean(y)
    stdY = np.std(y)
    stdY = 1.0 if stdY == 0 else stdY
    y = (y - meanY) / stdY

    X = data[:, [0, 2]]
    Xint = X[:, 0].reshape(-1, 1)
    Xfeature = X[:, 1].reshape(-1, 1)

    meanX = np.mean(Xfeature, axis=0)
    stdX = np.std(Xfeature, axis=0)
    stdX[stdX == 0] = 1.0
    XFeatureStd = (Xfeature - meanX) / stdX

    X = np.hstack([Xint, XFeatureStd])

    return X, y

if __name__ == '__main__':
    X, y = fetchData()

    wStar = np.zeros(X.shape[1])

    gdInfo = [
        (0.05, 0.1, 0.001, 50),
        (0.1, 0.01, 0.001, 50),
        (0.1, 0.0,  0.001, 100),
        (0.1, 0.0,  0.0,   100)
    ]

    sgdInfo = [
        (1.0, 0.1,  0.5, 800),
        (1.0, 0.01, 0.1, 800),
        (1.0, 0.0,  0.0,  40),
        (1.0, 0.0,  0.0, 800)
    ]

    iteration = 1
    for iteration, (eta, delta, lam, num_iter) in enumerate(gdInfo, start=1):
        w, lossHistory = bgd_l2(X, y, wStar, eta, delta, lam, num_iter)
        title = f"BGD: {iteration}"
        plt.figure()
        plt.plot(range(len(lossHistory)), lossHistory, marker='o', linestyle='-')
        plt.title(title)
        plt.xlabel('Iteration')
        plt.ylabel('Loss')
        plt.show()

    for iteration, (eta, delta, lam, num_iter) in enumerate(sgdInfo, start=1):
        w, lossHistory = sgd_l2(X, y, wStar, eta, delta, lam, num_iter)
        title = f"SGD: {iteration}"
        plt.figure()
        plt.plot(range(len(lossHistory)), lossHistory, marker='o', linestyle='-')
        plt.title(title)
        plt.xlabel('Iteration')
        plt.ylabel('Loss')
        plt.show()
