"""

"""

from src.modelo.service.session_service.session_manager import SessionManager

class MainViewController:
    @staticmethod
    def log_out():

        SessionManager.log_out()
        return True, 'Se cerró sesión con exito'