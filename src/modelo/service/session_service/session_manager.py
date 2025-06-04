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
        self.usuario = usuario

    @staticmethod
    def get_instance(usuario: Usuario = None):
        if not SessionManager.__instance:
            if not usuario:
                raise Exception("No existe un usuario logueado ahora mismo OR "
                                "\nNo se mandaron los datos necesarios para el inicio de sesión")
            SessionManager.__instance = SessionManager(usuario)
        return SessionManager.__instance


    @staticmethod
    def log_out():
        SessionManager.__instance = None

    def get_password(self):
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