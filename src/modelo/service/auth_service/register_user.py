"""
    Crea la clase para el registro de un nuevo usuario
    Tiene las restricciones de:
        No puede crear usuarios con el mismo alias
"""

from src.modelo.entities.usuario import Usuario
from src.modelo.service.user_service.user_service_data import UserService


class RegisterUser:

    def __init__(self, usuario: Usuario):
        self.usuario = usuario

    def register_user(self):

        if UserService.is_user_with_alias_exits(self.usuario.Alias):
            return False, 'Alias ocupado.'

        try:
            self.save_in_db()
        except Exception as E:
            return False, E

        return True, "SE GUARDÓ AL NUEVO USUARIO"

    def save_in_db(self):
        UserService.insert_new_user(self.usuario)


if __name__ == "__main__":
    pass
