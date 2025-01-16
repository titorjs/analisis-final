import psycopg2
import pandas as pd
import json

# Cargar configuración desde archivo
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Configuración de la conexión a PostgreSQL
ORIGIN_DB_CONFIG = config["databases"]["staging"]
STAGING_DB_CONFIG = config["databases"]["sor"]

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

def tra_loa_process():
    """Proceso Transform y Load principal"""
    try:
        # Conexión a las bases de datos
        origin_conn = psycopg2.connect(**ORIGIN_DB_CONFIG)
        sor_conn = psycopg2.connect(**STAGING_DB_CONFIG)

        print("Transform: grados")
        grados_df = extract_data("SELECT * FROM sistema_notas.grados;", origin_conn)
        grados_df.rename(columns={"grado_id": "id"}, inplace=True)

        print("Transform: estudiantes")
        estudiantes_df = extract_data("SELECT * FROM sistema_notas.estudiantes;", origin_conn)
        estudiantes_df.rename(columns={"estudiante_id": "id"}, inplace=True)
        estudiantes_df.drop(columns=["paralelo"], inplace=True)
        
        print("Transform: materias")
        materias_df = extract_data("SELECT * FROM sistema_notas.materias;", origin_conn)
        materias_df.rename(columns={"materia_id": "id", "grado_id": "grado_id"}, inplace=True)

        print("Transform: docentes")
        docentes_df = extract_data("SELECT * FROM sistema_notas.docentes;", origin_conn)
        docentes_df.rename(columns={"docente_id": "id"}, inplace=True)

        print("Transform: periodos")
        periodos_df = extract_data("SELECT * FROM sistema_notas.periodos_academicos;", origin_conn)
        periodos_df.rename(columns={"periodo_id": "id"}, inplace=True)

        print("Transform: anos_academicos")
        anos_academicos_df = extract_data("SELECT * FROM sistema_notas.anos_academicos;", origin_conn)
        anos_academicos_df.rename(columns={"ano_id": "id"}, inplace=True)
        
        print("Transform: matriculas")
        matriculas_df = extract_data("SELECT * FROM sistema_notas.matriculas;", origin_conn)
        hechos_matriculas = matriculas_df.groupby(["grado_id", "periodo_id", "ano_id"]).agg(
            total_inscritos=("matricula_id", "count"),
            total_egresados=("estado", lambda x: (x == "Egresado").sum()),
            total_abandonos=("estado", lambda x: (x == "Abandonado").sum())
        ).reset_index()

        print("Transform: asistencia")
        asistencias_df = extract_data("SELECT * FROM sistema_notas.asistencias;", origin_conn)
        hechos_asistencia = asistencias_df.groupby(["estudiante_id", "grado_id", "periodo_id"]).agg(
            total_presentes=("presente", lambda x: (x == True).sum()),
            total_ausentes=("presente", lambda x: (x == False).sum())
        ).reset_index()

        print("Transform: rendimiento")
        notas_df = extract_data("SELECT * FROM sistema_notas.notas;", origin_conn)
        hechos_rendimiento = notas_df.groupby(["materia_id", "ano_id", "periodo_id"]).agg(
            promedio_nota=("nota", "mean"),
            total_estudiantes=("estudiante_id", "count")
        ).reset_index()
        
        print("Load: grados")
        load_data(grados_df, "sor.grados", sor_conn)
        
        print("Load: estudiantes")
        load_data(estudiantes_df, "sor.estudiantes", sor_conn)
        
        print("Load: materias")
        load_data(materias_df, "sor.materias", sor_conn)
        
        print("Load: docentes")
        load_data(docentes_df, "sor.docentes", sor_conn)
        
        print("Load: periodos")
        load_data(periodos_df, "sor.periodos_academicos", sor_conn)
        
        print("Load: anios academicos")
        load_data(anos_academicos_df, "sor.anos_academicos", sor_conn)
        
        print("Load: matricula")
        load_data(hechos_matriculas, "sor.hechos_matricula", sor_conn)
        
        print("Load: pagos")
        #load_data(grados_df, "sor.hechos_pagos", sor_conn)
        
        print("Load: asistencia")
        load_data(hechos_asistencia, "sor.hechos_asistencia", sor_conn)
        
        print("Load: rendimiento")
        load_data(hechos_rendimiento, "sor.hechos_rendimiento", sor_conn)

        print("Proceso ETL completado con éxito.")

    except Exception as e:
        print(f"Error en el proceso ETL: {e}")
    finally:
        # Cerrar conexiones
        if origin_conn:
            origin_conn.close()
        if sor_conn:
            sor_conn.close()

if __name__ == "__main__":
    tra_loa_process()
