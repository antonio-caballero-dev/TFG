from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio import Phylo as phylo
import io


def generar_str_newick(phylip_string: str) -> str:
    '''
        Genera un arbol filogenetico a partir de un string en formato phylip-relaxed y lo devuelve en formato newick.
    '''
    # Carga las secuencias en la variable aln desde el string
    aln = AlignIO.read(io.StringIO(phylip_string), 'phylip-relaxed')

    # Calcular la matriz de distancias asociada
    calculator = DistanceCalculator('identity')
    distmatrix = calculator.get_distance(aln)

    # Obtener el arbol NJ
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(distmatrix)

    # Convertir el árbol a string en formato newick
    '''
        Se utiliza un StringIO para crear un archivo en memoria, en el que se escribe el árbol en formato newick.
        Luego se lee el archivo y se obtiene el string en formato newick.
    '''
    newick_str = io.StringIO()
    phylo.write(tree, newick_str, "newick")
    newick_str.seek(0)
    newick_output = newick_str.read().strip()

    return newick_output



def generar_tree_newick(phylip_string: str) -> str:
    '''
        Genera un árbol filogenético a partir de una cadena en formato phyli-relaxed y lo devuelve en formato arbol de Phylo.
    '''
    # Carga las secuencias en la variable aln desde el string
    aln = AlignIO.read(io.StringIO(phylip_string), 'phylip-relaxed')

    # Calcular la matriz de distancias asociada
    calculator = DistanceCalculator('identity')
    distmatrix = calculator.get_distance(aln)

    # Obtener el arbol NJ
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(distmatrix)

    #devolver el propio arbol
    return tree
