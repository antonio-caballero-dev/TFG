#!/bin/bash

# Script para renombrar archivos con porcentajes de un solo dígito añadiendo ceros delante
# Ejemplo: "M12x252_5%_example_1_out_of_5.phy" a "M12x252_05%_example_1_out_of_5.phy"

# Directorio a procesar (por defecto es el directorio actual)
DIR="${1:-.}"

# Verificar si el directorio existe
if [ ! -d "$DIR" ]; then
    echo "Error: El directorio '$DIR' no existe."
    exit 1
fi

echo "Buscando archivos para renombrar en $DIR..."
count=0

# Buscar y renombrar archivos
for file in "$DIR"/*; do
    # Omitir si no es un archivo
    [ -f "$file" ] || continue
    
    filename=$(basename "$file")
    
    # Buscar patrón de porcentaje de un solo dígito (_X%_)
    if [[ $filename =~ _([0-9])%_ ]]; then
        digit="${BASH_REMATCH[1]}"
        newname="${filename/_${digit}%_/_0${digit}%_}"
        
        # Renombrar el archivo
        mv "$file" "$DIR/$newname"
        echo "Renombrado: $filename → $newname"
        ((count++))
    fi
done

echo "Renombrado completo. Se renombraron $count archivo(s)."