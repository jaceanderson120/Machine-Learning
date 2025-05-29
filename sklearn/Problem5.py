import math
import random
import numpy as np

def bgd_l2(data, y, w, eta, delta, lam, num_iter):
    n, d = data.shape
    w_star = w.copy()
    lossHistory = []
    
    for t in range(num_iter):
        gradient = np.zeros_like(w_star)
        totalLoss = 0.0
        
        for i in range(n):
            residual = float(y[i] - np.dot(w_star, data[i]))
            if residual >= delta:
                diff = residual - delta
                totalLoss += diff * diff
                gradient += -2.0 * diff * data[i]
            elif residual <= -delta:
                diff = residual + delta
                totalLoss += diff * diff
                gradient += -2.0 * diff * data[i]

        totalLoss = totalLoss / n
        regularizationTerm = np.sum(w_star * w_star)

        totalLoss += lam * regularizationTerm
        lossHistory.append(totalLoss)

        gradient = gradient / n
        gradient += 2.0 * lam * w_star
        w_star = w_star - eta * gradient

    return w_star, lossHistory

def sgd_l2(data, y, w, eta, delta, lam, num_iter, i=-1):
    n, d = data.shape
    w_star = w.copy()
    lossHistory = []
    
    if i != -1:
        residual = float(y[i] - np.dot(w_star, data[i]))
        
        if residual >= delta:
            diff = residual - delta
            gradient = -2.0 * diff * data[i]
        elif residual <= -delta:
            diff = residual + delta
            gradient = -2.0 * diff * data[i]
        else:
            gradient = np.zeros_like(w_star)
            
        gradient += 2.0 * lam * w_star
        w_star = w_star - eta * gradient
        
        dataLoss = 0.0
        for j in range(n):
            r = float(y[j] - np.dot(w_star, data[j]))
            if r >= delta:
                diff = r - delta
                dataLoss += diff * diff
            elif r <= -delta:
                diff = r + delta
                dataLoss += diff * diff
        dataLoss /= n
        dataLoss += lam * np.sum(w_star * w_star)
        lossHistory.append(dataLoss)
        
    else:
        for t in range(1, num_iter+1):
            randomData = random.randint(0, n-1)
            residual = float(y[randomData] - np.dot(w_star, data[randomData]))
            
            if residual >= delta:
                diff = residual - delta
                gradient = -2.0 * diff * data[randomData]
            elif residual <= -delta:
                diff = residual + delta
                gradient = -2.0 * diff * data[randomData]
            else:
                gradient = np.zeros_like(w_star)
            
            gradient += 2.0 * lam * w_star
            learningRate = eta / np.sqrt(t)
            w_star = w_star - learningRate * gradient
            
            dataLoss = 0.0
            for j in range(n):
                point = float(y[j] - np.dot(w_star, data[j]))
                if point >= delta:
                    diff = point - delta
                    dataLoss += diff * diff
                elif point <= -delta:
                    diff = point + delta
                    dataLoss += diff * diff
            dataLoss /= n
            dataLoss += lam * np.sum(w_star * w_star)
            lossHistory.append(dataLoss)
    
    return w_star, lossHistory