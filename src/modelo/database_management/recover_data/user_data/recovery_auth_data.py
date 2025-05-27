from src.modelo.database_management.connection import ConnectionDataBase
from src.modelo.database_management.recover_data.recover_data import RecoverData

class RecoverAuthData:
    __connection = ConnectionDataBase.get_instance()

    @staticmethod
    def recover_id_user_for_alias(alias: str):
        atributs = ['id_user']
        query = RecoverData.constructor_query(table='USER', atributs = atributs, where='alias = ?')
        call_successful, response = RecoverAuthData.__connection.select_query(query, (alias,))
        if call_successful:
            if response:
                id_user = response[0][0]
            else:
                id_user = None
            return True, id_user
        return False, f"ERROR AL BUSCAR EN LA BASE DE DATOS: {response}"

    @staticmethod
    def recover_user_session_manager(alias: str):

        query = RecoverData.constructor_query("USER", ['id_user', 'alias', 'password'], where="alias = ?", limit=1)
        call_successful, response = RecoverAuthData.__connection.select_query(query, (alias,))

        if not call_successful:
            pass
            return call_successful, response

        data_user = {'id_user': response[0][0], 'alias': response[0][1], 'password': response[0][2]}

        return call_successful, data_user

if __name__ == "__main__":
    pass