import numpy as np
from scipy.linalg import get_blas_funcs
from sklearn.cluster import kmeans_plusplus


def euclid_skip(xxt, xv, v):
    ed2 = xxt + np.inner(v,v).ravel() - xv
    return ed2


def calculate_shortest_distance_refine1(data, centers):
    distance = np.empty([data.shape[0], centers.shape[0]])
    xxv = np.einsum('ij,ij->i',data, data) 
    xv = 2* np.inner(data, centers) #data.dot(centers.T) # BLAS LEVEL 3
    for i in range(centers.shape[0]):
        distance[:, i] = euclid_skip(xxv, xv[:,i], centers[i]) # LA.norm(data - centers[i], axis=1)
        
    return np.min(distance, axis=1)


def calculate_shortest_distance_refine2(data, centers): # involve additional memory copy, is slow for high dimensional data
    distance = np.empty([data.shape[0], centers.shape[0]])
    xxv = np.einsum('ij,ij->i',data, data) 
    gemm = get_blas_funcs("gemm", [data, centers.T])
    xv = 2*gemm(1, data, centers.T)
    for i in range(centers.shape[0]):
        distance[:, i] = euclid_skip(xxv, xv[:,i], centers[i]) # LA.norm(data - centers[i], axis=1)
        
    return np.min(distance, axis=1)


def calculate_shortest_distance_label(data, centers):
    distance = np.empty([data.shape[0], centers.shape[0]])
    xxv = np.einsum('ij,ij->i',data, data) 
    xv = 2*data.dot(centers.T) # BLAS LEVEL 3
    for i in range(centers.shape[0]):
        distance[:, i] = euclid_skip(xxv, xv[:,i], centers[i]) # LA.norm(data - centers[i], axis=1)
        
    return np.argmin(distance, axis=1)


class kmeans:
    def __init__(self, k=1, max_iter=300):
        self.n_clusters = k
        self.max_iter = max_iter
        self.labels_ = None
        self.record_iters = None # the iterations
        
    def fit_predict(self, X, init_centers):
        return self.fit(X, init_centers).labels_
        
    def fit(self, X, init_centers):
        self.centers = init_centers
        self.record_iters = 0
        prev_centers = None
        while np.not_equal(self.centers, prev_centers).any() and self.record_iters < self.max_iter:
            self.labels_ = calculate_shortest_distance_label(X, self.centers)

            prev_centers = self.centers
            for i in range(self.n_clusters):
                self.centers[i] = np.mean(X[self.labels_ == i], axis=0)
                
            for i, center in enumerate(self.centers):
                if np.isnan(center).any():  # Catch any np.nans, resulting from a centroid having no points
                    self.centers[i] = prev_centers[i]
                    
            self.record_iters += 1
            
        return self
            
    def predict(self, X):
        return calculate_shortest_distance_label(X, self.centers)
    
    

    

class kmeanspp:
    def __init__(self, k=1, max_iter=300, random_state=2022):
        self.n_clusters = k
        self.max_iter = max_iter
        self.labels_ = None
        self.record_iters = None # the iterations
        self.random_state = random_state
        
    def fit_predict(self, X):
        return self.fit(X).labels_
        
    def fit(self, X):
        self.centers, _ = kmeans_plusplus(X, self.n_clusters, random_state=self.random_state)
        self.record_iters = 0
        prev_centers = None
        while np.not_equal(self.centers, prev_centers).any() and self.record_iters < self.max_iter:
            self.labels_ = calculate_shortest_distance_label(X, self.centers)

            prev_centers = self.centers
            for i in range(self.n_clusters):
                self.centers[i] = np.mean(X[self.labels_ == i], axis=0)
                
            for i, center in enumerate(self.centers):
                if np.isnan(center).any():  # Catch any np.nans, resulting from a centroid having no points
                    self.centers[i] = prev_centers[i]
                    
            self.record_iters += 1
            
        return self
            
    def predict(self, X):
        return calculate_shortest_distance_label(X, self.centers)
