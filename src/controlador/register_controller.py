"""
register_controller.py

Este módulo define el controlador encargado de gestionar el registro de nuevos usuarios.
Valida los datos ingresados, asegura la coincidencia de contraseñas y utiliza bcrypt
para almacenar la contraseña de forma segura.
"""

from src.modelo.service.auth_service.register_user import RegisterUser
from src.modelo.entities.usuario import Usuario
import bcrypt


class RegisterUserController:
    """Controlador responsable del registro de nuevos usuarios."""

    @staticmethod
    def register_user(nombres, apellidos, alias, password, confirm_password, pregunta, respuesta):
        """Registra un nuevo usuario luego de validar los datos ingresados.

        Args:
            nombres (str): Nombres del usuario.
            apellidos (str): Apellidos del usuario.
            alias (str): Alias único para el usuario.
            password (str): Contraseña del usuario.
            confirm_password (str): Confirmación de la contraseña.

        Returns:
            tuple: (bool, str) indicando si el registro fue exitoso y un mensaje asociado.
        """
        if (not nombres or not apellidos or not alias or not password or not confirm_password
                or not pregunta or not respuesta):
            return False, 'Tiene que rellenar todos los campos.'

        if password != confirm_password:
            return False, 'Las contraseñas no coinciden.'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        hashed_respuesta = bcrypt.hashpw(respuesta.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        usuario = Usuario(Nombres=nombres, Apellidos=apellidos,
                          Alias=alias,Password=hashed_password, Pregunta=pregunta,
                          respuesta=hashed_respuesta)
        return RegisterUser(usuario).register_user()
