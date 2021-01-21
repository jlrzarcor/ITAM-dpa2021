# Proyecto - *Data Product Architecture* (Primavera 2021)

<p align = "center">
    <img src="images/logo_itam.png" width="300" height="110" />


---

### M. Sc. Liliana Millán Núñez

Integrante | Alumno                         | Clave única
---------- | ------------------------------ | -----------
1          | Carlos Román López Sierra      | 197911
2          | José Luis Zárate               |
1          | Octavio Fuentes Ortiz          | 150792
2          | Patricia Urriza Arellano       | 152026
3          | Uriel Abraham Rangel Díaz      | 193921

---

## Acerca de este proyecto

Trabajaremos con la base de datos de [***Chicago Food Inspections***](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5).

![](./images/chicago_summary.png)

---

El trabajo será desarrollado a lo largo del semestre y será dividido en los siguientes ***Checkpoints***:

- *Checkpoint* 1:  *Starting point*.

**NOTA**: Para el *checkpoint* 1, los datos los descargamos el sábado 16 de enero.

- *Checkpoint* 2:  Ingestión y almacenamiento.
- *Checkpoint* 3:  Pre-procesamiento y limpieza.
- *Checkpoint* 4:  *Feature engineering*.
- *Checkpoint* 5:  Entrenamiento.
- *Checkpoint* 6:  *Bias & Fairness*.
- *Checkpoint* 7:  Predicción.
- *Checkpoint* 8:  Interpretabilidad.
- *Checkpoint* 9:  *API*. 
- *Checkpoint* 10: *Dashboard*.

El proyecto es desarrollado utilizando como lenguaje principal `Python 3.7.4`.

---

***Summary*** de los datos con los que trabajamos:

- **Número de registros**: 215,130.

- **Número de columnas**: 17.

- **Variables con las que contamos**:

**Variable**            | **Tipo de dato**     | **¿Qué contiene?**
------------------------| ---------------------| ------------------------------------------------------------------------------------
*Inspection ID*.        | Número.              | *ID* correspondiente a la inspección.
*DBA Name*.             | Texto.               | Nombre bajo el que el negocio opera.
*AKA Name*.             | Texto.               | Nombre del negocio o un nombre distinto con el que taambién se le conoce al negocio.
*Licence*.              | Número.              | El número de licencia.
*Facility Type*.        | Texto.               | Tipo de negocio.
*Risk*.                 | Texto.               | Tres tipos de riesgo: 1-riesgo alto, 2-riesgo medio y 3-riesgo bajo.
*Address*.              | Texto.               | Dirección del negocio.
*City*.                 | Texto.               | Ciudad donde se encuentra el negocio.
*State*.                | Texto.               | Estado donde se encuentra el negocio.
*Zip*.                  | Número.              | Código postal del negocio.
*Inspection Date*.      | *Floating Timestamp*.| Fecha de la inspección.
*Inspection Type*.      | Texto.               | Tipo de inspección realizada al negocio.
*Results*.              | Texto.               | Resultados de la inspección.
*Violations*.           | Texto.               | Violaciones cometidas por el negocio.
*Latitude*.             | Número.              | Latitud del negocio.
*Longitude*.            | Número.              | Longitud del negocio.
*Location*.             | *Location*.          | Contiene la coordenada (longitud y latitud) del negocio.

- **Pregunta analítica a contestar con el modelo predictivo**: ¿El establecimiento pasará o no la inspección?

- **Frecuencia de actualización de los datos**: diaria.

- **Frecuencia de actualización del producto de datos**: semanal.

---

## Estructura básica del proyecto

```
├── README.md          <- The top-level README for developers using this project.
├── conf
│   ├── base           <- Space for shared configurations like parameters.
│   └── local          <- Space for local configurations, usually credentials.
│
├── docs               <- Space for Sphinx documentation.
│
├── notebooks          <- Jupyter notebooks.
│   └── eda
│
├── images             <- Contains images used in the repository.
│
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── results            <- Intermediate analysis as HTML, PDF, LaTeX, etc.
│
├── requirements.txt   <- The requirements file.
│
├── .gitignore         <- Avoids uploading data, credentials, outputs, system files etc.
│
├── infrastructure
├── sql
├── setup.py
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module.
    │
    ├── utils      <- Functions used across the project.
    │
    │
    ├── etl       <- Scripts to transform data from raw to intermediate.
    │
    │
    ├── pipeline
```
