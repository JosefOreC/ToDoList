from src.logica.connection_db.recover_data.user_data.recovery_auth_data import RecoverAuthData
from src.logica.connection_db.connection import ConnectionDataBase
from src.logica.connection_db.insert_data import (InsertData)

"""
    Crea la clase para el registro de un nuevo usuario
    Tiene las restricciones de:
        No puede crear usuarios con el mismo alias
"""


class RegisterUser:

    __alias: str
    __name: str
    __apellido_paterno: str
    __apellido_materno: str
    __password: str
    __confirm_password: str

    def __init__(self, alias, name, apellido_paterno, apellido_materno, password, confirm_password):
        self.__alias = alias
        self.__name = name
        self.__apellido_materno = apellido_materno
        self.__apellido_paterno = apellido_paterno
        self.__password = password
        self.__confirm_password = confirm_password

    def is_alias_valid(self):
        call_successful, response = RecoverAuthData.recover_id_user_for_alias(self.__alias)

        if not call_successful:
            pass
            return False

        if response:
            pass
            return False

        return True

    def is_same_password(self):
        if self.__password == self.__confirm_password:
            return True
        return False

    def register_user(self):
        if not self.is_same_password():
            return False, "LAS CONTRASEÑAS NO COINCIDEN"
        if not self.is_alias_valid():
            return False, "EL ALIAS YA ESTÁ OCUPADO"

        is_save, response = self.save_in_db()

        if not is_save:
            return False, f"NO SE GUARDÓ AL USUARIO: \n{response}"
        return True, "SE GUARDÓ AL NUEVO USUARIO"

    def save_in_db(self):
        call_successful, response = InsertData.insert_user(name=self.__name, apellido_paterno=self.__apellido_paterno,
                               apellido_materno=self.__apellido_materno, alias=self.__alias,
                               password = self.__password)

        if not call_successful:
            #view error
            pass

        return call_successful, response




if __name__ == "__main__":
    pass