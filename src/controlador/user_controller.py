"""
user_controller.py

Este módulo define el controlador responsable de manejar eventos relacionados con
la modificación y recuperación de datos del usuario actualmente en sesión.
Incluye funciones para actualizar datos personales y obtener información de sesión.
"""

from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.user_service.user_service_data import UserServiceData

class UserController:
    """
        Controlador para eventos relacionados con la modificación
        y recuperación de datos del usuario en sesión.
    """

    @staticmethod
    def event_update_user(nombres=None, apellidos=None, alias = None, password = None):
        """
        Maneja el evento de actualización del usuario actual.

        Args:
            nombres (str, optional): Nuevos nombres del usuario.
            apellidos (str, optional): Nuevos apellidos del usuario.
            alias (str, optional): Nuevo alias del usuario.
            password (str, optional): Nueva contraseña del usuario.

        Returns:
            tuple:
                bool: True si se guardaron los cambios, False si no se realizaron.
                str: Mensaje indicando el resultado de la operación.
        """
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
        """
        Obtiene los datos actuales del usuario en sesión.

        Returns:
            dict or object: Datos del usuario según el
            formato devuelto por SessionManager.get_data().
        """
        return SessionManager.get_instance().get_data()
