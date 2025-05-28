"""
    Crea la clase para el registro de un nuevo usuario
    Tiene las restricciones de:
        No puede crear usuarios con el mismo alias
"""

from src.modelo.entities.usuario import Usuario


class RegisterUser:

    def __init__(self, usuario: Usuario, confirm_password):
        self.usuario = Usuario
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
        return self.__password == self.__confirm_password

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
        return InsertData.insert_user(name=self.__name, apellido_paterno=self.__apellido_paterno,
                               apellido_materno=self.__apellido_materno, alias=self.__alias,
                               password = self.__password)




if __name__ == "__main__":
    pass