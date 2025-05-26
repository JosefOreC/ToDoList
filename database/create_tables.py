import sqlite3 as sql

conn = sql.connect("../src/modelo/database_management/todolist_db.db")
cursor = conn.cursor()

tables = [
        """
            CREATE TABLE USUARIO (
                IDUsuario INT PRIMARY KEY, 
                Nombres VARCHAR(60),
                Apellidos VARCHAR(60),
                Alias VARCHAR(30),
                Estado BOOLEAN NOT NULL CHECK (Estado IN (0, 1)),
                Password VARCHAR(24)
            );
        """,
        """
            CREATE TABLE GRUPO (
                IDGrupo INT PRIMARY KEY,
                Nombre VARCHAR(50),
                Fecha_Creacion DATE,
                IDMaster INT,
                Descripcion VARCHAR(150)
            );
        """,
        """
            CREATE TABLE USUARIO_GRUPO (
                IDUsuario INT,
                IDGrupo INT,
                PRIMARY KEY (IDUsuario, IDGrupo),
                FOREIGN KEY (IDUsuario) REFERENCES USUARIO(IDUsuario),
                FOREIGN KEY (IDGrupo) REFERENCES GRUPO(IDGrupo)
                Rol INT NOT NULL CHECK (Rol IN (1, 3))
            );
        """,
        """
            CREATE TABLE PRIORIDAD (
                IDPrioridad INT PRIMARY KEY,
                Nombre VARCHAR(20),
                Descripcion VARCHAR(150)
            );
        """,
        """
            CREATE TABLE TAREA (
                IDTarea INT PRIMARY KEY,
                Nombre VARCHAR(100),
                Descripcion TEXT,
                Activo INT,
                Fecha_Programada DATE,
                IDPrioridad INT,
                FOREIGN KEY (IDPrioridad) REFERENCES PRIORIDAD(IDPrioridad)
            );
        """,
        """
            CREATE TABLE NOTIFICACION (
                IDNotificacion INT PRIMARY KEY,
                IDTarea INT,
                Mensaje TEXT,
                Fecha_Prog DATE,
                Hora_Programada TIME,
                FOREIGN KEY (IDTarea) REFERENCES TAREA(IDTarea)
            );
        """,
        """
            CREATE TABLE CLIENTE_TAREA (
                IDCliente_Tarea INT PRIMARY KEY,
                IDCliente INT AUTO_INCREMENT,
                IDUsuario INT,
                IDTarea INT,
                IDGrupo INT,
                Estado INT,
                FOREIGN KEY (IDUsuario) REFERENCES USUARIO(IDUsuario),
                FOREIGN KEY (IDGrupo) REFERENCES GRUPO(IDGrupo),
                FOREIGN KEY (IDTarea) REFERENCES TAREA(IDTarea)
            );
        """,
        """
            CREATE TABLE CATEGORIA (
                IDCategoria INT PRIMARY KEY,
                IDCliente INT,
                Nombre VARCHAR(30),
                Descripcion TEXT,
                FOREIGN KEY (IDCliente) REFERENCES CLIENTE_TAREA(IDCliente)
            );
        """]

for table in tables:

    conn.execute(
        table
    )

    conn.commit()