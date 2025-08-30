import re
import numpy as np

class CodonHandler:
    def __init__(self):
        
        
        
        ## Diccionario para dado un aminoacido, obtener los codones que lo codifican
        self.dictAminoacidos = {
            'phe': ['TTT', 'TTC'],
            'leu': ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'],
            'ile': ['ATT', 'ATC', 'ATA'],
            'met': ['ATG'],
            'val': ['GTT', 'GTC', 'GTA', 'GTG'],
            'ser': ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'],
            'pro': ['CCT', 'CCC', 'CCA', 'CCG'],
            'thr': ['ACT', 'ACC', 'ACA', 'ACG'],
            'ala': ['GCT', 'GCC', 'GCA', 'GCG'],
            'tyr': ['TAT', 'TAC'],
            'his': ['CAT', 'CAC'],
            'gln': ['CAA', 'CAG'],
            'asn': ['AAT', 'AAC'],
            'lys': ['AAA', 'AAG'],
            'asp': ['GAT', 'GAC'],
            'glu': ['GAA', 'GAG'],
            'cys': ['TGT', 'TGC'],
            'trp': ['TGG'],
            'arg': ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
            'gly': ['GGT', 'GGC', 'GGA', 'GGG'],
            'stop': ['TAA', 'TAG', 'TGA']
        }
        self.dictNucleotidoAIndex = {
            'T': 0,
            'C': 1,
            'A': 2,
            'G': 3,
            '?': None
        }

        self.dictIndexANucleotido = {
            0: 'T',
            1: 'C',
            2: 'A',
            3: 'G',
            np.nan: '?'
        }
        
        ## Mapa de aminoacidos para dado un nucleotido (XYZ), obtener el aminoacido correspondiente
        self.mapaAminoacidos = [[['' for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.fillMapaAminoacidos()

       


    
    def fillMapaAminoacidos(self):
        for amino_acid, codons in self.dictAminoacidos.items():
            for codon in codons:
                i = self.dictNucleotidoAIndex[codon[0]]
                j = self.dictNucleotidoAIndex[codon[1]]
                k = self.dictNucleotidoAIndex[codon[2]]
                self.mapaAminoacidos[i][j][k] = amino_acid

    def getAminoAcido(self, codon: str) -> str:
    
        i = self.dictNucleotidoAIndex[codon[0]]
        j = self.dictNucleotidoAIndex[codon[1]]
        k = self.dictNucleotidoAIndex[codon[2]]
        if i is None or j is None or k is None:
            return None
        return self.mapaAminoacidos[i][j][k]
    
    def getCodones(self, aminoacido: str) -> list:
        return self.dictAminoacidos.get(aminoacido, None)
    
    def aminoAcidoIndexado(self, i, j, k):
        if isinstance(i, str):
            i = self.dictNucleotidoAIndex[i]
        if isinstance(j, str):
            j = self.dictNucleotidoAIndex[j]
        if isinstance(k, str):
            k = self.dictNucleotidoAIndex[k]
        
        return self.mapaAminoacidos[i][j][k]
    
    
    def mostrarMapa(self):
        for i in range(4):
            for j in range(4):
                linea = ""
                for k in range(4):                    
                    aa = self.mapaAminoacidos[i][k][j]  
                    primerNucleotido = self.dictIndexANucleotido[i]
                    segundoNucleotido = self.dictIndexANucleotido[k]
                    tercerNucleotido = self.dictIndexANucleotido[j]
                    linea += f"{primerNucleotido}{segundoNucleotido}{tercerNucleotido}({aa})\t"
                print(linea)
            print()
    
    ## Devuelve un diccionario con los aminoacidos candidatos para un codon con un nucleotido o más desconocidos
    def getCandidatos(self, codon):
        dictCandidatos = {}
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    candidate_codon = f"{self.dictIndexANucleotido[i]}{self.dictIndexANucleotido[j]}{self.dictIndexANucleotido[k]}"
                    if re.match(codon.replace('?', '.'), candidate_codon):
                        aa = self.mapaAminoacidos[i][j][k]
                        if aa:
                            if aa in dictCandidatos:
                                dictCandidatos[aa] += 1
                            else:
                                dictCandidatos[aa] = 1

        total = sum(dictCandidatos.values())
        for aa in dictCandidatos:
            dictCandidatos[aa] /= total

        return dictCandidatos
        
        
 

 
if __name__ == "__main__":
    
    bi = CodonHandler()

    bi.mostrarMapa()

    codon = "TGG"
    aa = bi.getAminoAcido(codon)
    print(f"El aminoacido del codon {codon} es {aa}")
    aa = "leu"
    codones = bi.getCodones(aa)
    print(f"Los codones del aminoacido {aa} son {codones}")
    
    print(bi.aminoAcidoIndexado('T', 'G', 'G'))
    print(bi.aminoAcidoIndexado(0, 3, 'A'))
    
    print ("Para el codon TGA los candidatos son:")
    print(bi.getCandidatos("TGA"))
    print ("Para el codon T?A los candidatos son:")
    print(bi.getCandidatos("T?A"))
    print ("Para el codon T?? los candidatos son:")
    print(bi.getCandidatos("T??"))
    print ("Para el codon ?GA los candidatos son:")
    print(bi.getCandidatos("?GA"))
    