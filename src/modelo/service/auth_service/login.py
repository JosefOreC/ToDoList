"""
Módulo que genera la lógica del inicio de sesión de usuario.
"""

from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.user_service.user_service_data import UserServiceData

class LoginIn:
    """Clase responsable de manejar el proceso de inicio de sesión."""

    def __init__(self, alias, password):
        """Inicializa una instancia del inicio de sesión.

        Args:
            alias (str): Alias del usuario (nombre de usuario).
            password (str): Contraseña del usuario.
        """
        self.__alias = alias
        self.__password = password

    def process_login(self):
        """Procesa la autenticación del usuario.

        Returns:
            tuple: Un par (bool, str) que indica si el inicio de sesión fue exitoso
            y un mensaje asociado con el resultado.
        """
        SessionManager.log_out()
        if not UserServiceData.is_user_with_alias_exits(self.__alias):
            return False, "EL USUARIO NO EXISTE"
        usuario = UserServiceData.recover_user_for_alias(self.__alias)
        SessionManager.get_instance(usuario)
        if SessionManager.get_instance().validar_usuario(self.__password):
            return True, "USER LOGIN SUCCESSFUL"
        SessionManager.log_out()
        return False, "CONTRASEÑA INCORRECTA"

if __name__ == "__main__":
    print(LoginIn('Betos', 'Cisco').process_login())
