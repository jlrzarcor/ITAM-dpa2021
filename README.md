# Proyecto - *Data Product Architecture* (Primavera 2021)

<p align = "center">
    <img src="images/logo_itam.png" width="300" height="110" />


---

### M. Sc. Liliana Millán Núñez

Integrante | Alumno                         | Clave única
---------- | ------------------------------ | -----------
1          | Carlos Román López Sierra      | 197911
2          | José Luis Zárate Cortés        | 183347
3          | Octavio Fuentes Ortiz          | 150792
4          | Patricia Urriza Arellano       | 152026
5          | Uriel Abraham Rangel Díaz      | 193921

---

## Acerca de este proyecto

Trabajaremos con la base de datos de [***Chicago Food Inspections***](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5).

![](./images/chicago_summary.jpg)

#### Conocimiento a priori de la información:
* **_Title:_** *Food Inspections*

* **_Descripción:_**  
  * La información se obtiene de las inspecciones de restaurantes y otros establecimientos de comida en Chicago desde 01/01/2010 hasta la actualidad.
  * Las inspecciones se realizan por personal del ***Chicago Department of Public Health’s Food Protection Program*** siguiendo un procedimiento estandarizado.
  * Se debe precisar que e1 **01/07/2018 se realizaron modificaciones** a los procedimientos de inspección que afectan a los datos. Estructuralmente el *dataset* no será afectado. No obstante, la columna **"Violations"**, si bien aún contiene el número de violación, descripción y comentarios delimitando violaciones independientes con el "*pipe character*", las violaciones actuales se modificaron substancialmente. Debemos ser cuidadosos al analizar los datos en los posibles cambios de tendencia en el largo plazo.
Para consultar las modificaciones: [***Food Inspection Violations Changes***](http://bit.ly/2yWd2JB).
  * En adición, encontramos la modificación a los siguientes términos (**validar en la información**) [2019 Chicago Food Code Major Changes ](https://www.cityofchicago.org/city/en/depts/cdph/provdrs/healthy_restaurants/svcs/food-protection-services.html.):
     * _Potentially Hazardous Foods (PHF)" has been changed to “Time/Temperature Control for Safety Foods (TCS Foods)_"
     * "_Critical Violation" has been changed to “Priority (P) Violation_"
     * "_Serious Violation" has been changed to "Priority Foundation (PF)Violation_"
     * "_Minor Violation" has been changed to "Core (C) Violation_"
     * "_Corrected During Inspection (CDI)" has been changed to "Corrected on Site (COS)_"

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

***Summary*** de los datos con los que trabajamos (hasta el día 16 de enero de 2021):

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

- **Pregunta analítica a contestar con el modelo predictivo**: `¿El establecimiento pasará o no la inspección?`

- **Frecuencia de actualización de los datos**: `diaria`.

- **Frecuencia de actualización del producto de datos**: `semanal`.

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
