Para verificar que las funciones estan correctamente implementadas, seguir los siguientes pasos:

1. Clonar repositorio
2. Posicionarse en la carpeta donde se hizo el clon
3. Cargar el entorno -pyenv- adecuado (ver readme)
4. Ejecutar el comando 'python'
5. Dentro de la terminal de python (>>>) ejecutar los siguientes comandos:
   >>> import os
   >>> import src.utils.general as gral
   >>> import src.pipeline.ingesta_almacenamiento as ial
   >>> my_bucket = 'data-product-architecture-equipo-5.0'
   >>> bucket_path = 'ingestion/consecutive'
   >>> ial.guardar_ingesta(my_bucket,bucket_path)

Observaciones:

- El nombre del bucket que se puso en la variable -my_bucket- corresponde al que se creó en la cuenta personal AWS del usuario. Tú deberás colocar el nombre del bucket correspondientea a tu usuario. (el valor por default es: 'data-product-architecture-equipo-5.0') 

- Al mandar llamar la librería: -import src.pipeline.ingesta_almacenamiento as ial-, se mandan llamar también las siguientes variables de entorno que son utilizadas para realizar la ingesta:

socrata_domain = "data.cityofchicago.org"
socrata_ds_id = "4ijn-s7e5"
path = os.path.realpath('conf/local/credentials.yaml')

- La variable -bucket_path- determina el tipo de ingesta que se realiza (el valor por default es: 'ingestion/consecutive')

 -Si bucket_path = 'ingestion/consecutive' : mandará a guardar al bucket una consuta que va desde el 2021-02-11T00:00:00.000 y cuenta 1,000 registros hacia adelante (la fecha mostrada es el valor por default que tiene la función). Si se desea cambiar este parámetro, por ejemplo, para realizar una búsqueda que empieze en otra fecha, deberá escribir el siguiente código:
  
  >>> delta_date = '2021-02-15T00:00:00.000'

en el cual puede especificar fecha y hora a partir de la cual desea obtener información. Este comando debe ser puesto antes de mandar llamar la función:
  
  >>> ial.guardar_ingesta(my_bucket,bucket_path)
  
 - Si bucket_path = 'ingestion/initial': mandará a guardar al bucket una consuta que va desde la fecha en que se ejecuta la función -ial.guardar_ingesta- y 300,000 registros hacia atrás (este valor es el establecido por default y garantiza que se extraigan todos los registros existentes en la BD de Chicago food inspections).

- Si solo manda llamar los siguientes comandos:
   >>> import os
   >>> import src.utils.general as gral
   >>> import src.pipeline.ingesta_almacenamiento as ial
   >>> ial.guardar_ingesta(my_bucket,bucket_path)

 Le marcará error porque los valores por default que tomará no coresponderán ni a sus credenciales ni al nombre del bucket asociado a su cuenta de AWS. Sin embargo, puede modificar el código del archivo: -ingesta_almacenamiento.py- para configurar las variables de entorno que se cargan por default de acuerdo a sus necesidades. Esto lo puede realizar en esta parte del código:

''' Variables de entorno que se cargan por default al cargar la librería
    ingesta_almacenamiento.py
'''

socrata_domain = "data.cityofchicago.org"
socrata_ds_id = "4ijn-s7e5"
path = os.path.realpath('conf/local/credentials.yaml')
delta_date = '2021-02-15T00:00:00.000'
my_bucket = 'data-product-architecture-equipo-5.0'
bucket_path = 'ingestion/consecutive'