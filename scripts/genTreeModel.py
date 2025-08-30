# Descripcion: Genera un arbol filogenetico a partir de un archivo .phy
# Uso: python3 genTreeModel.py -f <archivo.phy> -o <directorio_salida> 

import os
import argparse
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo as phylo

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Genera un arbol filogenetico a partir de un archivo .phy')
    parser.add_argument('file', help="Ruta al archivo .phy")
    parser.add_argument('output', help="Directorio de salida")
    
    args = parser.parse_args()
    file = args.file
    pathWrite = args.output
    
    if not file.endswith('.phy'):
        print("El archivo debe ser de formato .phy")
        exit(1)
        
    if not os.path.exists(pathWrite):
        print("El directorio de salida no existe.")
        exit(1)

    # print(f"Generando arbol para el archivo {file}")

    # Carga las secuencias en la variable aln
    aln = AlignIO.read(file, 'phylip-relaxed')

    # Calcular la matriz de distancias asociada
    calculator = DistanceCalculator('identity')
    distmatrix = calculator.get_distance(aln)

    # Obtener el arbol NJ
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(distmatrix)

    output_file = os.path.basename(file).replace('.phy', '.nwk')
    phylo.write(trees=tree, file=os.path.join(pathWrite, output_file), format="newick") # Guardar el arbol en un archivo .nwk
    # print(f"Arbol generado en {os.path.join(pathWrite, output_file)}.")


