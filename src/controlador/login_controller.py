from src.modelo.service.auth_service.login import LoginIn

class LoginController:
    @staticmethod
    def login(alias: str, password: str):
        if not alias or not password:
            return False, "DEBE RELLENAR LOS DOS ESPACIOS"

        return LoginIn(alias, password).process_login()

