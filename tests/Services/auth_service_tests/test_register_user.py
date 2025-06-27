import unittest
from unittest.mock import patch, MagicMock
from src.modelo.service.auth_service.register_user import RegisterUser


class TestRegisterUser(unittest.TestCase):

    @patch('src.modelo.service.auth_service.register_user.UserServiceData')
    def test_register_user_alias_exists(self, mock_user_service_data):
        mock_user = MagicMock()
        mock_user.Alias = 'usuario1'

        # Simular que el alias ya existe
        mock_user_service_data.is_user_with_alias_exits.return_value = True

        reg = RegisterUser(mock_user)
        result = reg.register_user()

        self.assertEqual(result, (False, 'Alias ocupado.'))
        mock_user_service_data.is_user_with_alias_exits.assert_called_once_with('usuario1')

    @patch('src.modelo.service.auth_service.register_user.UserServiceData')
    def test_register_user_success(self, mock_user_service_data):
        mock_user = MagicMock()
        mock_user.Alias = 'usuario2'

        # Simular que el alias NO existe y que no lanza excepciones
        mock_user_service_data.is_user_with_alias_exits.return_value = False

        reg = RegisterUser(mock_user)
        result = reg.register_user()

        self.assertEqual(result, (True, "SE GUARDÓ AL NUEVO USUARIO"))
        mock_user_service_data.insert_new_user.assert_called_once_with(mock_user)

    @patch('src.modelo.service.auth_service.register_user.UserServiceData')
    def test_register_user_insert_exception(self, mock_user_service_data):
        mock_user = MagicMock()
        mock_user.Alias = 'usuario3'

        mock_user_service_data.is_user_with_alias_exits.return_value = False
        mock_user_service_data.insert_new_user.side_effect = Exception("DB error")

        reg = RegisterUser(mock_user)
        result = reg.register_user()

        self.assertEqual(result[0], False)
        self.assertIsInstance(result[1], Exception)
        self.assertEqual(str(result[1]), "DB error")

if __name__ == '__main__':
    unittest.main()
