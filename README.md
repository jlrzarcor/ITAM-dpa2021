# Proyecto - *Data Product Architecture* (Primavera 2021)

<p align = "center">
    <img src="images/logo_itam.png" width="300" height="110" />

---

### Maestría en Ciencia de Datos

### M. Sc. Liliana Millán Núñez

### Equipo 5

##

<center>
Integrante | Alumno                         | Clave única
---------- | ------------------------------ | -----------
1          | Carlos Román López Sierra      | 197911
2          | José Luis Zárate Cortés        | 183347
3          | Octavio Fuentes Ortiz          | 150792
4          | Patricia Urriza Arellano       | 152026
5          | Uriel Abraham Rangel Díaz      | 193921
</center>

---

## Acerca de este proyecto

![](./images/cdp.png)

Trabajamos con la base de datos de [***Chicago Food Inspections***](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5).

![](./images/chicago_summary.jpg)

#### Conocimiento a priori de la información:
* **_Title:_** *Food Inspections*

* **Descripción:**  
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

## ¿Cómo está dividido nuestro proyecto?

El proyecto será desarrollado a lo largo del semestre y será dividido en los siguientes ***Checkpoints***:

![Checkpoint_Actual](https://img.shields.io/badge/Checkpoint%20actual-3-brightgreen)
![Entrega](https://img.shields.io/badge/Fecha%20de%20entrega-18%2F03%2F2021-brightgreen)
![Proximo](https://img.shields.io/badge/Pr%C3%B3ximo%20checkpoint-4-yellow)
![Restantes](https://img.shields.io/badge/Checkpoints%20restantes-7-red)

- :white_check_mark:  *Checkpoint* 1:  *Starting point*.

<sup><sub>**NOTA**: Para el *checkpoint* 1, los datos los descargamos el sábado 16 de enero.</sup></sub>

- :white_check_mark:  *Checkpoint* 2:  Ingestión y almacenamiento.
- :soon:  *Checkpoint* 3:  Pre-procesamiento y limpieza.
- :yellow_circle:  *Checkpoint* 4:  *Feature engineering*.
- :red_circle:  *Checkpoint* 5:  Entrenamiento.
- :red_circle:  *Checkpoint* 6:  *Bias & Fairness*.
- :red_circle:  *Checkpoint* 7:  Predicción.
- :red_circle:  *Checkpoint* 8:  Interpretabilidad.
- :red_circle:  *Checkpoint* 9:  *API*. 
- :red_circle:  *Checkpoint* 10: *Dashboard*.

---

## ¿Qué lenguaje utlizamos?

![Lenguaje_utilizado](https://img.shields.io/badge/Python-3.7.4-informational/?logo=Python)

[***Python.org***](https://www.python.org/)

![](./images/python-logo.png)

---

***Summary*** de los datos con los que trabajamos (hasta el día 16 de enero de 2021) para el ***Checkpoint 1***:

![Registros](https://img.shields.io/badge/N%C3%BAmero%20de%20registros-215%2C130-important)

![Columnas](https://img.shields.io/badge/N%C3%BAmero%20de%20columnas-17-important)

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
*Inspection Type*.           | Texto.               | Tipo de inspección, puede ser cualquiera de las siguientes: _canvass_, el tipo de inspección más común realizado con una frecuencia relativa al **riesgo del establecimiento**; _consultation_, es cuando la inspección se realiza por requerimiento del dueño previo a la apertura del establecimiento; _complaint_, se realiza una inspección en respuesta a una queja en contra del establecimiento; _license_, se realiza cuando el establecimiento lo requiere para recibir su lecencia para operar; _suspect food poisoning_, se realiza en respuesta a una o más presonas que presumiblemente hayan enfermado como resultado de haber comido en el establecimiento; _task-force inspection_, cuando la inspección se realiza a un bar o taverna.
*Results*.                   | Texto.               | _Pass, pass with conditions, fail, out of business or not located_; '_pass_' implica que no se tienen violaciones críticas o severas (códigos de violación 1-14 y 15-29 respectivamente). '_pass with conditions_', se encontraton violaciones críticas o severas, pero fueron corregidas durante la inspección. '_fail_' implica que se tienen violaciones críticas o severas y que no se corrigieron durante la inspección.
*Violations*.                | Texto.               |  Un establecimiento puede recibir más de una de las 45 distintas violaciones (código de violación 1 al 44 y 70). Pensar en como analizar esta variable.
*Latitude*.                  | Número.              | Latitud del negocio.
*Longitude*.                 | Número.              | Longitud del negocio.
*Location*.                  | *Location*.          | Contiene la coordenada (longitud y latitud) del negocio.

---

## ¿Qué buscamos contestar con nuestro modelo?
![Objetivo](https://img.shields.io/badge/Pregunta%20anal%C3%ADtica%20a%20contestar%20con%20el%20modelo%20predictivo-%C2%BFEl%20establecimiento%20pasar%C3%A1%20o%20no%20la%20inspecci%C3%B3n%3F-orange)

## Tomar en cuenta

![Frecuencia](https://img.shields.io/badge/Frecuencia%20de%20actualizaci%C3%B3n%20de%20los%20datos-Diaria-orange)

![Producto](https://img.shields.io/badge/Frecuencia%20de%20actualizaci%C3%B3n%20del%20producto%20de%20datos-Semanal-orange)

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
    │   ├── constants.py
    |   └── general.py 
    │
    │
    ├── etl       <- Scripts to transform data from raw to intermediate.
    │
    │
    ├── pipeline  <- Functions used for the pipeline.
    |   └── ingesta_almacenamiento.py 
```

---
## ¿Cómo reproducir los resultados de este repositorio?

Si usted desea reproducir los resultados mostrados en este trabajo, lo que tiene que hacer es lo siguiente:

1. Clonar el repositorio en la dirección de su agrado dentro de su computadora con el comando:
 
`git clone <url del repositorio> <nombre que desea poner al repositorio dentro de su sistema>`.

![Reproducir_EDA](https://img.shields.io/badge/PARA%20REPRODUCIR%20LOS%20RESULTADOS%20DE%20NUESTRO-EDA-inactive)

2. Descargar el csv de esta [url](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5) y colocarlo en la ruta: `/notebooks/eda`.

3. **Opcional, requiere pyenv:** Genera el ambiente virtual para este proyecto con el comando:

`pyenv virtualenv 3.7.4 nombre_de_tu_environment`.

  Activa el ambiente virtual con el siguiente comando: `pyenv activate nombre_de_tu_environment`

  --> instalar ipykernel<br>
  `pip install ipykernel`

  --> hacer accesible el ambiente virtual al notebook de jupyter<br>
  `python -m ipykernel install --user --name nombre_de_tu_environment --display-name nombre_de_tu_environment`
  
![Instalar_requirements](https://img.shields.io/badge/C%C3%93MO%20INSTALAR%20NUESTRO-requirements.txt-inactive)

4. Instalar el `requirements.txt` que se encuentra en el mismo directorio de este archivo `README.md` con el comando:

`pip install -r requirements.txt`.

5. Abre tu terminal y desde ella entra al directorio raíz de este archivo.

6. Corre el comando `jupyter notebook` (asegúrate de tener activo tu environment).

7. Abre el archivo `EDA_GEDA_Checkpoint1.ipynb` y ya podrás operarlo sin problemas.

---

## Sobre nuestro ***EDA***

<p align = "left">
    <img src="images/eda.png" width="520" height="250" />

- En la ruta `notebooks/eda/EDA_GEDA_Checkpoint1.ipynb` encontrarás el *notebook* que contiene los resultados encontrados en el ***checkpoint 1*** del proyecto.

- En la ruta `notebooks/eda/Food_Inspections.csv` deberá ser el archivo que descargaste de la liga mencionada anteriormente para poder utilizarse con el *notebook* de nuestro *EDA*.

---

## Cómo funciona nuestro proceso de ingestión

<p align = "left">
    <img src="images/di.jpg" width="200" height="200" />

![Resumen](https://img.shields.io/badge/Proceso%20de%20Ingesti%C3%B3n-Resumen-yellowgreen)

El proceso **consiste** en descargar la información de inspecciones que está contenida en la página [***Chicago Food Inspections***](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5) de **forma programática y automatizada**. Se realiza una **ingesta inicial (descarga)** y posteriormente se realizarán **descargas semanales consecutivas**.

![](./images/cfi.jpeg)

En los **módulos** siguientes se integran las funciones que nos permitirán realizar todo el proceso:

`general.py` e `ingesta_almacenamiento.py`.

Se encuentran ubicadas en la rama `main` dentro de la carpeta `src` de la siguiente manera:

```
├── src               
    ├── __init__.py
    │
    ├── utils
    |   └── general.py    
    │
    │
    ├── etl
    │
    │
    ├── pipeline
    |   └── ingesta_almacenamiento.py    
```

Una vez que se ha realizado la ingesta inicial como la consecutiva, la información será transformada en un archivo compacto (formato *pickle*, `.pkl`) para posteriormente ser almacenada en la nube de [***AWS S3***](https://aws.amazon.com/s3/). De esta forma, **mantendremos nuestro producto de datos actualizado**.

![Prerrequisitos](https://img.shields.io/badge/Proceso%20de%20Ingesti%C3%B3n-Prerrequisitos-yellowgreen)

1.	Para realizar la ingestión de información de ***Chicago Food Inspections*** es necesario que el usuario se dé de alta [aquí](https://data.cityofchicago.org/login) y genere un `app token`.

![](./images/app_token.jpg)

2.	Contar con una cuenta activa de ***AWS***. En ésta, se debe tener un *bucket* de ***S3*** exclusivo para almacenar la información del proyecto; **importante** mencionar que se debe conocer el **nombre exacto** del *bucket* y contar con el ***Access Key ID***.

<p align = "left">
    <img src="images/aws_s3_logo.jpeg" width="620" height="200" />

3.	Debe crear un archivo `.yaml` siguiendo la siguiente estructura: 

```
---
s3:
    aws_access_key_id: "de_tu_cuenta_de_AWS"
    aws_secret_access_key: "de_tu_cuenta_de_AWS"
food_inspections:
    api_token: "de_tu app_token_del_prerrquisito_1"
```

4.	Contar con un ambiente virtual de `pyenv` y tenerlo activo. Una vez posicionado dentro de éste, debe definir su variable de entorno `PYTHONPATH`. Debe abrir su terminal y posicionarse en la raíz del repositorio y ejecutar el comando `export PYTHONPATH=$PWD`.

5.	Para poder generar las conexiones necesarias con los clientes, debe crear la carpeta `conf/local` donde deberá colocar su archivo `.yaml` (del prerrequisito 3). 

![Macroprocesos](https://img.shields.io/badge/Proceso%20de%20Ingesti%C3%B3n-Macroprocesos-yellowgreen)

Para iniciar con el **proceso de ingesta/almacenamiento** debe colocarse en la **raíz** de su **repostorio clonado** y seguir los siguientes **macroprocesos**:

![M1](https://img.shields.io/badge/Macroproceso%201-Conexi%C3%B3n%20a%20la%20API%20con%20SODAPY%20y%20con%20AWS%20S3-red)

- Estableceremos una **conexión** tipo "**cliente**" con la *API* del *Chicago Portal* llamando a nuestra función `get_client` (que se encuentra dentro de `ingesta_almacenamiento.py`), utilizando la **clase Socrata** de ***SODAPY***). Ésta a su vez llamará a la función `get_api_token` (que se encuentra dentro de `general.py`) la cual leerá  el *token* desde el archivo `credential.yaml` (descrito en `prerrequisitos`). Se retorna un cliente que podemos asignar a una variable `client`.

- Análogamente, establecemos una conexión con *AWS* en el servicio de *S3* del tipo `resource service client by name` llamando a nuestra función `get_s3_credentials()` (que se encuentra dentro de `ingesta_almacenamiento.py`), que a su vez llamará a la función `get_S3_credentials` (que se encuentra dentro de `general.py`) la cual leerá  el *token* desde el archivo `credential.yaml` y retorna las credenciales necesarias para establecer la conexión (se utiliza la clase ***Session*** de ***Boto3***). Se retorna un cliente que podemos asignar a una variable "***S3***".

![M2](https://img.shields.io/badge/Macroproceso%202-Generar%20datos%20ingesta-red)

**Inicial**:

- Se realiza sólo una vez y consiste en descargar toda la información generada hasta cierta fecha específica que sea lo más actual posible, considerando que la actualización de los datos se realiza en el portal los lunes a las 6:00 a.m.

- Solicitamos una descarga con la función `ingesta_inicial(client, limit)`, la cual recibe la variable "***client***" (definida en el macropoceso 1) y la variable "***limit***" (que define el número de registros a ingestar; se recomienda utilizar como **cota superior 300,000** para garantizar que se ingesta la totalidad de registros a la fecha específica).

- Retorna un objeto `list` con los registros generados en la consulta que pueden ser asignados a la variable `data_ii`.

**Consecutiva**:

- Se realizará de **forma automátizada cada semana posterior a la actualización del portal**. Actualmente el proceso de automatización está en desarrollo, por lo que sólo se puede realizar un *test* llamando a la función).

- Solicitamos una descarga con la función `ingesta_consecutiva(client, date, limit)`:
    - `client`: definida en el macroproceso 1.
    - `date`: *timestamp (string)* con el siguiente formato '**AAAA-MM-DDT00:00:000**'. Se debe respetar las comillas simples. Donde "AAAA" 4 dígitos del año, "MM" 2 dígitos del mes y "DD" 2 dígitos del día; "T" es un separador para el horario. Por último se deben conservar los dígitos en 0.
    - `limit`: *numeric* que define el número de registros a ingestar (se recomienda utilizar como **cota superior 1,000** para garantizar la totalidad del diferencial o "*delta* de registros").

- Retorna un objeto `list` con los registros generados en la consulta que pueden ser asignados a la variable `data_ic`.

**NOTA**: Las funciones anteriores invocan a la función `client.get()` de la clase **Socrata** de ***SODAPY***, la cual requiere los parámetros indicados en [***Access Dataset via SODA API***](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5):

- `socrata_domain` = "data.cityofchicago.org"
 
- `socrata_ds_id` = "4ijn-s7e5"
    
- Por último, estos se cargan de forma automática, no se requiere indicarlos.

![](./images/access_ds.jpeg)

![M3](https://img.shields.io/badge/Macroproceso%203-Trasformar%20y%20guardar%20los%20datos%20de%20ingesta%20en%20el%20bucket%20de%20S3-red)

Una vez que se ha realizado la **ingesta**, los datos generados en el proceso anterior serán transformados en un archivo con formato `pickle` o `.pkl` y serán almacenados en su *bucket* de *S3* de *AWS* con el nombre `historic-inspections-AAAA-MM-DD` o `consecutive-inspections-AAAA-MM-DD` según sea el caso, integrándolos en las subcarpetas denominadas `initial` y `consecutive` que están en una carpeta que se denmominará `ingestion` (mencionamos que no es necesaria tal estructura en el *bucket*, en automático se crea si no existe).

Para lo anterior, utilizaremos nuestra función `guardar_ingesta(my_bucket, bucket_path, data)` que recibe las variables:
   - `my_bucket`: *string* con el nombre de su *bucket* de *S3*.
   - `bucket_path`: *string* con alguno de los siguientes valores `ingestion/initial` o `ingestion/consecutive` según sea la ingesta a almacenar. Para estos valores, hemos realizado una declaración previa en las variables de ambiente `constants.py`, como `key1` y `key2` respectivamente.
   - `data`: recibe el objeto `list` generado en el macroproceso 2. Si se declararon las variables `data_ii` o `data_ic`, debe utilizarlas en lugar de declarar la variable `data`.
 
 ![Ejecución](https://img.shields.io/badge/Proceso%20de%20ingesti%C3%B3n-Ejecuci%C3%B3n%20del%20pipeline-yellowgreen)
 
1. Posicionarse en la carpeta donde se hizo el clon.
2. Activar el entorno `pyenv` adecuado y exportar la variable de entorno `PYTHONPATH` (mencionado arriba).
3. Ejecutar el comando `python`.
4. Dentro de la terminal de python (>>>) ejecutar los siguientes comandos:
```
# Declaración de módulos.
>>> import src.utils.constants as ks
>>> import src.utils.general as gral
>>> import src.pipeline.ingesta_almacenamiento as ial

# Declaración de variables auxiliares.
>>> date = '2020-02-18T00:00:000'  # Ejemplo con declaración de variable date de acuerdo a lo mencionado en el Macroproceso 2.
>>> my_bucket = "bucket_del_equipo_rocket"  # Ejemplo de declaración de la variable my_bucket de acuerdo a lo indicado en el Macroproceso 3.

# Desarrollo de funciones.
>>> client = ial.get_client()
>>> data_ii = ial.ingesta_inicial(client, limit = 300000)
>>> data_ic = ial.ingesta_consecutiva(client, date , limit=1000)
>>> ial.guardar_ingesta(my_bucket, ks.key1, data_ii) # Para la ingesta inicial.
>>> ial.guardar_ingesta(my_bucket, ks.key2, data_ic) # Para la ingesta consecutiva.
```
![Observaciones](https://img.shields.io/badge/Proceso%20de%20ingesti%C3%B3n-Observaciones-yellowgreen)

Al mandar llamar la librería `import src.utils.constants as ks`, se mandan llamar también las siguientes variables de entorno que son utilizadas para realizar la ingesta:

 - `socrata_domain` = "data.cityofchicago.org"
 
 - `socrata_ds_id` = "4ijn-s7e5"
 
 - `path` = os.path.realpath('conf/local/credentials.yaml')
 
 - `key1` = 'ingestion/initial'
 
 - `key2` = 'ingestion/consecutive'

---

## Sobre nuestro *Data Pipeline*

<p align = "left">
    <img src="images/dp.png" width="220" height="220" />
    
Nuestro proyecto está conformado por diferentes *pipelines*. Para ordenar la secuencia que éstos deben seguir, utilizamos un orquestador llamado [***Luigi***](https://luigi.readthedocs.io/en/stable/).

![Luigi_version](https://img.shields.io/badge/Luigi-3.0.2-brightgreen)

[***Luigi's documentation***](https://luigi.readthedocs.io/en/stable/)

[**Luigi's GitHub page**](https://github.com/spotify/luigi)

![](./images/luigi.png)

### ¿Qué es *Luigi*?

![](./images/luigi_is.jpeg)

<sub><sup>**Fuente**:[***Luigi's documentation***](https://luigi.readthedocs.io/en/stable/)</sup></sub>

Este orquestador es la herramienta que nos permite correr nuestro *data pipeline*, definiendo aspectos importantes como el cómo, el cúando y el con qué se debe correr cada proceso.

Para administrar el orden de las tareas (cómo nuestros distintos *tasks* correrán) en el *pipeline*, ***Luigi*** utiliza una estructura de datos llamada ***DAG*** (***Directed Acyclic Graph***). Es una herramienta visual útil y que ilustra de manera clara los procesos que nuestro proyecto sigue.

**Así se ve el** ***DAG*** **de nuestro** ***data pipeline*** **orquestado en** ***Luigi***:

**NOTA: INSERTAR FOTO DE DAG AQUÍ**

##

![DAG](https://img.shields.io/badge/Aspectos%20importantes%20a%20considerar-DAG-blue)

- Se permite tener más de 1 entrada y sólo 1 salida. **NO** se permite tener ciclos.

##

- Está conformado por:

![EP1](https://img.shields.io/badge/1.-V%C3%A9rtices%2Fnodos-blueviolet)

Cada arco nodo representa el *task* a ejecutar.

![EP2](https://img.shields.io/badge/2.-Aristas%2Farcos-blueviolet)

Cada arista la dirección de flujo.

##

- Sigue 3 principios:

![DP1](https://img.shields.io/badge/DAG--Principio%201-Idempotencia-blueviolet)

Aunque un proceso se corra con los mismos parámetros múltiples ocasiones, la salida que se obtiene siempre es la misma. Esto implica que tampoco se generan salidas repetidas.

![DP2](https://img.shields.io/badge/DAG--Principio%202-Direcci%C3%B3n-blueviolet)

La dirección del grafo va en un sólo sentido.

![DP3](https://img.shields.io/badge/DAG--Principio%203-Ac%C3%ADclico-blueviolet)

La salida de un nodo no puede regresar a uno que ya fue procesado.

##

![L_aspectos](https://img.shields.io/badge/Aspectos%20importantes%20a%20considerar-Luigi-blue)

***Luigi*** tiene 2 objetos principales para construir su ***DAG***:

![LO1](https://img.shields.io/badge/Luigi--Objeto%201-Target-9cf)

Dónde se sacan los datos que requiere un *task*.

![LO2](https://img.shields.io/badge/Luigi--Objeto%202-Task-9cf)

La tarea que queremos sea administrada. Para declarar un *task* en *Luigi* debemos tener un *script* que tenga los siguientes 4 métodos requeridos:

![LM1](https://img.shields.io/badge/Luigi--Task--M%C3%A9todo%201-run()-inactive)

El código que se debe correr.

##

![LM2](https://img.shields.io/badge/Luigi--Task--M%C3%A9todo%202-input()-inactive)

Qué requiere de entrada la tarea y dónde se debe obtener.

##

![LM3](https://img.shields.io/badge/Luigi--Task--M%C3%A9todo%203-output%20()-inactive)

Qué salida genera la tarea y dónde se queda persistida. Éste siempre regresa un objeto de tipo `target`.

##

![LM4](https://img.shields.io/badge/Luigi--Task--M%C3%A9todo%204-requires%20()-inactive)

Método con el que se define cómo está formado el grafo de dependencias entre tareas.

<sub><sup>**NOTA: Algunos de estos métodos son opcionales**.</sup></sub>

---
