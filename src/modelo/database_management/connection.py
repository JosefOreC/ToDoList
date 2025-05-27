import sqlite3 as sql


"""
    Establece las conexiones con la base de datos
"""

class ConnectionDataBase:

    instance = None

    def __init__(self):
        self.__connection = sql.connect('.//src//logica//database_management//todolist_db.db')
        self.__cursor = self.__connection.cursor()

    @staticmethod
    def get_instance():
        if not ConnectionDataBase.instance:
            ConnectionDataBase.instance = ConnectionDataBase()
        return ConnectionDataBase.instance

    def select_query(self, query, data: tuple = ()):
        if type(data) != tuple  and type(data) == list:
            data=tuple(data)
        try:
            rs = self.instance.__cursor.execute(query, data)
            rs = rs.fetchall()
            if not rs:
                return  True, None
            return True, rs
        except Exception as E:
            return False, E

    def insert_or_update_query(self, query, *data):

        try:
            self.instance.__cursor.execute(query, data)
            self.instance.__connection.commit()
            return True, "ACTUALIZACION EXITOSA"
        except Exception as E:
            return False, E



if __name__ == "__main__":
    pass

