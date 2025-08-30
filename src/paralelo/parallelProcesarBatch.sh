#!/bin/bash

# Verificar si se proporciona el número correcto de argumentos
if [ $# -ne 2 ]; then
    echo "Uso: $0 dirInput arbolVerdad"
    exit 1
fi

dirInput="$1"
arbolVerdadPath="$2"

# Verificar si las rutas existen
if [ ! -d "$dirInput" ]; then
    echo "El directorio de entrada no existe."
    exit 1
fi

if [ ! -f "$arbolVerdadPath" ]; then
    echo "El arbol de verdad no existe."
    exit 1
fi

echo "Directorio de entrada: $dirInput"
datasetProcesado=$(basename "$dirInput")

# Usar mapfile para crear un array ordenado de archivos .phy
mapfile -t filesPhy < <(find "$dirInput" -name "*.phy" | sort)

# Mostrar lista enumerada de archivos .phy encontrados
# echo "Archivos .phy encontrados:"
# for i in "${!filesPhy[@]}"; do
#     echo "  $((i+1)). ${filesPhy[$i]}"
# done

echo "Ininciando el procesamiento de los archivos .phy"

runCommand="python3 -B ./src/paralelo/parallelProcesarPhy.py"
errolog=" 2>> ./logs/error_${datasetProcesado}_$(date +%Y%m%d).log"
nCores=8


tiempoInicio=$(date +%s.%N)


for file in "${filesPhy[@]}"; do
    echo "Processing file: $(basename "$file")"
    eval "$runCommand $file $arbolVerdadPath --nCores $nCores $errolog"
    echo "----------------------------------------"
done

# Capturar tiempo final y calcular total
tiempoFin=$(date +%s.%N)
tiempoTotal=$(echo "$tiempoFin - $tiempoInicio" | bc)

echo "Proceso finalizado."
echo "Tiempo total de procesamiento: $tiempoTotal segundos."
echo ""


fileDAMBE="./Outputs/DAMBE/arboles_estimados/MLCompositeTN93/${datasetProcesado}_MLCompositeTN93.csv"
if [ ! -f "$fileDAMBE" ]; then
    echo "El archivo DAMBE no existe. Asegúrate de que el procesamiento se haya completado correctamente."
else
    echo "El archivo de resultados DAMBE existe. Añadiendo resultados..."
    # Añadir resultados DAMBE
    runCommand="python3 -B ./scripts/saveDambeOutToOutputs.py $fileDAMBE ./modelTrees/${datasetProcesado}.nwk --paralelo"
    eval "$runCommand"
    echo "Resultados DAMBE añadidos."
    
fi

echo ""
echo "Calculando resultados promedio..."
runCommand="python3 -B ./scripts/calcularResultados.py"
dirResults="./Outputs/paralelo/${datasetProcesado}"

eval "$runCommand $dirResults"
echo "Resultados promedio calculados."
echo "----------------------------------------"



