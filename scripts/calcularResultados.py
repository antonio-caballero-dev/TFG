import argparse
import os
import numpy as np



parser = argparse.ArgumentParser(description="Procesar resultados de imputacion")
parser.add_argument("dir", help="Ruta al directorio con los archivos de resultados")
args = parser.parse_args()

directorio = args.dir
if not os.path.isdir(directorio):
    print(f"El directorio {directorio} no existe")
    exit()

subdirs = ["arboles_estimados", "imputaciones", "out_robinson_foulds", "tiempos_ejecucion"]
missing_subdirs = [subdir for subdir in subdirs if not os.path.isdir(os.path.join(directorio, subdir))]

if missing_subdirs:
    print(f"Faltan los siguientes subdirectorios: {', '.join(missing_subdirs)}")
    exit()

# Para todos los archivos en directorio/tiempos_ejecucion/ calcular la media de tiempos para cada método y cada %
print(f"Procesando outputs del conjunto: {directorio.split('/')[3]} en {directorio.split('/')[2]}")

tiempos_dir = os.path.join(directorio, "tiempos_ejecucion")
print(f"Ruta de outputs de tiempos de ejecucion: {tiempos_dir}")

conjunto = directorio.split('/')[2]

print("Calculando medias de tiempos de ejecucion para cada metodo y porcentaje de faltantes...")
metodosSumas = {}

for file in os.listdir(tiempos_dir):
    #print(f"Procesando archivo {file}")
    porcentaje = int(file.split('_')[1].replace('%', '')) 
    with open(os.path.join(tiempos_dir, file), "r") as f:
        lineas = f.readlines()
        lineas = lineas[1:]
        lineas = [linea.strip().split(';') for linea in lineas]
                
        for metodo, tiempo in lineas:
            tiempo = float(tiempo.replace(',', '.'))
            # print(f"{metodo};{tiempo}")
            if metodo not in metodosSumas:
                metodosSumas[metodo] = {porcentaje: [tiempo]}
            else:
                if porcentaje not in metodosSumas[metodo]:
                    metodosSumas[metodo][porcentaje] = [tiempo]
                else:
                    metodosSumas[metodo][porcentaje].append(tiempo)
            
# print(metodosSumas)

metodosMedias = {}

for metodo, porcentajes in metodosSumas.items():
    metodosMedias[metodo] = {}
    for porcentaje, tiempos in porcentajes.items():
        metodosMedias[metodo][porcentaje] = np.mean(tiempos)
        
# print(metodosMedias)

ficheroMediaTiempos = os.path.join(directorio, "media_tiempos.csv")

with open(ficheroMediaTiempos, "w") as f:
    
    cabecera = "Nombre_metodo"
    primerImputer= list(metodosMedias.keys())[0]
    listaPorcentajes = list(metodosMedias[primerImputer].keys())
    listaPorcentajes = sorted(listaPorcentajes)
    for porcentaje in listaPorcentajes:
        cabecera += f";{porcentaje}%"
    cabecera += ";media_global\n"
    f.write(cabecera)

    for metodo in metodosMedias:
        f.write(f"{metodo}")
        mediaMetodo=0.0
        for porcentaje in listaPorcentajes:
            if porcentaje in metodosMedias[metodo]:
                f.write(f";{str(metodosMedias[metodo][porcentaje]).replace('.', ',')}")
                mediaMetodo+=float(metodosMedias[metodo][porcentaje].item())
            else:
                f.write(";N/A")
        mediaMetodo=float(mediaMetodo/len(listaPorcentajes))
        mediaMetodo=str(mediaMetodo)
        f.write(f";{mediaMetodo.replace('.',',')}\n")
print("Hecho.")
print(f"Fichero guardado: {ficheroMediaTiempos}")
print()
        

#Ahora se calcula la media de los RF para cada metodo y porcentaje de faltantes       
robinson_foulds_dir = os.path.join(directorio, "out_robinson_foulds")
print(f"Ruta de outputs de Robinson Foulds: {robinson_foulds_dir}")

print("Calculando medias de Robinson Foulds para cada metodo y porcentaje de faltantes...")
metodosSumas = {}

for file in os.listdir(robinson_foulds_dir):
    #print(f"Procesando archivo {file}")
    porcentaje = int(file.split('_')[1].replace('%', '')) 
    with open(os.path.join(robinson_foulds_dir, file), "r") as f:
        lineas = f.readlines()
        lineas = lineas[1:]
        lineas = [linea.strip().split(';') for linea in lineas]
                
        for metodo, rf, rf_norm in lineas:
            
            rf_norm = float(rf_norm.replace(',', '.'))
            # print(f"{metodo};{tiempo}")
            if metodo not in metodosSumas:
                metodosSumas[metodo] = {porcentaje: [(rf_norm)]}
            else:
                if porcentaje not in metodosSumas[metodo]:
                    metodosSumas[metodo][porcentaje] = [(rf_norm)]
                else:
                    metodosSumas[metodo][porcentaje].append((rf_norm))

# print(metodosSumas)

metodosMedias = {}

for metodo, porcentajes in metodosSumas.items():
    metodosMedias[metodo] = {}
    for porcentaje, rfs in porcentajes.items():
        metodosMedias[metodo][porcentaje] = np.mean(rfs)

# print(metodosMedias)

ficheroMediaRF = os.path.join(directorio, "media_robinson.csv")

with open(ficheroMediaRF, "w") as f:
        
    cabecera = "Nombre_metodo"
    primerImputer= list(metodosMedias.keys())[0]
    listaPorcentajes = list(metodosMedias[primerImputer].keys())
    listaPorcentajes = sorted(listaPorcentajes)
    for porcentaje in listaPorcentajes:
        cabecera += f";{porcentaje}%"
    cabecera += ";media_global\n"
    f.write(cabecera)

    for metodo in metodosMedias:
        f.write(f"{metodo}")
        mediaMetodo=0.0
        for porcentaje in listaPorcentajes:
            if porcentaje in metodosMedias[metodo]:
                f.write(f";{str(metodosMedias[metodo][porcentaje]).replace('.', ',')}")
                mediaMetodo+=float(metodosMedias[metodo][porcentaje].item())
            else:
                f.write(";N/A")
        mediaMetodo=float(mediaMetodo/len(listaPorcentajes))
        mediaMetodo=str(mediaMetodo)
        f.write(f";{mediaMetodo.replace('.',',')}\n")


print("Hecho.")
print(f"Fichero guardado: {ficheroMediaRF}")


            

            
   
        


