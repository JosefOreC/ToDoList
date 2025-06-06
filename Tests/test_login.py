import sys
import os
import unittest
from unittest.mock import patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controlador.login_controller import LoginController

class TestLoginController(unittest.TestCase):

    @patch('controlador.login_controller.LoginIn')
    def test_login_success(self, mock_login_in):
        mock_login_in.return_value.process_login.return_value = (True, "Inicio de sesión exitoso")

        result = LoginController.login("usuario", "contraseña")
        self.assertEqual(result, (True, "Inicio de sesión exitoso"))

    def test_login_missing_alias(self):
        result = LoginController.login("", "contraseña")
        self.assertEqual(result, (False, "DEBE RELLENAR LOS DOS ESPACIOS"))

    def test_login_missing_password(self):
        result = LoginController.login("usuario", "")
        self.assertEqual(result, (False, "DEBE RELLENAR LOS DOS ESPACIOS"))

    def test_login_both_fields_missing(self):
        result = LoginController.login("", "")
        self.assertEqual(result, (False, "DEBE RELLENAR LOS DOS ESPACIOS"))

if __name__ == '__main__':
    unittest.main()