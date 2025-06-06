"""
main_view_controller.py

Este módulo define el controlador de la vista principal de la aplicación.
Se encarga de gestionar acciones clave como el cierre de sesión del usuario
y la recuperación de tareas programadas para el día actual, aplicando el formato necesario.
"""

from src.modelo.service.session_service.session_manager import SessionManager
from src.controlador.task_controller import TaskController
from src.modelo.service.data_service.data_format import DataFormat

class MainViewController:
    """Controlador de la vista principal. Maneja funciones clave como cerrar sesión
    y recuperar tareas del día con formato adecuado."""

    @staticmethod
    def log_out():
        """Cierra la sesión actual del usuario.

        Returns:
            tuple: (bool, str) que indica si se cerró sesión con éxito y un mensaje.
        """
        SessionManager.log_out()
        return True, 'Se cerró sesión con exito'

    @staticmethod
    def recover_task_today_with_format():
        """Recupera las tareas del día actual y las convierte a un formato de diccionario.

        Returns:
            tuple:
                - bool: True si la recuperación fue exitosa, False en caso contrario.
                - list[dict] or str: Lista de tareas formateadas o mensaje de error.
        """
        is_task_recover, response =TaskController.recover_tasks_today()

        if not is_task_recover or not response:
            return is_task_recover, response

        tareas = DataFormat.convert_to_dict_task_data(response)

        return is_task_recover, tareas
