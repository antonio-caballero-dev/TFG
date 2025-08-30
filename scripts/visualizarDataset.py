
import os
import argparse

from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo as phylo

import matplotlib.pyplot as plt

colors = {
    'A': 'red',
    'C': 'blue',
    'G': 'green',
    'T': 'yellow',
    '?': 'gray'
}

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Genera un arbol filogenetico a partir de un archivo .phy')
    parser.add_argument('file', help="Ruta al archivo .phy")
    
    args = parser.parse_args()
    file = args.file
    
    if not file.endswith('.phy'):
        print("El archivo debe ser de formato .phy")
        
    conjunto = AlignIO.read(file, "phylip-relaxed")
    print("El conjunto de datos tiene {} secuencias y {} posiciones".format(len(conjunto), len(conjunto[0])))
    
    etiquetas = [str(seq.id) for seq in conjunto]
    secuencias = [str(seq.seq) for seq in conjunto]
    
    for etiqueta, secuencia in zip(etiquetas, secuencias):
        print(f"{etiqueta}: {secuencia}")
    
   