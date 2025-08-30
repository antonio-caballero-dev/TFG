import argparse
import os
import sys
from Bio import AlignIO

extension = {
    'FASTA': '.FASTA',
    'PHYLIP': '.phy'
}

BIO_Format = {
    'FASTA': 'fasta',
    'PHYLIP': 'phylip-relaxed'
}

if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Transforma entre formatos de secuencias')
    parser.add_argument('dir', help="Archivo de entrada")
    parser.add_argument('formatIN', help="Formato de entrada")
    parser.add_argument('formatOUT', help="Formato de salida")
    
    args = parser.parse_args()
    dir = args.dir
    dirSalida = dir
    formatIN = args.formatIN
    formatOUT = args.formatOUT
    
    extensionIN = extension.get(formatIN)
    extensionOUT = extension.get(formatOUT)
    
    bioFormatIN = BIO_Format.get(formatIN)
    bioFormatOUT = BIO_Format.get(formatOUT)
    
    for file in os.listdir(dir):
        if file.endswith(extensionIN):
            # print(f"Transformando {file} a {formatOUT}")
            aln = AlignIO.read(os.path.join(dir, file), bioFormatIN)
            AlignIO.write(aln, os.path.join(dirSalida, file.replace(extensionIN, extensionOUT)), bioFormatOUT)
            # print(f"Transformado {file} a {formatOUT}")
            print(f"Creado {file}.")
            
    

            
    print("Proceso finalizado.")