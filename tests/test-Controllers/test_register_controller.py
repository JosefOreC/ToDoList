import unittest
from unittest.mock import patch, MagicMock
from src.controlador.register_controller import RegisterUserController

class TestRegisterUserController(unittest.TestCase):

    def test_campos_vacios(self):
        result, message = RegisterUserController.register_user(
            "", "", "", "", "", "", ""
        )
        self.assertFalse(result)
        self.assertEqual(message, 'Tiene que rellenar todos los campos.')

    def test_contrasenas_no_coinciden(self):
        result, message = RegisterUserController.register_user(
            "Juan", "Pérez", "juan123", "pass123", "otra_pass", "Color favorito?", "Azul"
        )
        self.assertFalse(result)
        self.assertEqual(message, 'Las contraseñas no coinciden.')

    @patch('src.controlador.register_controller.RegisterUser')
    def test_registro_exitoso(self, MockRegisterUser):
        # Configurar el mock
        mock_register_instance = MagicMock()
        mock_register_instance.register_user.return_value = (True, "Usuario registrado exitosamente.")
        MockRegisterUser.return_value = mock_register_instance

        result, message = RegisterUserController.register_user(
            "Ana", "López", "ana2025", "securePass", "securePass", "Mascota favorita?", "Toby"
        )
        self.assertTrue(result)
        self.assertEqual(message, "Usuario registrado exitosamente.")
        MockRegisterUser.assert_called_once()  # Se asegura de que se haya llamado
        mock_register_instance.register_user.assert_called_once()

if __name__ == '__main__':
    unittest.main()
