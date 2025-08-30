import numpy as np

def codificarSecuencias(datos:list)->np.array:
    
    
    codificacion = {'T': 1.0, 'C': 2.0 , 'A': 3.0, 'G': 4.0, '?': np.nan}
 

    secuencias = []
    for secuencia in datos:
        secuencia_codificada = [codificacion[char] for char in secuencia]
        secuencias.append(secuencia_codificada)
    
    secuencia = np.array(secuencias)

    return secuencia

   
def decodificarSecuencias(datos: np.array)->list:
    

    decodificacion = {1.0: 'T', 2.0: 'C', 3.0: 'A', 4.0: 'G', np.nan: '?'}
  
    
    secuencias = []
    for secuencia in datos:
        secuencia_decodificada = ''.join(decodificacion[val] if val in decodificacion else '?' for val in secuencia)
        secuencias.append(secuencia_decodificada)
    
    return secuencias
   
def corregir(datos:np.array)->np.array:
    corregido = np.abs(np.round(datos))
    return corregido




if __name__ == "__main__":
    
    
    diccionario = {
        "organismo1": "ACGT?ACGT",
        "organismo2": "TG??ATGCA"
    }
    
    secuencias = list(diccionario.values())
    
    print ("Secuencias originales")
    print(secuencias)
    
    print ("Secuencias codificadas")
    npSecuencia_1 = codificarSecuencias(secuencias)
    print(npSecuencia_1)
    
    print ("Secuencias decodificadas")
    secuencias_decodificadas = decodificarSecuencias(npSecuencia_1)
    print(secuencias_decodificadas)
    
    
    
    
    

   