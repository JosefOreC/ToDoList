"""
    Crea la clase para el registro de un nuevo usuario
    Tiene las restricciones de:
        No puede crear usuarios con el mismo alias
"""

from src.modelo.entities.usuario import Usuario
from src.modelo.service.user_service.user_service_data import UserServiceData


class RegisterUser:
    """Clase para gestionar el registro de un nuevo usuario."""

    def __init__(self, usuario: Usuario):
        """Inicializa la instancia con un objeto Usuario.

        Args:
            usuario (Usuario): Objeto que contiene los datos del usuario a registrar.
        """
        self.usuario = usuario

    def register_user(self):
        """Registra un nuevo usuario si el alias no está ocupado.

        Verifica que el alias no exista en la base de datos antes de insertar.
        En caso de error durante la inserción, captura la excepción y devuelve un mensaje.

        Returns:
            tuple: (bool, str) indicando el éxito o fracaso del registro y un mensaje explicativo.
        """
        if UserServiceData.is_user_with_alias_exits(self.usuario.Alias):
            return False, 'Alias ocupado.'

        try:
            self.save_in_db()
        except Exception as E:
            return False, E

        return True, "SE GUARDÓ AL NUEVO USUARIO"

    def save_in_db(self):
        """Inserta el nuevo usuario en la base de datos.
        """
        UserServiceData.insert_new_user(self.usuario)

if __name__ == "__main__":
    pass
