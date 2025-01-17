# Documentación del Proyecto ETL CEIAF

## Acerca del Proyecto

El presente proyecto contiene una recopilación de los scripts en Python necesarios para la generación, extracción, transformación y carga de datos (ETL). Este flujo está diseñado para gestionar y procesar datos en las bases de datos _origin_, _staging_ y _sor_.

----------

## Instalación, Ejecución y Requisitos

### 1. Clonación del Repositorio

Para comenzar, clone el repositorio del proyecto desde GitHub utilizando el siguiente comando:

```
git clone https://github.com/titorjs/analisis-final
```

Acceda al directorio clonado:

```
cd analisis-final
```

### 2. Configuración del Proyecto

Localice y edite el archivo `config.json` dentro del directorio del proyecto. Este archivo contiene la configuración de las bases de datos. Cambie los parámetros según sea necesario para las bases de datos de _origin_, _staging_ y _sor_.

Un ejemplo del archivo `config.json`:

```
{
    "origin": {
        "host": "localhost",
        "port": 5432,
        "database": "origin_db",
        "user": "usuario",
        "password": "contraseña"
    },
    "staging": {
        "host": "localhost",
        "port": 5432,
        "database": "staging_db",
        "user": "usuario",
        "password": "contraseña"
    },
    "sor": {
        "host": "localhost",
        "port": 5432,
        "database": "sor_db",
        "user": "usuario",
        "password": "contraseña"
    }
}
```

### 3. Instalación de Dependencias

Asegúrese de tener Python instalado en su sistema. Instale las dependencias necesarias ejecutando el siguiente comando:

```
pip install psycopg2 pandas faker
```

### 4. Generación de Datos

1.  Ejecute el archivo `sql.sql` en las bases de datos correspondientes:
    
    -   Sección "ORIGIN": En las bases de datos _origin_ y _staging_.
        
    -   Sección "SOR": En la base de datos _sor_.
        
    
    Esto configurará las estructuras necesarias para las bases de datos involucradas.
    
2.  Genere datos aleatorios ejecutando el script `faker_generate.py`. Esto creará registros ficticios en la base de datos _origin_ según las estructuras definidas.
    

```
python faker_generate.py
```

### 5. Extracción de Datos

Ejecute el script `extract_compund.py` para transferir datos desde la base de datos _origin_ a _staging_.

```
python extract_compund.py
```

### 6. Transformación y Carga de Datos

Ejecute el script `transform.py` para realizar ajustes a los datos en la base de datos _staging_ y cargarlos en la base de datos _sor_.

```
python transform.py
```

----------

## Estructura del Proyecto

-   `**config.json**`: Archivo de configuración para las bases de datos.
    
-   `**sql.sql**`: Script SQL con las estructuras necesarias para las bases de datos.
    
-   `**faker_generate.py**`: Script para generar datos ficticios.
    
-   `**extract_compund.py**`: Script para realizar la extracción de datos.
    
-   `**transform.py**`: Script para transformar y cargar datos.
    

----------

## Notas Finales

-   Asegúrese de tener las bases de datos correctamente configuradas antes de ejecutar los scripts.
    
-   Verifique que las dependencias de Python estén instaladas correctamente para evitar errores durante la ejecución de los scripts.
    
-   Para cualquier duda, revise la documentación oficial de las bibliotecas utilizadas o consulte al administrador del proyecto.
