from src.modelo.service.user_service.user_service_data import UserService, Usuario

class UserController:
    @staticmethod
    def event_update_user(usuario: int or Usuario, nombres=None, apellidos=None, alias = None, estado = None, password = None):
        if not(nombres or apellidos or alias or password or estado != None):
            return False, "No se hizo ningún cambio"

        try:
            UserService.update_user(usuario,nombres,apellidos, alias, estado, password)
            return True, 'Se guardaron los cambios.'
        except Exception as E:
            return False, f'No se pudieron guardar los cambios.\n {E}'

