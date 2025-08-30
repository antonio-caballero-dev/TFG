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

runCommand="python3 -B ./src/secuencial/seqProcesarPhy.py"
errolog=" 2>> ./logs/error_${datasetProcesado}_$(date +%Y%m%d).log"

# Crear el archivo de control si no existe
auxOutFile="./Outputs/aux_out.txt"
if [ ! -f "$auxOutFile" ]; then
    touch "$auxOutFile"
fi

# Capturar tiempo de inicio
tiempoInicio=$(date +%s.%N)

# Procesar cada archivo usando correctamente el array
for file in "${filesPhy[@]}"; do
    fileName=$(basename "$file")
    
    # Verificar si el archivo ya ha sido procesado
    if grep -Fxq "$fileName" "$auxOutFile"; then
        echo "Skipping file: $fileName (already processed)"
        continue
    fi
    
    echo "Processing file: $fileName"
    eval "$runCommand $file $arbolVerdadPath $errolog"
    
    # Si el comando se ejecutó exitosamente, añadir el archivo al control
    if [ $? -eq 0 ]; then
        echo "$fileName" >> "$auxOutFile"
        echo "File $fileName added to processed list"
    else
        echo "Error processing $fileName - not added to processed list"
    fi
    
    echo "----------------------------------"
done

# Capturar tiempo final y calcular total
tiempoFin=$(date +%s.%N)
tiempoTotal=$(echo "$tiempoFin - $tiempoInicio" | bc)

echo "Proceso finalizado."
echo "Tiempo total de procesamiento: $tiempoTotal segundos."
echo

fileDAMBE="./Outputs/DAMBE/arboles_estimados/MLCompositeTN93/${datasetProcesado}_MLCompositeTN93.csv"
if [ ! -f "$fileDAMBE" ]; then
    echo "El archivo DAMBE no existe. Asegúrate de que el procesamiento se haya completado correctamente."
else
    echo "El archivo de resultados DAMBE existe. Añadiendo resultados..."
    # Añadir resultados DAMBE
    runCommand="python3 -B ./scripts/saveDambeOutToOutputs.py $fileDAMBE ./modelTrees/${datasetProcesado}.nwk"
    eval "$runCommand"
    echo "Resultados DAMBE añadidos."
fi

echo
echo "Calculando resultados promedio..."
runCommand="python3 -B ./scripts/calcularResultados.py"
dirResults="./Outputs/secuencial/${datasetProcesado}"

eval "$runCommand $dirResults"
echo "Resultados promedio calculados."
echo "----------------------------------------"
