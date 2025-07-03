import unittest
from unittest.mock import patch, MagicMock
from src.controlador.login_controller import LoginController


class TestLoginController(unittest.TestCase):

    def test_login_empty_fields(self):
        # Caso cuando alias y/o password están vacíos
        result = LoginController.login("", "")
        self.assertFalse(result[0])
        self.assertEqual(result[1], "DEBE RELLENAR LOS DOS ESPACIOS")

    @patch('src.controlador.login_controller.LoginIn')
    def test_login_success(self, mock_login_in_class):
        # Simulamos un inicio de sesión exitoso
        mock_instance = MagicMock()
        mock_instance.process_login.return_value = (True, "Inicio de sesión exitoso")
        mock_login_in_class.return_value = mock_instance

        result = LoginController.login("usuario", "contraseña123")

        self.assertTrue(result[0])
        self.assertEqual(result[1], "Inicio de sesión exitoso")

    @patch('src.controlador.login_controller.LoginIn')
    def test_login_failure(self, mock_login_in_class):
        # Simulamos un fallo de inicio de sesión
        mock_instance = MagicMock()
        mock_instance.pr_
