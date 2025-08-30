import os
import argparse

if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Genera arboles filogeneticos a partir de archivos .phy de un directorio especifico')
    parser.add_argument('dirInput', help="Directorio de entrada")
    
    args = parser.parse_args()
    dirInput = args.dirInput
    dirOutput = "./modelTrees"
    
    print(f"Directorio de entrada: {dirInput}")
    print(f"Directorio de salida: {dirOutput}")
    
    if not os.path.exists(dirInput):
        print("El directorio de entrada no existe.")
        exit(1)
        
    if not os.path.exists(dirOutput):
        print("El directorio de salida no existe. Creando el directorio...")
        os.makedirs(dirOutput)
        
    for file in os.listdir(dirInput):
        if file.endswith('.phy'):
            os.system(f"python3 ./scripts/genTreeModel.py \"{os.path.join(dirInput, file)}\" \"{dirOutput}\"")
            print(f"Arbol generado para el archivo {file}.")
            
    print("Proceso finalizado.")