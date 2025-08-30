import numpy as np
import codonHandler
import adaptarSecuencia as aS
import re
from time import sleep
import random

class BiologicalImputer():
    
    def __init__(self, umbralFrecuencia = 0.5, maxIter = 100, verbose = False):
        self.codonHandler = codonHandler.CodonHandler()
        self.umbralFrecuencia = umbralFrecuencia
        self.maxIter = maxIter
        self.verbose = verbose
        
    def countMissing(self, X):
        count = 0
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                if np.isnan(X[i, j]):
                    count += 1
        return count
    
    def reduceFrequencyThreshold(self, cantidad):
        self.umbralFrecuencia -= cantidad
        if self.umbralFrecuencia < 0.05:
            self.umbralFrecuencia = 0.05
    
    def fillFrecuency(self, X):
        data=X.copy()
        
        for columna in range(data.shape[1]):
            dictFrecuencias = {
             
                1.0:0,
                2.0:0,
                3.0:0,
                4.0:0,
                
            }
            countNoMissing = 0 #Contador de valores no faltantes para calcular la frecuencia
            for i in range(data.shape[0]):
                if not np.isnan(data[i, columna]):
                    dictFrecuencias[data[i, columna]] += 1
                    countNoMissing += 1
           
            
            for key in dictFrecuencias:
                dictFrecuencias[key] = dictFrecuencias[key]/countNoMissing
               
            #Obtener la(s) frecuencia(s) maxima(s), si hay empate, se elige uno aleatoriamente 
            keyMaxFrequency = max(dictFrecuencias.values())
            maxKeys = [key for key, value in dictFrecuencias.items() if value == keyMaxFrequency]
            keyMaxFrequency = random.choice(maxKeys)
            
            if self.verbose:
                print(f"Máxima frecuencia: {keyMaxFrequency} en columna {columna} con frecuencias: {dictFrecuencias[keyMaxFrequency]}")
            
            
            if dictFrecuencias[keyMaxFrequency] > self.umbralFrecuencia:
                for i in range(data.shape[0]):
                    if  np.isnan(data[i, columna]):
                        data[i, columna] = keyMaxFrequency
                        
            
            
        return data, self.countMissing(data)
    
    
    def rellenarCodonIncompleto(self, codon: str, aminoAcidoFrecuente: str, listFrecuenciasColumnas) -> str:
        
        codonesPosiblesAminoacido = self.codonHandler.getCodones(aminoAcidoFrecuente) #Combinaciones de nucleotidos que codifican para el aminoacido
        
        newCodon = codon
        
        posicionesDesconocidas = [i for i in range(len(codon)) if codon[i] == '?']
        
        frecuenciasOrdenadasColumnas = []
        for i in posicionesDesconocidas:
            listaColumna = sorted(listFrecuenciasColumnas[i].keys(), key=lambda x: listFrecuenciasColumnas[i][x], reverse=True)
            frecuenciasOrdenadasColumnas.append(listaColumna)
        
        # Si solo hay una posicion desconocida, se rellena con el nucleotido mas frecuentemente encontrado en la columna
        if len(posicionesDesconocidas) == 1:
            for nucleotidoFrecuente in frecuenciasOrdenadasColumnas[0]:
                newCodon = codon.replace('?', nucleotidoFrecuente, posicionesDesconocidas[0])
                if self.codonHandler.getAminoAcido(newCodon) == aminoAcidoFrecuente:
                    return newCodon
        
        # Si hay dos posiciones desconocidas, se rellena con los dos nucleotidos mas frecuentemente encontrados en las columnas
        elif len(posicionesDesconocidas) == 2:
            for nucleotidoFrecuente1 in frecuenciasOrdenadasColumnas[0]:
                for nucleotidoFrecuente2 in frecuenciasOrdenadasColumnas[1]:
                    newCodon = codon.replace('?', nucleotidoFrecuente1, posicionesDesconocidas[0])
                    newCodon = newCodon.replace('?', nucleotidoFrecuente2, posicionesDesconocidas[1])
                    if self.codonHandler.getAminoAcido(newCodon) == aminoAcidoFrecuente:
                        return newCodon
        
        
        return newCodon
                

    def fillAminoAcid(self, X)-> np.array:
        
        dictFreqAminoAcids = {
            'phe': 0,
            'leu': 0,
            'ile': 0,
            'met': 0,
            'val': 0,
            'ser': 0,
            'pro': 0,
            'thr': 0,
            'ala': 0,
            'tyr': 0,
            'his': 0,
            'gln': 0,
            'asn': 0,
            'lys': 0,
            'asp': 0,
            'glu': 0,
            'cys': 0,
            'trp': 0,
            'arg': 0,
            'gly': 0,
            'stop': 0
        }      
       
        #Funcion interna que calcula la frecuencia de los nucleotidos en una columna en forma de char
        def frecuenciasNucleotidosColumna(X, i):
            dictFrecuencias = {
                'T':0,
                'C':0,
                'A':0,
                'G':0
            }
            countNoMissing = 0
            for fila in range(X.shape[0]):
                if not np.isnan(X[fila, i]):
                    dictFrecuencias[X_char[fila][i]] += 1
                    countNoMissing += 1
            
            for key in dictFrecuencias:
                dictFrecuencias[key] = dictFrecuencias[key]/countNoMissing
            return dictFrecuencias
        
        nMissing = self.countMissing(X)
        lastMissing = nMissing
        
        X_char = aS.decodificarSecuencias(X) #Decodificar las secuencias de np.array a char
        if self.verbose:
            print(X_char)
            
        
            
        #Contar la frecuencia de los aminoacidos en las secuencias
        codonesCompletos = 0
        for fila in range(X.shape[0]):
            aminoAcido = self.codonHandler.getAminoAcido(X_char[fila])
            if aminoAcido is not None:
                dictFreqAminoAcids[aminoAcido] += 1
                codonesCompletos += 1
        
        #Normalizar las frecuencias entre 0 y 1
        for key in dictFreqAminoAcids:
            dictFreqAminoAcids[key] = dictFreqAminoAcids[key]/codonesCompletos
   
        
        #Obtener la(s) frecuencia(s) maxima(s), si hay empate, se elige uno aleatoriamente
        keyMaxFrequency = max(dictFreqAminoAcids.values())
        maxKeys = [key for key, value in dictFreqAminoAcids.items() if value == keyMaxFrequency]
        keyMaxFrequency = random.choice(maxKeys)
        
        if self.verbose:
            print(f"Aminoacido con mayor frecuencia: {keyMaxFrequency} con frecuencia: {dictFreqAminoAcids[keyMaxFrequency]}")
        
        
        # Si la frecuencia del aminoacido es mayor al umbral, se rellenan los codones incompletos con la frecuencia maxima de los nucleotidos
        if dictFreqAminoAcids[keyMaxFrequency] > self.umbralFrecuencia:
            for fila in range(len(X_char)):
                listFreqNucleotidosColumnas = [
                    frecuenciasNucleotidosColumna(X, i) 
                    for i in range(len(X_char[fila]))
                ]
                if '?' in X_char[fila]:
                    rellenado = self.rellenarCodonIncompleto(X_char[fila], keyMaxFrequency, listFreqNucleotidosColumnas)
                    X_char[fila] = rellenado
                  
            
        X = aS.codificarSecuencias(X_char)
        
        
        return X, self.countMissing(X)
    

    
    def fit_transform(self, X):      
        
            new_X = X.copy()
            nMissing = self.countMissing(X)
            lastMissing = nMissing
            if self.verbose:
                print(f"Umbral de frecuencia - Inicial: {self.umbralFrecuencia}")
                print(f"Missing values - Inicial: {nMissing}")
            iter = 0
            while nMissing > 0 and iter < self.maxIter:
                new_X, nMissing = self.fillFrecuency(new_X)
                if self.verbose:
                    print(f"Rellenados {lastMissing - nMissing} missing values con frecuencia de nucleotidos por columna")
                
                if nMissing == lastMissing:
                    new_X, nMissing = self.fillAminoAcid(new_X)
                    if self.verbose:
                        print(f"Rellenados {lastMissing - nMissing} missing values con frecuencia de aminoacidos")
                
                if nMissing == lastMissing:
                    self.reduceFrequencyThreshold(0.05)
                    if self.verbose:
                        print(f"Reduciendo umbral de frecuencia a {self.umbralFrecuencia}")
                
                lastMissing = nMissing
                if self.verbose:
                    print(f"Iteracion {iter}: {nMissing} missing values")
                iter += 1
                
            return new_X
        
        
        
        
        
        
      
        
        

if __name__=='__main__':
    
    bioImputer = BiologicalImputer(umbralFrecuencia=0.7)
    
    X = ["?GA", "AGA", "AGA", "AGA", "CGA", "CGA", "CGA", "GGA", "GGA", "GGA", "?GA", "?GA"]
    
    X = aS.codificarSecuencias(X)
    print(X)
   
    X = bioImputer.fit_transform(X)
    print(X)

  
        
    