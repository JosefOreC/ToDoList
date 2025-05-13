"""
    Genera la lógica del inicio de sesión
"""

from src.logica.connection_db.recover_data.user_data.recovery_auth_data import RecoverAuthData
from src.modelo.session_manager import SessionManager

class LoginIn:

    __alias: str
    __password: str
    __data_user: dict

    def __init__(self, alias, password):
        self.__alias = alias
        self.__password = password

    def user_exits(self):
        call_successful, response = RecoverAuthData.recover_id_user_for_alias(alias=self.__alias)
        if not call_successful or not response:
            return False
        return True

    def password_confirm(self):
        if self.__password == self.__data_user.get('password'):
            return True
        return False

    def process_login(self):
        if self.user_exits():
            call_successful, self.__data_user = RecoverAuthData.recover_user_session_manager(self.__alias)
        else:
            return False, "EL USUARIO NO EXISTE"

        if not call_successful:
            pass
            return False, self.__data_user

        if self.password_confirm():
            SessionManager.get_instance(self.__data_user.get('name'),
                                        self.__data_user.get('alias'),
                                        self.__data_user.get('password'))
            return True, "USER LOGIN SUCCESSFUL"

        return False, "CONTRASEÑA INCORRECTA"


if __name__ == "__main__":
    pass