

from src.logica.connection_db.connection import ConnectionDataBase


class InsertData:

    __connection = ConnectionDataBase.get_instance()

    @staticmethod
    def get_id_user():
        query = """
                        SELECT id_user FROM USER ORDER BY id_user DESC LIMIT 1    
                    """
        call_successful, id_user = ConnectionDataBase.get_instance().select_query(query)
        if not call_successful:
            return 'NOT ID RECOVER', False
        id_user = id_user[0][0]

        if id_user:
            id_user = str(int(id_user) + 1)

        aux = ''
        for i in range(10 - len(id_user)):
            aux += '0'
        id_user = aux + id_user
        return True, id_user

    @staticmethod
    def constructor_query(table: str, atributs: list):

        query = f""" INSERT INTO {table}("""
        for atribut in atributs:
            query += atribut
            if atributs.index(atribut) < len(atributs)-1:
                query += ", "

        query += ") VALUES("

        for i in range(len(atributs)):
            query += '?'
            if i < len(atributs) - 1:
                query += ", "

        return query + ')'

    @staticmethod
    def insert_user(name: str, apellido_paterno: str, apellido_materno: str , alias: str, password: str):
        atributs = ['id_user', 'nombre', 'apellido_parterno', 'apellido_marterno', 'alias', 'password']
        query = InsertData.constructor_query(table='USER', atributs=atributs)
        call_successfull, id_user = InsertData.get_id_user()
        if not call_successfull:
            pass
            return False, "NO SE PUDO RECUPERAR UN ID PARA EL NUEVO USUARIO"

        return InsertData.__connection.insert_or_update_query(query, id_user, name, apellido_paterno, apellido_materno, alias, password)





if __name__ == "__main__":
    pass