# Simple imputer
from sklearn.impute import SimpleImputer
# Iterative imputer
from sklearn.experimental import enable_iterative_imputer  #noqa 
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.svm import LinearSVR
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern
from sklearn.cross_decomposition import PLSRegression
from sklearn.isotonic import IsotonicRegression
# KNN imputer
from sklearn.impute import KNNImputer as knnimputer
# Custom imputer
from CustomImputers.biologicalImputer import BiologicalImputer as bioImputer
from CustomImputers.AlternativeImputer import AlternativeImputer as alternativeImputer

import numpy as np
import os
import time


def process_imputer(data: np.array, imputer) -> np.array:
    
    if isinstance(imputer, IterativeImputer) and (isinstance(imputer.estimator, PLSRegression) or isinstance(imputer.estimator, IsotonicRegression)):
        start=time.perf_counter()
        original_shape = data.shape
        data = data.reshape(-1, 1)
        out_data = imputer.fit_transform(data)  
        out_data = out_data.reshape(original_shape)
        fin = time.perf_counter()      
    elif imputer is None:
        start = time.perf_counter()
        out_data = data
        fin = time.perf_counter()
    elif isinstance(imputer, knnimputer) or isinstance(imputer, SimpleImputer):
        start=time.perf_counter()  
        out_data = imputer.fit_transform(data)
        fin=time.perf_counter()
     
    else:     
        start=time.perf_counter()  
        out_data = imputer.fit_transform(data)
        fin=time.perf_counter()
        
    impute_time = fin - start
    return out_data, impute_time



### Simple Imputers
def SimpleImputer_mean(data: np.array):
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    out_data, impute_time = process_imputer(data, imputer)

    return out_data, impute_time

def SimpleImputer_median(data: np.array):
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def SimpleImputer_most_frequent(data: np.array):
    imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

### Iterative Imputers

def commonIterativeImputer() -> IterativeImputer:
    return IterativeImputer(initial_strategy="most_frequent",
                            missing_values=np.nan,
                            min_value=1,
                            max_value=4,
                            n_nearest_features=None
                            )

def IterativeImputer_BayesianRidge(data: np.array) -> np.array:    
    imputer = commonIterativeImputer()
    imputer.estimator = BayesianRidge()
    
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def IterativeImputer_KNeighborsRegressor(data: np.array) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = KNeighborsRegressor(n_neighbors=1, n_jobs=-1)
    # imputer.estimator = KNeighborsRegressor(n_jobs=-1)
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def IterativeImputer_HistGradientBoostingRegressor(data: np.array) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = HistGradientBoostingRegressor(min_samples_leaf=1)
    os.environ["OMP_NUM_THREADS"] = "1"  # OpenMP (usado por sklearn)
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def IterativeImputer_LinearSVR(data: np.array) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = LinearSVR()
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def IterativeImputer_MLPRegressor(data: np.array) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = MLPRegressor(solver="lbfgs")
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def IterativeImputer_GaussianProcessRegressor(data: np.array) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = GaussianProcessRegressor()
 
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def IterativeImputer_PLSRegression(data: np.array) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = PLSRegression()
    imputed_data = np.zeros(data.shape)
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def IterativeImputer_IsotonicRegression(data: np.array) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = IsotonicRegression(increasing="auto", y_min=1, y_max=4)
    imputed_data = np.zeros(data.shape)
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

### KNN Imputer

def KNNImputer(data: np.array) -> np.array:
    # imputer = knnimputer(missing_values=np.nan)
    imputer = knnimputer(missing_values=np.nan, n_neighbors= 1)
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

def NullImputer(data: np.array) -> np.array:
    imputer = None
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

### Biological Imputer

def BiologicalImputer(data: np.array) -> np.array:
    imputer = bioImputer()
    out_data, impute_time = process_imputer(data, imputer)
    return out_data, impute_time

### JC Imputer - Alternativa 1

def AlternativeImputer(data: np.array) -> np.array:
    imputer = alternativeImputer(strategy='most_frequent')
    outData, impute_time = process_imputer(data, imputer)
    return outData, impute_time


if __name__ == "__main__":
    pass 