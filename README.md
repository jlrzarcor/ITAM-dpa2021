# Proyecto - *Data Product Architecture* (Primavera 2021)

<p align = "center">
    <img src="images/logo_itam.png" width="300" height="110" />


---

### Maestría en Ciencia de Datos

### M. Sc. Liliana Millán Núñez

### Equipo 5

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
  * Se debe precisar que el **01/07/2018 se realizaron modificaciones** a los procedimientos de inspección que afectan a los datos. Estructuralmente el *dataset* no será afectado. No obstante, la columna **_"Violations"_**, si bien aún contiene el número de violación, descripción y comentarios delimitando violaciones independientes con el "*pipe character*", las violaciones actuales se modificaron substancialmente. Debemos ser cuidadosos al analizar los datos en los posibles cambios de tendencia en el largo plazo.
Para consultar las modificaciones: [***Food Inspection Violations Changes***](http://bit.ly/2yWd2JB).
  * En adición, encontramos la modificación a los siguientes términos (**validar en la información**) [_2019 Chicago Food Code Major Changes_](https://www.cityofchicago.org/city/en/depts/cdph/provdrs/healthy_restaurants/svcs/food-protection-services.html.):
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

---

**¿Qué lenguaje utlizamos?**

El proyecto es desarrollado utilizando como lenguaje principal `Python 3.7.4`.

---

***Summary*** de los datos con los que trabajamos (hasta el día 16 de enero de 2021) para el ***Checkpoint 1***:

- **Número de registros**: 215,130.

- **Número de columnas**: 17.

- **Variables con las que contamos inicialmente**:

**Variable**                 | **Tipo de dato**     | **¿Qué contiene?**
-----------------------------| ---------------------| ------------------------------------------------------------------------------------
*Inspection ID*.             | Número.              | *ID* correspondiente a la inspección.
*DBA Name*.                  | Texto.               | _'Doing business as'_ Nombre legal del establecimiento.
*AKA Name*.                  | Texto.               | _'Also known as'_ Nombre público como se conoce al establecimiento.
*Licence*.                   | Número.              | Número único asignado al establecimiento con fines de licenciamiento.
*Facility Type*.             | Texto.               | Cada establecimiento se etiqueta con alguno de los siguientes: *bakery, banquet hall, candy store, caterer, coffee shop, day care center (for ages less than 2), day care center (for ages 2 – 6), day care center (combo, for ages less than 2 and 2 – 6 combined), gas station, Golden Diner, grocery store, hospital, long term care center(nursing home), liquor store, mobile food dispenser, restaurant, paleteria, school,shelter, tavern, social club, wholesaler, or Wrigley Field Rooftop*.
*Risk*.                      | Texto.               | Cada establecimiento se categoriza de acuerdo al riesgo de afectar la salud pública. 1 el más alto riesgo y 3 el menor. La frecuencia de las inspecciones está ligada a su nivel de riesgo.
*Address, City, State, Zip*. | Texto.               | Dirección completa donde se localizan las instalaciones.
*Inspection Date*.           | *Floating Timestamp*.| Fecha de la inspección.
*Inspection Type*.           | Texto.               | Tipo de inspección, puede ser cualquiera de las siguientes: _canvass_, el tipo de inspección más común realizado con una frecuencia relativa al **riesgo del establecimiento**; _consultation_, es cuando la inspección se realiza por requerimiento del dueño previo a la apertura del establecimiento; _complaint_, se realiza una inspección en respuesta a una queja en contra del establecimiento; _license_, se realiza cuando el establecimiento lo requiere para recibir su lecencia para operar; _suspect food poisoning_, se realiza en respuesta a una o más presonas que presubmiblemente hayan engermado como resultado de haber comiedo en el establecimiento; _task-force inspection_, cuando la inspección se realiza a un bar o taverna.
*Results*.                   | Texto.               | _Pass, pass with conditions, fail, out of business or not located_; '_pass_' implica que no se tienen violaciones críticas o severas (códigos de violación 1-14 y 15-29 respectivamente). '_pass with conditions_', se encontraton violaciones críticas o severas, pero fueron corregidas durante la inspección. '_fail_' implica que se tienen violaciones críticas o severas y que no se corrigieron durante la inspección.
*Violations*.                | Texto.               |  Un establecimiento puede recibir más de una de las 45 distintas violaciones (código de violación 1 al 44 y 70). Pensar en como analizar esta variable.
*Latitude*.                  | Número.              | Latitud del negocio.
*Longitude*.                 | Número.              | Longitud del negocio.
*Location*.                  | *Location*.          | Contiene la coordenada (longitud y latitud) del negocio.

---

### Lo que buscamos

- **Pregunta analítica a contestar con el modelo predictivo**: `¿El establecimiento pasará o no la inspección?`

### Tomar en cuenta

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

---
## ¿Cómo reproducir los resultados de este repositorio?

Si usted desea reproducir los resultados mostrados en este trabajo, lo que tiene que hacer es lo siguiente:

1. Clonar el repositorio en la dirección de su agrado dentro de su computadora con el comando: `git clone <url del repositorio> <nombre que desea poner al repositorio dentro de su sistema>`.

**PARA RPRODUCIR LOS RESULTADOS DE NUESTRO** ***EDA***:

2. Descargar el csv de esta [url](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5) y colocarlo en la ruta: `/notebooks/eda`.

3. **Opcional, requiere pyenv:** Genera el ambiente virtual para este proyecto con el comando `pyenv virtualenv 3.7.4 nombre_de_tu_environment`.

  Activa el ambiente virtual con el siguiente comando: `pyenv activate nombre_de_tu_environment`

  --> instalar ipykernel<br>
  `pip install ipykernel`

  --> hacer accesible el ambiente virtual al notebook de jupyter<br>
  `python -m ipykernel install --user --name nombre_de_tu_environment --display-name nombre_de_tu_environment`
  
**CÓMO INSTALAR NUESTRO** ***requirements***.**txt**:

4. Instalar el `requirements.txt` que se encuentra en el mismo directorio de este archivo `README.md` con el comando: `pip install -r requirements.txt`

5. Abre tu terminal y desde ella entra al directorio raíz de este archivo.

6. Corre el comando `jupyter notebook` (asegúrate de tener activo tu environment).

7. Abre el archivo `EDA_GEDA_Checkpoint1.ipynb` y ya podrás operarlo sin problemas.

## Sobre nuestro ***EDA***:
- En la ruta `notebooks/eda/EDA_GEDA_Checkpoint1.ipynb` encontrarás el notebook que contiene los resultados encontrados en el primer *checkpoint*** del proyecto.
- En la ruta `notebooks/eda/Food_Inspections.csv` deberá ser el archivo que descargaste de la liga mencionada anteriormente para poder utilizarse con el *notebook* de nuestro *EDA*.

---

### Resumen de cómo funciona nuestro proceso de ingestión
