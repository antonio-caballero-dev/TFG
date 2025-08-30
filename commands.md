# Manual de Ejecución

> **Nota:** Ejecutar todos los comandos desde el directorio `/workspace`.

---

## Tabla de Contenidos

1. [Generar Árboles de Verdad](#generar-árboles-de-verdad)
2. [Procesar un Fichero Secuencial](#procesar-un-fichero-secuencial)
3. [Procesar un Fichero en Paralelo (8 Cores)](#procesar-un-fichero-en-paralelo-8-cores)
4. [Calcular Robinson-Foulds para DAMBE](#calcular-robinson-foulds-para-dambe)
5. [Procesar un Batch (Secuencial)](#procesar-un-batch-secuencial)
6. [Procesar un Batch (Paralelo)](#procesar-un-batch-paralelo)
7. [Añadir Resultados DAMBE](#añadir-resultados-dambe)
8. [Traducir a FASTA](#traducir-a-fasta)

---

### 1. Generar Árboles de Verdad

Ejecuta el siguiente comando para generar los árboles de verdad:

```bash
python3 -B ./scripts/generarArbolesVerdad.py ../Datasets/Secuencias\ verdad/
```

---

### 2. Procesar un Fichero Secuencial

Para procesar un fichero de forma secuencial, utiliza:

```bash
python3 -B ./src/secuencial/seqProcesarPhy.py ../Datasets/missing/M180/M180x2031_10%_example_1_out_of_5.phy ./modelTrees/M180x2031.nwk 2>> "./logs/log$(date).log"
```

---

### 3. Procesar un Fichero en Paralelo (8 Cores)

Para procesar un fichero utilizando 8 núcleos, ejecuta:

```bash
python3 -B ./src/paralelo/parallelProcesarPhy.py ../Datasets/missing/M180/M180x2031_10%_example_1_out_of_5.phy ./modelTrees/M180x2031.nwk --nCores 8 2>> "./logs/log$(date).log"
```

---

### 4. Calcular Robinson-Foulds para DAMBE

Calcula la métrica Robinson-Foulds para DAMBE con el siguiente comando:

```bash
python3 -B ./scripts/saveDambeOutToOutputs.py ./Outputs/DAMBE/EstimatedTrees/M12x252_MLCompositeTN93_trees.csv ../modelTrees/M12x252.nwk
```

---

### 5. Procesar un Batch (Secuencial)

Para procesar todos los archivos `.phy` de un directorio de forma secuencial:

```bash
./src/secuencial/seqProcesarBatch.sh ./dataset/Perdidos/M12x252/ ./modelTrees/M12x252.nwk 
```

---

### 6. Procesar un Batch (Paralelo)

Para procesar todos los archivos `.phy` de un directorio en paralelo (8 chunks):

```bash
./src/paralelo/parallelProcesarBatch.sh ./dataset/Perdidos/M12x252 ./modelTrees/M12x252.nwk
```

---

### 7. Añadir Resultados DAMBE

Para añadir los resultados de DAMBE a los outputs:

```bash
python3 -B ./scripts/saveDambeOutToOutputs.py ./Outputs/DAMBE/arboles_estimados/MLCompositeTN93/M12x252_MLCompositeTN93.csv ./modelTrees/M12x252.nwk
```

---

### 8. Traducir a FASTA

Para convertir archivos de PHYLIP a FASTA:

```bash
python3 ./scripts/sequenceFormat.py ./dataset/Perdidos/M40x359 PHYLIP FASTA
```

---
