import psycopg2
import json
from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta

# Cargar configuración desde archivo
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Configuración de la conexión a PostgreSQL
DB_CONFIG = config["databases"]["origin"]

# Inicializar Faker
fake = Faker()

# Función para insertar datos en las tablas defiriendo las FK
def populate_database():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Generar años académicos desde 2020 hasta 2030
        anos_academicos = []
        for ano in range(2020, 2025):  # Rango incluye 2030
            descripcion = f"A\u00f1o escolar {ano}-{ano + 1}"
            cursor.execute(
                "INSERT INTO sistema_notas.anos_academicos (ano, descripcion) VALUES (%s, %s) RETURNING ano_id;",
                (ano, descripcion)
            )
            ano_id = cursor.fetchone()[0]
            anos_academicos.append(ano_id)


        # Generar grados
        grados = []
        niveles = ["Primaria", "Secundaria"]
        nombres = ["1ro B\u00e1sico", "2do B\u00e1sico", "3ro B\u00e1sico", "1ro Bachillerato", "2do Bachillerato"]
        for nivel in niveles:
            for nombre in nombres:
                cursor.execute(
                    "INSERT INTO sistema_notas.grados (nivel, nombre) VALUES (%s, %s) RETURNING grado_id;",
                    (nivel, nombre)
                )
                grado_id = cursor.fetchone()[0]
                grados.append(grado_id)

        # Generar docentes
        docentes = []
        for _ in range(10):
            nombre = fake.first_name()
            apellido = fake.last_name()
            correo = fake.email()
            telefono = fake.msisdn()[:15]  # Asegurar que el teléfono no exceda los 15 caracteres
            fecha_contratacion = fake.date_between(start_date="-5y", end_date="today")
            cursor.execute(
                """
                INSERT INTO sistema_notas.docentes (nombre, apellido, correo, telefono, fecha_contratacion)
                VALUES (%s, %s, %s, %s, %s) RETURNING docente_id;
                """,
                (nombre, apellido, correo, telefono, fecha_contratacion)
            )
            docente_id = cursor.fetchone()[0]
            docentes.append(docente_id)

        # Generar materias
        materias = []
        for grado_id in grados:
            for _ in range(5):
                nombre = fake.word().capitalize()
                cursor.execute(
                    "INSERT INTO sistema_notas.materias (nombre, grado_id) VALUES (%s, %s) RETURNING materia_id;",
                    (nombre, grado_id)
                )
                materia_id = cursor.fetchone()[0]
                materias.append((materia_id, grado_id))

        # Asignar docentes a materias
        for docente_id in docentes:
            for materia_id, _ in materias:
                if randint(0, 1):
                    cursor.execute(
                        "INSERT INTO sistema_notas.docentes_materias (docente_id, materia_id) VALUES (%s, %s);",
                        (docente_id, materia_id)
                    )

        # Generar estudiantes
        estudiantes = []
        for _ in range(60):
            nombre = fake.first_name()
            apellido = fake.last_name()
            fecha_nacimiento = fake.date_of_birth(minimum_age=6, maximum_age=18)
            direccion = fake.address()
            grado_actual = choice(grados)
            paralelo = choice("ABCDEF")
            fecha_matricula = fake.date_between(start_date="-2y", end_date="today")
            cursor.execute(
                """
                INSERT INTO sistema_notas.estudiantes (nombre, apellido, fecha_nacimiento, direccion, grado_actual, paralelo, fecha_matricula)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING estudiante_id;
                """,
                (nombre, apellido, fecha_nacimiento, direccion, grado_actual, paralelo, fecha_matricula)
            )
            estudiante_id = cursor.fetchone()[0]
            estudiantes.append((estudiante_id, grado_actual))

        # Generar periodos académicos
        periodos = []
        for _ in range(4):
            nombre = fake.word().capitalize()
            fecha_inicio = fake.date_between(start_date="-2y", end_date="today")
            fecha_fin = fecha_inicio + timedelta(days=randint(90, 180))
            cursor.execute(
                "INSERT INTO sistema_notas.periodos_academicos (nombre, fecha_inicio, fecha_fin) VALUES (%s, %s, %s) RETURNING periodo_id;",
                (nombre, fecha_inicio, fecha_fin)
            )
            periodo_id = cursor.fetchone()[0]
            periodos.append(periodo_id)

        # Generar notas
        for estudiante_id, grado_actual in estudiantes:
            for periodo_id in periodos:
                for materia_id, materia_grado in materias:
                    if materia_grado == grado_actual:
                        nota = round(randint(60, 100) + fake.random_number(digits=2) / 100, 2)
                        cursor.execute(
                            """
                            INSERT INTO sistema_notas.notas (estudiante_id, materia_id, periodo_id, ano_id, nota)
                            VALUES (%s, %s, %s, %s, %s);
                            """,
                            (estudiante_id, materia_id, periodo_id, choice(anos_academicos), nota)
                        )

        # Generar matrículas
        for estudiante_id, grado_actual in estudiantes:
            for ano_id in anos_academicos:
                estado = choice(["Inscrito", "Egresado", "Abandonado"])
                fecha_estado = fake.date_between(start_date="-2y", end_date="today")
                razon_abandono = fake.sentence(nb_words=10) if estado == "Abandonado" else None
                cursor.execute(
                    """
                    INSERT INTO sistema_notas.matriculas (estudiante_id, periodo_id, grado_id, ano_id, estado, fecha_estado, razon_abandono)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        estudiante_id,
                        choice(periodos),  # Periodo aleatorio
                        grado_actual,
                        ano_id,
                        estado,
                        fecha_estado,
                        razon_abandono,
                    ),
                )
        
        # Generar asistencias
        for estudiante_id, grado_actual in estudiantes:
            for periodo_id in periodos:
                for _ in range(30):  # 30 días de asistencias
                    fecha = fake.date_between(start_date="-1y", end_date="today")
                    presente = choice([True, False])
                    cursor.execute(
                        """
                        INSERT INTO sistema_notas.asistencias (estudiante_id, grado_id, ano_id, fecha, presente, periodo_id)
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """,
                        (
                            estudiante_id,
                            grado_actual,
                            choice(anos_academicos),
                            fecha,
                            presente,
                            periodo_id,
                        ),
                    )
        
        connection.commit()
        print("Datos generados con éxito.")

    except Exception as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    populate_database()
