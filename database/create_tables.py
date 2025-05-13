import sqlite3 as sql

conn = sql.connect("../src/logica/connection_db/todolist_db.db")
cursor = conn.cursor()

conn.execute(
    '''
        CREATE TABLE USER(
            id_user VARCHAR(10) PRIMARY KEY,
            password VARCHAR(150),
            alias VARCHAR(45),
            nombre VARCHAR(50),
            apellido_parterno VARCHAR(25),
            apellido_marterno VARCHAR(25)
        )
    '''
)

conn.commit()