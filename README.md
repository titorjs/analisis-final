# ETL CEIAF
## A cerca del proyecto

El presente proyecto tiene una corta recopilación de los scripts en python para la generación, extracción, transformación y carga de los datos.

## Instalación, ejecución y requisitos

1. Parametrización

Primero nos dirigiremos al archivo config.json y cambiamos los datos para las bases de datos de origen (origin), staging y sor.

Además, debemos instalar las dependencias de python: pip install psycopg2 pandas faker

2. Generación de datos

Primero, ejecutaremos la secció nde código sql.sql "ORIGIN" en las bases de datos staging y origin. Así mismo, se ejecutará la sección "SOR" en las base de datos sor.

Posterior a ello, se ejecutará el script de python faker_generate.py. Esto generará datos randómicos mediante la librería faker en base a la estructura antes descrita.

3. Extracción

Para el paso de extracción se ejecutará el script extract_compund.py el cual pasará los datos del origin al staging.

4. Transformación y carga

Finalmente, se debe ejecutar el script transform.py para tomar los datos del staging, hacerle diversos ajustes y pasarlos al sor.