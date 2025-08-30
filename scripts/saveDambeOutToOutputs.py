import argparse
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.robinsonFouldsComputer as rfc


formatoNewickDAMBE = 0
maxExample = 5

outputDir = "./Outputs/DAMBE/out_robinson_foulds/"
outputsDir = "./Outputs"

def fileDestBuilder(dataset:str, porcentaje:int, example:int, exampleMax:int):


    if porcentaje < 10:
        porcentaje = "0"+str(porcentaje) #Para que 5% sea 05% 
        
    return f"{dataset}_{porcentaje}%_example_{example}_out_of_{exampleMax}.csv"

def pathArbolEstimado(dataset:str, porcentaje:int, example:int, exampleMax:int, paralelo:bool):

    
    fileDest = fileDestBuilder(dataset, porcentaje, example, exampleMax)
   
    if paralelo:
        modo = "paralelo"
    else:
        modo = "secuencial"
    
    return f"{outputsDir}/{modo}/{dataset}/arboles_estimados/{fileDest}"

def pathOutRobinsonFoulds(dataset:str, porcentaje:int, example:int, exampleMax:int, paralelo:bool):
    
    fileDest = fileDestBuilder(dataset, porcentaje, example, exampleMax)
   
    if paralelo:
        modo = "paralelo"
    else:
        modo = "secuencial"
    
    return f"{outputsDir}/{modo}/{dataset}/out_robinson_foulds/{fileDest}"


def actualizarArbolEstimado(metodo:str, arbolEstimado:str, dataset:str, porcentaje:int, example:int, exampleMax:int, paralelo:bool):
    fileArbolEstimado = pathArbolEstimado(dataset, porcentaje, example, exampleMax, paralelo)
    fileArbolEstimado = fileArbolEstimado.replace("/", os.sep)
    if  os.path.exists(fileArbolEstimado):
        fileArbolEstimado = open(fileArbolEstimado, 'a')
        fileArbolEstimado.write(f"DAMBE_{metodo};{arbolEstimado}")
        fileArbolEstimado.close()
    else:
        print(f"El fichero {fileArbolEstimado} no existe, no se puede actualizar el arbol estimado.")
   
    
def actualizarOutRobinsonFoulds(metodo:str, rf:int, n_rf:int, dataset:str, porcentaje:int, example:int, exampleMax:int, paralelo:bool):
    fileOut = pathOutRobinsonFoulds(dataset, porcentaje, example, exampleMax, paralelo)
    fileOut = fileOut.replace("/", os.sep)
    if  os.path.exists(fileOut):
        fileOut = open(fileOut, 'a')
        fileOut.write(f"DAMBE_{metodo};{rf};{n_rf}\n")
        fileOut.close()      
    else:
        print(f"El fichero {fileOut} no existe, no se puede actualizar el out robinson foulds.")
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Leer un fichero CSV con árboles, método y conjunto.")
    parser.add_argument("csv_file", help="Ruta al fichero CSV con los árboles")
    parser.add_argument("arbol_verdad", help="Ruta al árbol verdadero")
    parser.add_argument("--paralelo", action="store_true", help="Indica si el procesamiento es paralelo")
    args = parser.parse_args()
    
    ficheroCSV = args.csv_file
    arbolVerdad = args.arbol_verdad
    paralelo = args.paralelo
    
    print(f"Procesando fichero CSV: {ficheroCSV}")
    
    csvBaseName = os.path.basename(ficheroCSV)
    Conjunto = csvBaseName.split("_")[0]
    Metodo = csvBaseName.split("_")[1].split(".")[0]
    
    outputDir = os.path.join(outputDir, Metodo, Conjunto)
    
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    fileOut = os.path.join(outputDir, f"{Conjunto}_{Metodo}_RobinsonFoulds.csv")
    outputDir = fileOut
    fileOut = open(fileOut, 'w')
    fileOut.write("File;Robinson Foulds;RF Normalizado\n")

    RFC = rfc.RobinsonFouldsComputer(arbolVerdad, format=1)
    with open(ficheroCSV, 'r') as file:
        lines = file.readlines()
        n_lines = len(lines)
        if n_lines != 50:
            print("El fichero no tiene el formato correcto, debe tener 50 líneas")
            exit(1)
        porcentaje = 5
        example = 1
        for line in lines:
            arbolEstimado = line
            arbolEstimado = arbolEstimado.replace("\n", "")
            arbolEstimado = arbolEstimado+";"
            file_field = str(porcentaje)+"%_example_"+str(example)+"_out_of_5"
            
            # print(f"Procesando {porcentaje}%_{example}_out_of_5: {arbolEstimado}")
            rf, n_rf = RFC.calcular_robinson_foulds(arbolEstimado, formatoNewickDAMBE)
            fileOut.write(f"{file_field};{rf};{n_rf}\n")
            
            
            actualizarArbolEstimado(Metodo, arbolEstimado, Conjunto, porcentaje, example, maxExample, paralelo)
            actualizarOutRobinsonFoulds(Metodo, rf, n_rf, Conjunto, porcentaje, example, maxExample, paralelo)
    
            
            example += 1
            if example % 6 == 0:
                porcentaje += 5
                example = 1
    
    fileOut.close()
    
    print(f"Resultados de RF guardados en {outputDir}")
    paralelo = "paralelos" if args.paralelo else "secuencials"
    print(f"Resultados {paralelo} actualizados para el conjunto {Conjunto}")
            
       
    