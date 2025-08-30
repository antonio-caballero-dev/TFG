import os
import argparse
from ete3 import Tree, TreeStyle
import Bio.Phylo as phylo

dirOutput = "./Outputs/TreeImages"

def mostrar_arbol(fichero):
    arbol = phylo.read(fichero, "newick")
    phylo.draw_ascii(arbol)
    
def mostrar_arbol_ete3(fichero, format=1):
    fileName = os.path.basename(fichero)
    fileName = fileName.replace(".nwk", "")
    arbol = Tree(fichero, format)
    # arbol.show()
    if not os.path.exists(dirOutput):
        os.makedirs(dirOutput)
    print(f"Generando imagen del árbol filogenético en {dirOutput}/{fileName}.png")
    arbol.render(f"{dirOutput}/{fileName}.png", w=1920, units="px")

def main():
    parser = argparse.ArgumentParser(description='Visualizar un árbol filogenético.')
    parser.add_argument('fichero', type=str, help='Ruta al fichero .nwk')
    args = parser.parse_args()

    fichero = args.fichero

    if not fichero.endswith('.nwk'):
        print(f"Error: El fichero '{fichero}' no tiene la extensión '.nwk'.")
    else:
        # mostrar_arbol(fichero)
        # phylo.draw(phylo.read(fichero, "newick"))
        
        # Mostrar el árbol usando ete3
        mostrar_arbol_ete3(fichero)

if __name__ == "__main__":
    main()
    

