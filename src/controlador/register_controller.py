from src.modelo.service.auth_service.register_user import RegisterUser
from src.modelo.entities.usuario import Usuario

class RegisterUserController:
    @staticmethod
    def register_user(nombres, apellidos, alias, password, confirm_password):
        if not nombres or not apellidos or not alias or not password or not confirm_password:
            return False, 'Tiene que rellenar todos los campos.'

        if password != confirm_password:
            return False, 'Las contraseñas no coinciden.'
        usuario = Usuario(Nombres=nombres, Apellidos=apellidos, Alias=alias,Password=password)
        return RegisterUser(usuario).register_user()
