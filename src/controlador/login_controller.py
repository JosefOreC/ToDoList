from src.modelo.service.auth_service.login import LoginIn

class LoginController:
    """Controlador encargado de gestionar el proceso de inicio de sesión."""

    @staticmethod
    def login(alias: str, password: str):
        """Procesa el inicio de sesión para un usuario dado su alias y contraseña.

        Args:
            alias (str): Alias del usuario.
            password (str): Contraseña del usuario.

        Returns:
            tuple: (bool, str) indicando si el inicio de sesión fue exitoso y un mensaje asociado.
        """
        if not alias or not password:
            return False, "DEBE RELLENAR LOS DOS ESPACIOS"

        return LoginIn(alias, password).process_login()
