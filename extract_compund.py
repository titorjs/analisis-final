import psycopg2
import pandas as pd
import json

# Cargar configuración desde archivo
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Configuración de la conexión a PostgreSQL
ORIGIN_DB_CONFIG = config["databases"]["origin"]
STAGING_DB_CONFIG = config["databases"]["staging"]

def extract_data(query, connection):
    """Extrae datos desde la base origin"""
    try:
        return pd.read_sql_query(query, connection)
    except Exception as e:
        print(f"Error al extraer datos: {e}")
        return None

def load_data(df, table_name, connection):
    """Carga datos en la base staging"""
    try:
        cursor = connection.cursor()
        for _, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join(row.index)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
            cursor.execute(sql, tuple(row))
        connection.commit()
        print(f"Datos cargados en la tabla {table_name}")
    except Exception as e:
        print(f"Error al cargar datos en la tabla {table_name}: {e}")
        connection.rollback()

def etl_process():
    """Proceso ETL principal"""
    try:
        # Conexión a las bases de datos
        origin_conn = psycopg2.connect(**ORIGIN_DB_CONFIG)
        staging_conn = psycopg2.connect(**STAGING_DB_CONFIG)

        # Definir las tablas y consultas
        tables_queries = {
            "anos_academicos": "SELECT * FROM sistema_notas.anos_academicos;",
            "grados": "SELECT * FROM sistema_notas.grados;",
            "docentes": "SELECT * FROM sistema_notas.docentes;",
            "periodos_academicos": "SELECT * FROM sistema_notas.periodos_academicos;",
            "materias": "SELECT * FROM sistema_notas.materias;",
            "estudiantes": "SELECT * FROM sistema_notas.estudiantes;",
            "notas": "SELECT * FROM sistema_notas.notas;",
            "docentes_materias": "SELECT * FROM sistema_notas.docentes_materias;",
            "asistencias": "SELECT * FROM sistema_notas.asistencias;",
            "matriculas": "SELECT * FROM sistema_notas.matriculas;"
        }

        # Proceso ETL por tabla
        for table, query in tables_queries.items():
            print(f"Procesando tabla: {table}")
            
            # Extracción
            data = extract_data(query, origin_conn)
            if data is not None and not data.empty:
                # Carga
                load_data(data, f"sistema_notas.{table}", staging_conn)

        print("Proceso ETL completado con éxito.")

    except Exception as e:
        print(f"Error en el proceso ETL: {e}")
    finally:
        # Cerrar conexiones
        if origin_conn:
            origin_conn.close()
        if staging_conn:
            staging_conn.close()

if __name__ == "__main__":
    etl_process()
