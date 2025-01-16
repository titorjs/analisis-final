-- ORIGIN
-- SISTEMA DE NOTAS - BDD - ORIGEN = STAGING

CREATE SCHEMA IF NOT EXISTS sistema_notas;

CREATE TABLE sistema_notas.anos_academicos (
    ano_id SERIAL PRIMARY KEY,
    ano INT NOT NULL, -- Ejemplo: 2024, 2025
    descripcion VARCHAR(50) -- Ejemplo: "Año escolar 2024-2025"
);

CREATE TABLE sistema_notas.grados (
    grado_id SERIAL PRIMARY KEY,
    nivel VARCHAR(50), -- Ejemplo: "Primaria", "Secundaria"
    nombre VARCHAR(50) -- Ejemplo: "1ro Básico", "2do Bachillerato"
);

CREATE TABLE sistema_notas.docentes (
    docente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100),
    telefono VARCHAR(15),
    fecha_contratacion DATE NOT NULL
);

CREATE TABLE sistema_notas.periodos_academicos (
    periodo_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50), -- Ejemplo: "Primer Trimestre"
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

CREATE TABLE sistema_notas.materias (
    materia_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    grado_id INT REFERENCES sistema_notas.grados(grado_id)
);

CREATE TABLE sistema_notas.estudiantes (
    estudiante_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT,
    grado_actual INT REFERENCES sistema_notas.grados(grado_id), -- Grado actual del estudiante
    paralelo CHAR(1) NOT NULL, -- Ejemplo: "A", "B", "C"
    fecha_matricula DATE NOT NULL
);

CREATE TABLE sistema_notas.notas (
    nota_id SERIAL PRIMARY KEY,
    estudiante_id INT REFERENCES sistema_notas.estudiantes(estudiante_id),
    materia_id INT REFERENCES sistema_notas.materias(materia_id),
    periodo_id INT REFERENCES sistema_notas.periodos_academicos(periodo_id),
    ano_id INT REFERENCES sistema_notas.anos_academicos(ano_id), -- Nuevo campo
    nota DECIMAL(5, 2) NOT NULL
);

CREATE TABLE sistema_notas.docentes_materias (
    docente_id INT REFERENCES sistema_notas.docentes(docente_id),
    materia_id INT REFERENCES sistema_notas.materias(materia_id),
    PRIMARY KEY (docente_id, materia_id)
);

CREATE TABLE sistema_notas.asistencias (
    asistencia_id SERIAL PRIMARY KEY,
    estudiante_id INT REFERENCES sistema_notas.estudiantes(estudiante_id),
    grado_id INT REFERENCES sistema_notas.grados(grado_id),
    ano_id INT REFERENCES sistema_notas.anos_academicos(ano_id), -- Nuevo campo
    periodo_id INT REFERENCES sistema_notas.periodos_academicos(periodo_id),
    fecha DATE NOT NULL,
    presente BOOLEAN NOT NULL
);

CREATE TABLE sistema_notas.matriculas (
    matricula_id SERIAL PRIMARY KEY,
    estudiante_id INT REFERENCES sistema_notas.estudiantes(estudiante_id),
    periodo_id INT REFERENCES sistema_notas.periodos_academicos(periodo_id),
    grado_id INT REFERENCES sistema_notas.grados(grado_id),
    ano_id INT REFERENCES sistema_notas.anos_academicos(ano_id), -- Nuevo campo para diferenciar años
    estado VARCHAR(20) NOT NULL, -- Ejemplo: "Inscrito", "Egresado", "Abandonado"
    fecha_estado DATE NOT NULL,
    razon_abandono TEXT -- Opcional
);

-- SOR

    CREATE SCHEMA IF NOT EXISTS sor;


    -- DIMENSIONES

    CREATE TABLE sor.grados (
        id BIGSERIAL PRIMARY KEY,
        nivel VARCHAR(50) NOT NULL, -- Ejemplo: "Primaria", "Secundaria", "Bachillerato"
        nombre VARCHAR(50) NOT NULL -- Ejemplo: "1ro Básico", "3ro Bachillerato"
    );

    CREATE TABLE sor.estudiantes (
        id BIGSERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        direccion TEXT,
        grado_actual INT REFERENCES sor.grados(id), -- Grado actual del estudiante
        fecha_matricula DATE NOT NULL
    );

    CREATE TABLE sor.materias (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        grado_id INT REFERENCES sor.grados(id) -- Grado en el que se imparte la materia
    );

    CREATE TABLE sor.docentes (
        id BIGSERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        correo VARCHAR(100),
        telefono VARCHAR(15),
        fecha_contratacion DATE NOT NULL
    );

    CREATE TABLE sor.periodos_academicos (
        id BIGSERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL, -- Ejemplo: "Primer Trimestre", "Segundo Trimestre"
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE NOT NULL
    );

    CREATE TABLE sor.anos_academicos (
        id BIGSERIAL PRIMARY KEY,
        ano INT NOT NULL, -- Ejemplo: 2024, 2025
        descripcion VARCHAR(50) -- Ejemplo: "Año escolar 2024-2025"
    );


    -- HECHOS
    CREATE TABLE sor.hechos_matricula (
        id BIGSERIAL PRIMARY KEY,
        grado_id BIGINT REFERENCES sor.grados(id),
        periodo_id BIGINT REFERENCES sor.periodos_academicos(id),
        ano_id BIGINT REFERENCES sor.anos_academicos(id), -- Nuevo campo
        total_inscritos INT,
        total_egresados INT,
        total_abandonos INT
    );

    CREATE TABLE sor.hechos_asistencia (
        id BIGSERIAL PRIMARY KEY,
        estudiante_id BIGINT REFERENCES sor.estudiantes(id),
        grado_id BIGINT REFERENCES sor.grados(id),
        ano_id BIGINT REFERENCES sor.anos_academicos(id),
        periodo_id BIGINT REFERENCES sor.periodos_academicos(id),
        total_presentes INT,
        total_ausentes INT
    );

    CREATE TABLE sor.hechos_rendimiento (
        id BIGSERIAL PRIMARY KEY,
        materia_id BIGINT REFERENCES sor.materias(id),
        grado_id BIGINT REFERENCES sor.grados(id),
        periodo_id BIGINT REFERENCES sor.periodos_academicos(id),
        ano_id BIGINT REFERENCES sor.anos_academicos(id),
        promedio_nota DECIMAL(5, 2),
        total_estudiantes INT
    );