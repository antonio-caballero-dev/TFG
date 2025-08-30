import argparse
import os
import time
import ete3 as ete
import Bio.Phylo as phylo
import numpy as np

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Para poder importar los modulos de src

import genEstimatedTree as genTree
import robinsonFouldsComputer as robinsonFaulds
import adaptarSecuencia as adaptar

import seqGlobalImputer as seqGlobalImputer
import atexit




def verificar_archivo_phy(ruta_archivo):
    if not ruta_archivo.endswith('.phy'):
        raise ValueError("El archivo debe ser un archivo .phy")
    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
    return ruta_archivo
def verificar_archivo_nwk(ruta_archivo):
    if not ruta_archivo.endswith('.nwk'):
        raise ValueError("El archivo debe ser un archivo .nwk")
    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
    return ruta_archivo

def extraer_informacion_archivo(nombre_fichero: str):
    nombre_fichero = os.path.basename(nombre_fichero)
    partes = nombre_fichero.split('_')
    conjunto = partes[0]
    porcentaje_faltantes = partes[1]
    ejemplo = partes[3]
    total = partes[-1].split('.')[0]
    return conjunto, porcentaje_faltantes, ejemplo, total

def crear_directorios_salida(conjunto: str):
    output_dir = f"./Outputs/secuencial/{conjunto}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        os.makedirs(f"{output_dir}/imputaciones")
        os.makedirs(f"{output_dir}/arboles_estimados")
        os.makedirs(f"{output_dir}/tiempos_ejecucion")
        os.makedirs(f"{output_dir}/out_robinson_foulds")
        print(f"Directorio de salida creado: {output_dir}")
    return output_dir

def leer_archivo_phy(ruta_archivo, imprimir=False):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        n_organismos, len_secuencias = map(int, lineas[0].split())
        organismos = []
        secuencias = []
        for linea in lineas[1:]:
            partes = linea.split()
            organismos.append(partes[0])
            secuencias.append(partes[1])
        if imprimir:
            print("Organismos:")
            print(organismos)
            print("Secuencias:")
            print(secuencias)
        
    return n_organismos, len_secuencias, organismos, secuencias

def crear_flujos_escritura(output_dir, nombreFichero: str):
    if(not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    
    if(not os.path.exists(f"{output_dir}/imputaciones")):
        os.makedirs(f"{output_dir}/imputaciones")

    if(not os.path.exists(f"{output_dir}/arboles_estimados")):
        os.makedirs(f"{output_dir}/arboles_estimados")
    
    if(not os.path.exists(f"{output_dir}/tiempos_ejecucion")):
        os.makedirs(f"{output_dir}/tiempos_ejecucion")
    
    if(not os.path.exists(f"{output_dir}/out_robinson_foulds")):
        os.makedirs(f"{output_dir}/out_robinson_foulds")
        
        
    output_imputaciones = open(f"{output_dir}/imputaciones/{nombreFichero}.csv", 'w')
    output_imputaciones.write("Nombre_metodo;resultado\n")
    
    output_arboles_estimados = open(f"{output_dir}/arboles_estimados/{nombreFichero}.csv", 'w')
    output_arboles_estimados.write("Nombre_metodo;ETE Tree\n")
    
    output_tiempos_ejecucion = open(f"{output_dir}/tiempos_ejecucion/{nombreFichero}.csv", 'w')
    output_tiempos_ejecucion.write("Nombre_metodo;tiempo_ejecucion\n")
    
    output_robison_foulds = open(f"{output_dir}/out_robinson_foulds/{nombreFichero}.csv", 'w')
    output_robison_foulds.write("Nombre_metodo;Robinson Foulds;RF normalizado\n")
    
    return output_imputaciones, output_arboles_estimados, output_tiempos_ejecucion, output_robison_foulds

def cerrar_flujos_escritura(*flujos):
    for flujo in flujos:
        print(f"Fichero guardado: {flujo.name}")
        flujo.close()
        
def procesar_secuencias(nOrganismos: int,
                        lSecuencias: int,
                        secuencias_codificadas: list,
                        rFC:robinsonFaulds.RobinsonFouldsComputer,
                        output_imputaciones,
                        output_arboles_estimados,
                        output_tiempos_ejecucion,
                        output_robison_foulds,
                        metodos_imputacion : tuple,
                        ):
    '''
        Procesa las secuencias codificadas con cada metodo de imputacion y guarda los resultados en los flujos de escritura.
    '''
    for metodo in metodos_imputacion:
        
        if metodo is None:
            continue 
        # 1. Imputar secuencias y medir tiempo de ejecucion
        print(f"Procesando con metodo {metodo.__name__}...")    
        secuencias_imputadas, tiempo_ejecucion = metodo(data=secuencias_codificadas.copy())
        tiempo_ejecucion=str(tiempo_ejecucion)
        tiempo_ejecucion=tiempo_ejecucion.replace(".",",")
        print(f"Tiempo de ejecucion: {tiempo_ejecucion}")
        

        # 2. Decodificar secuencias imputadas
        if metodo.__name__ == "NullImputer":
            secuencias_imputadas = adaptar.corregir(secuencias_imputadas)
            secuencias_imputadas = adaptar.decodificarSecuencias(secuencias_imputadas)
          
            datos_imputados = list(zip(organismos, secuencias_imputadas))
            datos_imputados.insert(0, (nOrganismos, lSecuencias))
        else:
            secuencias_imputadas = adaptar.corregir(secuencias_imputadas)
            secuencias_imputadas = adaptar.decodificarSecuencias(secuencias_imputadas)
            datos_imputados = list(zip(organismos, secuencias_imputadas))
            datos_imputados.insert(0, (nOrganismos, lSecuencias))
        
        # print("Hecho.")
        
        
        # 3. Generar arbol estimado  
        arbol_estimado = genTree.generar_str_newick('\n'.join([f"{organismo} {secuencia}" for organismo, secuencia in datos_imputados]))

        
        # 4. Calcular RF
        rf, rf_norm = rFC.calcular_robinson_foulds(arbol_estimado)
        rf, rf_norm = str(rf), str(rf_norm)
        rf=rf.replace(".",",")
        rf_norm=rf_norm.replace(".",",")
        print(f"RF: {rf}, RF normalizado: {rf_norm}")
        
        # 5.Guardar resultados
        output_imputaciones.write(f"{metodo.__name__}\n")
        for organismo, secuencia in datos_imputados[1:]:
            output_imputaciones.write(f"{organismo};{secuencia}\n")
        
        
        output_arboles_estimados.write(f"{metodo.__name__};{arbol_estimado}\n")
        output_tiempos_ejecucion.write(f"{metodo.__name__};{tiempo_ejecucion}\n")
        output_robison_foulds.write(f"{metodo.__name__};{rf};{rf_norm}\n")
        
  

#comienzo del programa

if __name__ == "__main__":
        

    parser = argparse.ArgumentParser(description="Procesar un archivo .phy")
    parser.add_argument("archivo", type=verificar_archivo_phy, help="Ruta al archivo .phy")
    parser.add_argument("archivo_arbol", type=verificar_archivo_nwk, help="Ruta al archivo con el arbol de verdad")
    
    args = parser.parse_args()
    
   

    #Extraer informacion del archivo .phy
    archivo_phy = args.archivo
    print(f"Procesando archivo: {archivo_phy}")
    conjunto, porcentaje_faltantes, ejemplo, total = extraer_informacion_archivo(archivo_phy)
    
    
    # Verificar si el porcentaje de faltantes es mayor o igual al 55% y no procesar el archivo
    # 26 de febrero de 2025
    if int (porcentaje_faltantes.split('%')[0]) >=55:
        print(f"El porcentaje de faltantes es mayor o igual al 55%")
        print(f"El archivo {archivo_phy} no se procesara en este experimento")
        exit()
        
        
        
    print(f"Conjunto: {conjunto}")
    print(f"Porcentaje faltantes: {porcentaje_faltantes}")
    print(f"Ejemplo: {ejemplo} de {total}")
    output_dir = crear_directorios_salida(conjunto)

    ## Leer archivo .phy
    n_organismos, len_secuencias, organismos, secuencias = leer_archivo_phy(archivo_phy)
    print(f"Numero de organismos(samples): {n_organismos}")
    print(f"Longitud de secuencias: {len_secuencias}")

    # Codificar las secuencias para que puedan ser procesadas por los metodos de imputacion
    secuencias_codificadas = adaptar.codificarSecuencias(secuencias)


    #Extraer informacion del archivo .nwk
    archivo_arbol = args.archivo_arbol
    print(f"Archivo arbol de verdad: {archivo_arbol}")
    # Leer arbol de verdad y crear un robinsonFauldsComputer (rFC)
    rFC = robinsonFaulds.RobinsonFouldsComputer(archivo_arbol)

    # Crear flujos de escritura para las salidas
    nombreFichero = os.path.basename(archivo_phy).split('.')[0]
    output_imputaciones, output_arboles_estimados, output_tiempos_ejecucion, output_robison_foulds = crear_flujos_escritura(output_dir, nombreFichero)


    print("Ejecutando imputaciones...")
    # Procesar las secuencias con cada metodo de imputacion
    metodos_imputacion = (
        None,
        seqGlobalImputer.SimpleImputer_mean,
        seqGlobalImputer.SimpleImputer_median,
        seqGlobalImputer.SimpleImputer_most_frequent,
        # seqGlobalImputer.IterativeImputer_BayesianRidge,
        seqGlobalImputer.IterativeImputer_KNeighborsRegressor,
        # seqGlobalImputer.IterativeImputer_HistGradientBoostingRegressor,
        seqGlobalImputer.IterativeImputer_LinearSVR,
        # seqGlobalImputer.IterativeImputer_MLPRegressor,
        seqGlobalImputer.IterativeImputer_GaussianProcessRegressor,
        # seqGlobalImputer.IterativeImputer_PLSRegression,
        # seqGlobalImputer.IterativeImputer_IsotonicRegression,
        seqGlobalImputer.KNNImputer,
        # seqGlobalImputer.BiologicalImputer,
        # seqGlobalImputer.AlternativeImputer,
        seqGlobalImputer.NullImputer
   
        
    )

    start_time = time.perf_counter()
    # Procesar las secuencias con cada metodo de imputacion
    procesar_secuencias(n_organismos,
                        len_secuencias,
                        secuencias_codificadas,
                        rFC,
                        output_imputaciones,
                        output_arboles_estimados,
                        output_tiempos_ejecucion,
                        output_robison_foulds,
                        metodos_imputacion
                        )
    end_time = time.perf_counter()


    output_arboles_estimados.write(f"Arbol_verdad;{rFC.getArbol_nwkStr()}\n")
    # Asegurarse de cerrar los archivos al final del programa
    cerrar_flujos_escritura(output_imputaciones, output_arboles_estimados, output_tiempos_ejecucion, output_robison_foulds)
    
    print(f"  Tiempo de procesamiento del fichero {archivo_phy} (secuencial): {end_time - start_time} segundos")