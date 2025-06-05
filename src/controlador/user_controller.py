from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.user_service.user_service_data import UserServiceData

class UserController:
    @staticmethod
    def event_update_user(nombres=None, apellidos=None, alias = None, password = None):
        if not(nombres or apellidos or alias or password):
            return False, "No se hizo ningún cambio"

        usuario_session = SessionManager.get_instance().usuario

        try:
            UserServiceData.update_user(usuario_session, nombres, apellidos, alias, password)
            return True, 'Se guardaron los cambios.'
        except Exception as E:
            return False, f'No se pudieron guardar los cambios.\n {E}'

    @staticmethod
    def get_data_session_manager():
        return SessionManager.get_instance().get_data()