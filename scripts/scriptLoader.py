import subprocess

# # Ejecutar el primer script en segundo plano
# p1 = subprocess.Popen(["./scripts/parallelRun.sh", "../Datasets/Secuencias con datos perdidos/M12", "../modelTrees/M12x252.nwk", "8"])
# p1.wait()  # Espera que termine el primer script

# # Ejecutar el segundo script en segundo plano
# p2 = subprocess.Popen(["./scripts/parallelRun.sh", "../Datasets/Secuencias con datos perdidos/M40", "../modelTrees/M40x498.nwk", "8"])
# p2.wait()  # Espera que termine el segundo script

# # Ejecutar el tercer script en segundo plano
# p3 = subprocess.Popen(["./scripts/parallelRun.sh", "../Datasets/Secuencias con datos perdidos/M100", "../modelTrees/M100x498.nwk", "8"])
# p3.wait()  # Espera que termine el tercer script

# Ejecutar el cuarto script en segundo plano
p4 = subprocess.Popen(["./scripts/parallelRun.sh", "../Datasets/Secuencias con datos perdidos/M180", "../modelTrees/M180x2031.nwk", "8"])
p4.wait()  # Espera que termine el cuarto script