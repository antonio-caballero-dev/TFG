from sklearn.impute import SimpleImputer
import numpy as np



class AlternativeImputer():
    
    def __init__(self, strategy='most_frequent', k_neighbors=5, consensus_threshold=0.6):
        self.strategy = strategy
        self.incompleteData = None
        self.seedData = None #self.generateSeed(incompleteData)
        self.distMatrix = None #self.generateJCDistMatrix(self.seedData)
        self.missingMask =  None # np.isnan(incompleteData)
        
        self.k_neighbors = k_neighbors
        self.consensus_threshold = consensus_threshold
        
    def generateSeed(self, incompleteData):
        simpleImputer = SimpleImputer(missing_values=np.nan, strategy=self.strategy)
        imputedData = simpleImputer.fit_transform(incompleteData)
        return imputedData
    
    def generateJCDistMatrix(self, seedMatrix):
        """
            Calcula la matriz de distancias de Jukes-Cantor entre las secuencias en seedMatrix.
            Se usa el modelo Jukes-Cantor.
            
            **Fórmula**:
            d = -3/4 ln(1 - 4p/3)
            
            donde:
            p: proporción de diferencias (número de diferencias / longitud de la secuencia)
        """
        
        nSamples = seedMatrix.shape[0]
        nFeatures = seedMatrix.shape[1]
        
        distMatrix = np.zeros((nSamples, nSamples))
        
        for i in range(nSamples):
            distMatrix[i, i] = np.inf
        
        # Se calcula la distancia entre cada par de secuencias
        for i in range(nSamples):
            for j in range(i + 1, nSamples):
                # Calcular el número de diferencias entre las secuencias i y j
                differences = np.sum(seedMatrix[i] != seedMatrix[j])
                
                # Se normaliza la distancia por el número de características
                p = differences / nFeatures
                
                if p < 0.75:
                    # p nunca será < 0.75, se multiplica por -0.75 para que la distancia sea positiva y se corrige la distancia
                    distMatrix[i, j] = -1*(3/4) * np.log(1 - (4/3) * p) # Se usa la fórmula de Jukes-Cantor
                else:
                    distMatrix[i, j] = np.inf  # Si es mayor a 0.75, la distancia es infinito
                distMatrix[j, i] = distMatrix[i, j]
            
        return distMatrix
    
        
        

    
    # Falta por implementar el paso iterativo hasta convergencia
    def fit_transform(self, incompleteData):
        """
            Imputa sobre incompleteData y devuelve el resultado.
        """
        self.incompleteData = incompleteData
        self.seedData = self.generateSeed(incompleteData)
        self.distMatrix = self.generateJCDistMatrix(self.seedData)
        self.missingMask = np.isnan(incompleteData)
        
        
        refinedData = self.seedData.copy()
        nSamples, nFeatures = refinedData.shape
        
        # Parámetros importantes
        k =  self.k_neighbors #5  # número de vecinos a considerar podría ser variable (por ahora es fijo)
        consensus_threshold = self.consensus_threshold  # umbral: al menos el 60% de los vecinos deben coincidir
        
        
        # Iterar sobre cada muestra y cada posición faltante (según la máscara original)
        for i in range(nSamples):
            for j in range(nFeatures):
                if self.missingMask[i, j]:
                    
                    # Se obtienen las distancias de la secuencia i a todas las demás
                    distances = self.distMatrix[i, :].copy()
                    
                    # Excluir la propia secuencia
                    distances[i] = np.inf
                    
                    # Se obtienen los índices de los k vecinos más cercanos
                    neighbor_indices = np.argsort(distances)[:k]
                    
                    # Se extraen los valores en la posición j de esos vecinos
                    neighbor_values = refinedData[neighbor_indices, j]
                    
                    # Se cuentan las ocurrencias de cada valor 
                    unique, counts = np.unique(neighbor_values, return_counts=True)
                    frequencies = dict(zip(unique, counts))
                    
                    # Si existe algún valor, se busca el que tenga mayor frecuencia
                    if frequencies:
                        # Se obtiene el valor de consenso y su frecuencia mayor
                        consensus_value = max(frequencies, key=frequencies.get)
                        
                        # Se calcula la frecuencia relativa del valor de consenso
                        freq_rel = frequencies[consensus_value] / k
                        
                        # Si la frecuencia relativa supera el umbral, se actualiza el valor en refinedData
                        if freq_rel >= consensus_threshold:
                            refinedData[i, j] = consensus_value
        
        return refinedData
        