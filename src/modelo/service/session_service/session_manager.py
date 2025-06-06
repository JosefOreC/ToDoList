"""
    Crea la clase con la que se operará toda la aplicacion
"""

from src.modelo.entities.usuario import Usuario
import bcrypt

class SessionManager:
    """
        Con esta clase se crearan y ejecutaran todas las acciones de la aplicacion
        Marcando los create y edit con su ID
        Funciones en las que intervendra:
            - crear tarea
            - iniciar sesion
            - crear grupo
            - editar tarea
            - validar tarea
            - extraer tareas... etc
    """
    __instance = None

    def __init__(self, usuario):
        """
        Inicializa el gestor de sesión con el usuario proporcionado.

        Args:
            usuario (Usuario): Instancia del usuario que ha iniciado sesión.
        """
        self.usuario = usuario

    @staticmethod
    def get_instance(usuario: Usuario = None):
        """
        Obtiene la instancia única del gestor de sesión. Si no existe,
        se debe proporcionar un usuario para crearla.

        Args:
            usuario (Usuario, optional): Usuario con el que se inicia sesión.

        Returns:
            SessionManager: Instancia única del gestor de sesión.

        Raises:
            Exception: Si no hay sesión activa ni se proporciona un usuario.
        """
        if not SessionManager.__instance:
            if not usuario:
                raise Exception("No existe un usuario logueado ahora mismo OR "
                                "\nNo se mandaron los datos necesarios para el inicio de sesión")
            SessionManager.__instance = SessionManager(usuario)
        return SessionManager.__instance


    @staticmethod
    def log_out():
        """
        Cierra la sesión actual eliminando la instancia activa del gestor.
        """
        SessionManager.__instance = None

    def get_password(self):
        """
        Obtiene la contraseña cifrada del usuario actual.

        Returns:
            str: Contraseña cifrada (hash).
        """
        return self.usuario.Password

    def validar_usuario(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.usuario.Password.encode('utf-8'))

    @staticmethod
    def get_id_user():
        return SessionManager.get_instance().usuario.IDUsuario

    def get_data(self):
        return {
            'nombres': self.usuario.Nombres,
            'apellidos': self.usuario.Apellidos,
            'alias': self.usuario.Alias
        }

if __name__ == "__main__":
    pass