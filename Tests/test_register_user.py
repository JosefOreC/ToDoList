import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Agregar el directorio src al sys.path (con doble guion bajo en __file__)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controlador.register_controller import RegisterUserController

class TestRegisterUserController(unittest.TestCase):

    @patch('controlador.register_controller.RegisterUser')
    def test_register_user_success(self, mock_register_user):
        # Configurar el mock para simular el registro exitoso
        mock_register_user.return_value.register_user.return_value = (True, "Usuario registrado con éxito")

        result = RegisterUserController.register_user("Juan", "Pérez", "juanp", "contraseña123", "contraseña123")
        self.assertEqual(result, (True, "Usuario registrado con éxito"))

    def test_register_user_missing_fields(self):
        result = RegisterUserController.register_user("", "Pérez", "juanp", "contraseña123", "contraseña123")
        self.assertEqual(result, (False, 'Tiene que rellenar todos los campos.'))

    def test_register_user_password_mismatch(self):
        result = RegisterUserController.register_user("Juan", "Pérez", "juanp", "contraseña123", "contraseña456")
        self.assertEqual(result, (False, 'Las contraseñas no coinciden.'))

if __name__ == '__main__':
    unittest.main()