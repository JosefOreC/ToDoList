"""
    Crea la clase con la que se operará toda la aplicacion
"""

from src.modelo.entities.usuario import Usuario

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

    def validar_usuario(self, password):
        if self.usuario and self.usuario.Password == password:
            return True
        return False

if __name__ == "__main__":
    pass