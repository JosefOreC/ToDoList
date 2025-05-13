"""
    Crea la clase con la que se operará toda la aplicacion
"""

from src.modelo.class_user import User


class SessionManager(User):
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

    __password: str
    __instance = None

    def __init__(self, initial_id, alias, password):
        super().__init__(initial_id, alias)
        self.__password = password

    @staticmethod
    def get_instance(initial_id = None, alias = None, password = None):
        if not SessionManager.__instance:
            SessionManager.__instance = SessionManager(initial_id,
                                                       alias,
                                                       password)
            return SessionManager.__instance

        if initial_id:
            SessionManager.__instance.update_id(initial_id)
        if alias:
            SessionManager.__instance.set_alias(alias)
        if password:
            SessionManager.__instance.set_password(password)
        return SessionManager.__instance


    def get_password(self):
        return self.__password

    def set_password(self, new_password):
        self.__password = new_password

if __name__ == "__main__":
    pass