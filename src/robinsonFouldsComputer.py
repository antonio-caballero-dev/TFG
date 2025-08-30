import ete3
import argparse
import Bio.Phylo as phylo



class RobinsonFouldsComputer:
    def __init__(self, file_path, format=1):
        self.arbol = ete3.Tree(file_path, format)#cargar arbol verdadero desde archivo .nwk para usarlo en las comparaciones
        self.format=format

    def calcular_robinson_foulds(self, arbol_estimado, format=1):
        arbol_estimado = ete3.Tree(arbol_estimado, format)
        resultados = self.arbol.robinson_foulds(arbol_estimado, unrooted_trees=True)
        rf=resultados[0]
        n_rf=rf/resultados[1]
        return rf, n_rf
    
    def getArbol_nwkStr(self):
        return self.arbol.write(format=self.format)
    
    def procesarFicheroCSV(self, file_path, format=1, conjunto:str="M12x252", Metodo:str=""):
        
        porcentaje = 5 ## 5% inicial
        with open(file_path, 'r') as file:
            lines = file.readlines()
            n_lines = len(lines)
            if n_lines != 60:
                return "El fichero no tiene el formato correcto, debe tener 60 líneas"
            for num, line in enumerate(lines):
                arbol_estimado = ete3.Tree(line, format)
                rf, n_rf = self.calcular_robinson_foulds(arbol_estimado)
                if num % 5 == 0:
                    print(f"Procesando {porcentaje}%")
                    porcentaje += 5
                    numExample = (num % 5) +1
                    
                    pathSave = f"./Outputs/{conjunto}/out_robinson_foulds/{conjunto}_{porcentaje}%_example_{numExample}_out_of_5.csv"
                    with open(pathSave, 'a') as file:
                        cad = f"{Metodo},{rf},{n_rf}\n"
                        file.write(cad)
                        print(f"Guardado en {pathSave}")
        
        print(f"Proceso finalizado para el conjunto {conjunto}")
                


    
def main():
    parser = argparse.ArgumentParser(description="Calculate Robinson-Foulds distances.")
    parser.add_argument("true_tree", help="Path to the true tree file in Newick format")
    parser.add_argument("csv_file", help="Path to the CSV file with estimated trees")
    parser.add_argument("--conjunto", default="M12x252", help="Conjunto parameter")
    parser.add_argument("--metodo", default="", help="Metodo parameter")
    args = parser.parse_args()

    rf_computer = RobinsonFouldsComputer(file_path=args.true_tree, format=1)
    rf_computer.procesarFicheroCSV(file_path=args.csv_file, conjunto=args.conjunto, Metodo=args.metodo, format=0)
    

if __name__ == "__main__":
    main()
                
                    


