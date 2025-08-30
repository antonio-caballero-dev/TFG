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

from CustomImputers.biologicalImputer import BiologicalImputer as bioImputer

from CustomImputers.AlternativeImputer import AlternativeImputer as alternativeImputer

import numpy as np
import os
import time

from multiprocessing import Pool, cpu_count


def impute_data(data:np.array,  imputer):
    
    out_data = np.zeros(data.shape)
    
    # Si el estimador es PLSRegression o IsotonicRegression, se imputa columna a columna
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
    
    else:     
        start=time.perf_counter()  
        out_data = imputer.fit_transform(data)
        fin=time.perf_counter()
        
    impute_time = fin - start
    return out_data, impute_time

def worker(chunk:np.array, imputer,  idx:int):
    
    out_chunk, impute_time = impute_data(chunk, imputer)
    # print(f"Chunk {idx} imputado en {impute_time} segundos")
    return out_chunk, impute_time


def parallel_process(chunks:list,  imputer, n_proc:int):
    
    # print(f"Procesando {len(chunks)} chunks con {n_proc} procesos...")
    out_chunks = []
    
    with Pool(n_proc) as pool:
       out_chunks = pool.starmap(worker, [(chunk, imputer,  i) for i,chunk in enumerate(chunks)])
    
    times = [impute_time for chunk, impute_time in out_chunks]
    max_time = max(times)
    # print(f"Max time: {max_time}")
    out_chunks = [chunk for chunk, impute_time in out_chunks]
    
    out_data = np.hstack(out_chunks)
    
    return out_data, max_time

def process_imputer(data: np.array, imputer, n_proc:int):
    
    nMayores = data.shape[1] % n_proc
    chunks = []
    chunks_size_mayor = data.shape[1] // n_proc + 1
    chunks_size_menor = data.shape[1] // n_proc
    
    
    index=0
    for i in range(n_proc):
        if nMayores > 0:
            chunks.append(data[:, index:index + chunks_size_mayor])
            nMayores -= 1
            index += chunks_size_mayor
        else:
            chunks.append(data[:, index:index + chunks_size_menor])
            index += chunks_size_menor
    
            
    # print(f"Shapes para ({len(chunks)}) chunks:")
    # for chunk in chunks:
    #     print(chunk.shape)
    
    out_data, imputed_time = parallel_process(chunks,  imputer, n_proc)
    return out_data, imputed_time


    
### Simple Imputers
def SimpleImputer_mean(data: np.array,  n_proc:int):
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    out_data, impute_time = process_imputer(data, imputer, n_proc)

    return out_data, impute_time
def SimpleImputer_median(data: np.array, n_proc:int):
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time

def SimpleImputer_most_frequent(data: np.array, n_proc:int):
    imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time

### Iterative Imputers

def commonIterativeImputer()->IterativeImputer:
    return IterativeImputer(initial_strategy="most_frequent",
                            missing_values=np.nan,
                            min_value=1,
                            max_value=4,
                            n_nearest_features=None
                            )

def IterativeImputer_BayesianRidge(data: np.array, n_proc:int) -> np.array:    
    
    imputer = commonIterativeImputer()
    imputer.estimator = BayesianRidge()
    
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    
    return out_data, impute_time

def IterativeImputer_KNeighborsRegressor(data: np.array, n_proc:int) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = KNeighborsRegressor(n_neighbors=1, n_jobs=1)
    
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    
    return out_data, impute_time

def IterativeImputer_HistGradientBoostingRegressor(data: np.array, n_proc:int) -> np.array:
    imputer=commonIterativeImputer()
    imputer.estimator = HistGradientBoostingRegressor(min_samples_leaf=1)
    

    os.environ["OMP_NUM_THREADS"] = "1"  # OpenMP (usado por sklearn)
    out_data, impute_time = process_imputer(data, imputer, n_proc)

    return out_data, impute_time

def IterativeImputer_LinearSVR(data: np.array, n_proc:int) -> np.array:
    imputer = commonIterativeImputer()
    imputer.estimator = LinearSVR(max_iter=1000)
    imputer.max_iter = 10
    
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    
    return out_data, impute_time

def IterativeImputer_MLPRegressor(data: np.array, n_proc:int) -> np.array:

    imputer = commonIterativeImputer()
    imputer.estimator = MLPRegressor(solver="lbfgs")
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time

def IterativeImputer_GaussianProcessRegressor(data: np.array, n_proc:int) -> np.array:

    imputer = commonIterativeImputer()
    imputer.estimator = GaussianProcessRegressor()
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time

def IterativeImputer_PLSRegression(data: np.array, n_proc:int) -> np.array:

    imputer = commonIterativeImputer()
    imputer.estimator = PLSRegression()
    imputed_data = np.zeros(data.shape)
    
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time
    

def IterativeImputer_IsotonicRegression(data: np.array, n_proc:int) -> np.array:

    imputer = commonIterativeImputer()
    imputer.estimator = IsotonicRegression(increasing="auto", y_min=1, y_max=4)
    imputed_data = np.zeros(data.shape)
    
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time

### KNN Imputer

def KNNImputer(data: np.array, n_proc:int) -> np.array:
    imputer = knnimputer(missing_values=np.nan,
                        n_neighbors=1 
                        )
    
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    
    return out_data, impute_time



def NullImputer(data: np.array, n_proc:int) -> np.array:
    imputer = None
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time

### Biological Imputer

def BiologicalImputer(data: np.array, n_proc:int) -> np.array:
    imputer = bioImputer()
    out_data, impute_time = process_imputer(data, imputer, n_proc)
    return out_data, impute_time

### JC Imputer - Alternativa 1

def AlternativeImputer(data: np.array, n_proc:int) -> np.array:
    
    imputer = alternativeImputer(strategy='most_frequent')
    
    outData, impute_time = process_imputer(data, imputer, n_proc)
    
    return outData, impute_time


if __name__ == "__main__":
    pass 