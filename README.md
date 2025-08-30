


<div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2em;">
    <div style="flex: 1;">
        <h1 style="font-size: 2.6em; margin-bottom: 0.2em; line-height: 1.15;">
            <b>Estudio de técnicas de Machine Learning para imputar datos perdidos<br>
            en secuencias biológicas</b>
        </h1>
    </div>
    <div style="flex: 0 0 auto; margin-left: 36px;">
        <img src="pictures/logos/logouex_transp.png" alt="Logo TFG" width="60" style="display: block;"/>
    </div>
</div>




--- 

<div align="center" style="margin-bottom: 1.5em;">
	<h1 style="margin-bottom: 0.3em;">🧩 El Problema</h1>
	<h2 style="margin-bottom: 1.2em; font-weight: 400; color: #444;">¿Por qué es importante la imputación de datos en filogenia?</h2>
	<div style="display: flex; align-items: flex-start; justify-content: center; max-width: 1100px; margin: 0 auto 2em auto;">
		<img src="pictures/filogenetica/art_5_2.jpg" alt="Filogenia" width="270" style="margin-right: 32px;"/>
		<p style="font-size: 1.13em; text-align: justify; margin: 0; max-width: 700px;">
			Los análisis computacionales en filogenia dependen de secuencias de ADN completas para reconstruir relaciones evolutivas entre organismos. Sin embargo, es frecuente que las matrices de datos contengan posiciones faltantes (<i>missing data</i>), lo que reduce la calidad de los árboles filogenéticos y afecta la robustez de las inferencias evolutivas.<br><br>
			<b>Objetivo:</b> Aplicar técnicas de Machine Learning para imputar o predecir los valores faltantes en las secuencias biológicas, mejorando así la integridad y calidad de los análisis filogenéticos.
		</p>
	</div>
	<div style="margin-top: 2em; margin-bottom: 2em;">
		<figure style="display: inline-block; margin: 0 32px;">
			<img src="pictures/secuencias_seaview/m12_verdad.png" alt="Secuencia completa del conjunto M12x252" width="490" style="display: block; margin-bottom: 8px; border-radius: 8px; box-shadow: 0 2px 8px #0001;"/>
			<figcaption style="text-align: center; font-size: 1em; margin-top: 4px; color: #444;">Secuencia completa (sin datos perdidos)</figcaption>
		</figure>
		<figure style="display: inline-block; margin: 0 32px;">
			<img src="pictures/secuencias_seaview/m12_con_35_perdida_1_de_5.png" alt="Secuencia con 35% de pérdida del conjunto M12x252" width="490" style="display: block; margin-bottom: 8px; border-radius: 8px; box-shadow: 0 2px 8px #0001;"/>
			<figcaption style="text-align: center; font-size: 1em; margin-top: 4px; color: #444;">Secuencia con 35% de datos perdidos</figcaption>
		</figure>
	</div>
</div>

<details>
	<summary><b>ℹ️ Detalles sobre los conjuntos de datos utilizados</b></summary>
	<ul>
		<li><b>M12x252</b>: 12 secuencias, 252 posiciones <sup>[1]</sup></li>
		<li><b>M40x359</b>: 40 secuencias, 359 posiciones <sup>[2]</sup></li>
		<li><b>M123x196</b>: 123 secuencias, 196 posiciones <sup>[3]</sup></li>
		<li><b>M203x302</b>: 203 secuencias, 302 posiciones <sup>[4]</sup></li>
	</ul>
    Todos los conjuntos incluyen versiones con diferentes porcentajes de datos perdidos para evaluar la robustez de los métodos de imputación.
</details>

---


<div align="center">
	<h1 style="margin-bottom: 0.5em;">🛠️ Enfoque y Métodos</h1>
	<p style="font-size:1.1em; max-width: 900px; margin: 0 auto 1.2em auto;">
		Para abordar el problema de los datos ausentes, se han implementado y comparado diferentes técnicas de imputación y reconstrucción filogenética.
	</p>
	<div style="margin-bottom: 1.2em;">
		<img src="https://img.shields.io/badge/Machine%20Learning-Bioinform%C3%A1tica-blue?style=for-the-badge" alt="ML Bioinfo"/>
		<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
		<img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn"/>
		<img src="https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="Numpy"/>
		<img src="https://img.shields.io/badge/BioPython-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="BioPython"/>
		<img src="https://img.shields.io/badge/Ete3-4E9A06?style=for-the-badge" alt="Ete3"/>
	</div>
	<ul style="display: inline-block; text-align: left; font-size: 1.08em; line-height: 1.7; margin: 0 auto 1.2em auto; padding-left: 0; list-style: none;">
		<li>🔹 <b>SimpleImputer</b></li>
		<li>🔹 <b>LinearSVR</b></li>
		<li>🔹 <b>BayesianRidge</b></li>
		<li>🔹 <b>GaussianProcessRegressor</b></li>
		<li>🔹 <b>KNeighborsRegressor</b></li>
		<li>🔹 <b>KNNImputer</b></li>
		<li>🔹 <b>DAMBE - MLCompositeTN93</b> <span style="font-size:0.95em; color:#888;">(software especializado en filogenia, sin imputación)</span></li>
	</ul>

</div>



---



## 📊 Resultados




### NRF Secuencial

| **Método**                                 | M12x252 | M40x359 | M123x196 | M203x302 | **Promedio** | **Pérdida** |
|--------------------------------------------|---------|---------|----------|----------|--------------|-------------|
| SimpleImputer (mean)                       | 0.3622  | 0.6378  | 0.9352   | 0.8461   | 0.6953       | 63.38%      |
| SimpleImputer (median)                     | 0.3289  | 0.6227  | 0.9060   | 0.8415   | 0.6748       | 58.55%      |
| SimpleImputer (most frequent)              | 0.3289  | 0.6195  | 0.9045   | 0.8397   | 0.6731       | 58.16%      |
| IterativeImputer (BayesianRidge)           | 0.1733  | 0.3405 | 0.6662   | 0.5769   | 0.4392       | 3.20%       |
| IterativeImputer (KNeighborsRegressor)     | 0.2133  | 0.4416  | 0.6445 | 0.4920   | 0.4479       | 5.23%       |
| IterativeImputer (LinearSVR)               | 0.1644 | 0.3665  | 0.6677   | 0.5038   | 0.4256   | 0.00%   |
| IterativeImputer (GaussianProcessRegressor)| 0.4778  | 0.7346  | 0.9345   | 0.9185   | 0.7663       | 80.06%      |
| KNNImputer                                 | 0.1911  | 0.4238  | 0.6607   | 0.4771 | 0.4382       | 2.95%       |
| DAMBE (MLCompositeTN93)                    | 0.4511  | 0.6914  | 0.9733   | 0.9353   | 0.7628       | 79.22%      |



### Tiempo de ejecución secuencial

| **Método**                                 | M12x252 | M40x359 | M123x196 | M203x302 | **Promedio** | **Pérdida** |
|--------------------------------------------|---------|---------|----------|----------|--------------|-------------|
| SimpleImputer (mean)                       | 0.0012  | 0.0014  | 0.0016   | 0.0022   | 0.0016       | -97.76%     |
| SimpleImputer (median)                     | 0.0014  | 0.0018  | 0.0022   | 0.0039   | 0.0023       | -96.70%     |
| SimpleImputer (most frequent)              | 0.0523  | 0.0697  | 0.0393   | 0.0600   | 0.0553       | -21.46%     |
| IterativeImputer (BayesianRidge)           | 4.1412  | 10.2118 | 7.4117   | 24.7196  | 11.6211      | 16398.48%   |
| IterativeImputer (KNeighborsRegressor)     | 0.5181  | 0.8759  | 0.5302   | 1.3882   | 0.8281       | 1075.65%    |
| IterativeImputer (LinearSVR)               | 8.1503  | 45.6914 | 54.5435  | 257.4513 | 91.4591      | 129744.99%  |
| IterativeImputer (GaussianProcessRegressor)| 0.5496  | 1.1204  | 2.4736   | 6.6919   | 2.7089       | 3745.80%    |
| KNNImputer                                 | 0.0409  | 0.0822  | 0.0566   | 0.1020   | 0.0704       | 0.00%       |

<sub>Valores en segundos. La columna "Pérdida" indica el incremento porcentual respecto al mejor método (KNNImputer).</sub>


<details>
<summary><b>ℹ️ Detalles sobre la métrica Robinson-Foulds y resultados paralelos</b></summary>

<p><b>Métrica Robinson-Foulds (NRF):</b> La calidad de los árboles filogenéticos estimados se evalúa mediante la distancia de Robinson-Foulds (RF), que mide la diferencia topológica entre dos árboles. Un valor más bajo indica mayor similitud entre el árbol estimado y el árbol de referencia. Para facilitar la comparación, los valores RF se han normalizado (NRF) dividiendo por el máximo posible para cada caso:</p>

<pre>NRF = Robinson-Foulds / Robinson-Foulds<sub>max</sub></pre>

<p><b>Referencia:</b> D. Robinson & L. Foulds, "Comparison of phylogenetic trees", Mathematical Biosciences, 53(1-2):131-147, 1981.</p>

<p><b>Nota sobre resultados paralelos:</b> Además de los resultados secuenciales mostrados, se han obtenido resultados en modo paralelo (multi-hilo) para evaluar la escalabilidad y eficiencia computacional de los métodos. Estos resultados no se incluyen aquí por motivos de espacio, pero están disponibles bajo petición o en los anexos del trabajo.</p>

</details>



### Comparativa visual: importancia de una buena imputación

La siguiente figura muestra la diferencia entre el árbol filogenético original (verdad), el obtenido tras imputar con KNNImputer y el obtenido con DAMBE (sin imputación específica). Se observa cómo una imputación adecuada permite recuperar una topología mucho más cercana a la realidad biológica.

<div align="center" style="margin-top: 24px; margin-bottom: 12px;">
	<figure style="display: inline-block; margin: 0 32px;">
		<img src="pictures/arboles_verdad/M12x252.png" alt="Árbol verdad" width="340" style="display: block; margin-bottom: 8px;"/>
		<figcaption style="text-align: center; font-size: 1em; margin-top: 4px;">Árbol original (realidad)</figcaption>
	</figure>
	<figure style="display: inline-block; margin: 0 32px;">
		<img src="pictures/arboles_verdad/M12x252_30_1_de_5_KNNImputer.png" alt="Árbol KNNImputer" width="340" style="display: block; margin-bottom: 8px;"/>
		<figcaption style="text-align: center; font-size: 1em; margin-top: 4px;">Imputación KNNImputer sobre una muestra con 30% de pérdida</figcaption>
	</figure>
	<figure style="display: inline-block; margin: 0 32px;">
		<img src="pictures/arboles_verdad/M12x252_30_1_de_5_DAMBE.png" alt="Árbol DAMBE" width="340" style="display: block; margin-bottom: 8px;"/>
		<figcaption style="text-align: center; font-size: 1em; margin-top: 4px;">DAMBE (sin imputación) sobre una muestra con 30% de pérdida</figcaption>
	</figure>
</div>


---

### Detalles sobre la métrica Robinson-Foulds y resultados paralelos

La calidad de los árboles filogenéticos estimados se evalúa mediante la distancia de Robinson-Foulds (RF), una métrica estándar que cuantifica la diferencia topológica entre dos árboles. El valor RF mide el número de particiones (biparticiones) presentes en un árbol y ausentes en el otro, y viceversa. Un valor más bajo indica mayor similitud entre el árbol estimado y el árbol de referencia ("verdad biológica"). Para facilitar la comparación, los valores RF se han normalizado (NRF) dividiendo por el máximo posible para cada caso.<br>

Referencia: D. Robinson & L. Foulds, "Comparison of phylogenetic trees", Mathematical Biosciences, 53(1-2):131-147, 1981.

<details>
<summary><b>ℹ️ Nota sobre resultados paralelos</b></summary>
Además de los resultados secuenciales mostrados, se han obtenido resultados en modo paralelo (multi-hilo) para evaluar la escalabilidad y eficiencia computacional de los métodos. Estos resultados no se incluyen aquí por motivos de espacio, pero están disponibles bajo petición o en los anexos del trabajo.
</details>


<p align="center">
	<sub>Trabajo Fin de Grado · Antonio Caballero · 2025</sub>
</p>


---

## 📚 Referencias

<ul style="font-size:1.05em; line-height:1.7; text-align:left; max-width:900px;">
	<li>[1] C. Kuiken, J. Thurmond, M. Dimitrijevic, and H. Yoon. The LANL hemorrhagic fever virus database, a new platform for analyzing biothreat viruses. <i>Nucleic Acids Research</i>, 40:D587–D592, 2012.</li>
	<li>[2] L. Quijada, H.-O. Baral, R. Jaen-Molina, M. Weiss, J. C. Pé-Castells, and E. Beltrán-Tejera. Phylogenetic and morphological circumscription of the Orbilia aurantiorubra group. <i>Phytotaxa</i>, 175(1):1–18, 2014.</li>
	<li>[3] J. Zhang, M. Chen, X. Dong, R. Lin, J. Fan, and Z. Chen. Evaluation of four commonly used DNA barcoding loci for Chinese medicinal plants of the family Schisandraceae. <i>PLoS One</i>, 10(5):e0125574, 2015.</li>
	<li>[4] C. Salgado-Salazar, A. Y. Rossman, and P. Chaverri. The genus Thelonectria (Nectriaceae, Hypocreales, Ascomycota) and closely related species with cylindrocarpon-like asexual states. <i>Fungal Diversity</i>, 80:411–455, 2016.</li>
</ul>