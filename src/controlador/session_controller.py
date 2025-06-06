"""
session_controller.py

Este módulo define el controlador de sesión que permite acceder a información
de la sesión activa del usuario, como el alias del usuario autenticado.
"""

from src.modelo.service.session_service.session_manager import SessionManager

class SessionController:
    """Controlador encargado de gestionar operaciones
    relacionadas con la sesión del usuario."""

    @staticmethod
    def get_alias_user():
        """Obtiene el alias del usuario actualmente en sesión.

        Returns:
            str: Alias del usuario autenticado.
        """
        return SessionManager.get_instance().usuario.Alias
