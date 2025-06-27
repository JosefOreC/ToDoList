import unittest
from unittest.mock import patch, MagicMock
from src.modelo.service.auth_service.login import LoginIn

class TestLoginIn(unittest.TestCase):

    @patch('src.modelo.service.auth_service.login.UserServiceData')
    @patch('src.modelo.service.auth_service.login.SessionManager')
    def test_login_user_not_exists(self, mock_session_manager, mock_user_service_data):
        mock_user_service_data.is_user_with_alias_exits.return_value = False

        login = LoginIn('fakeuser', '1234')
        result = login.process_login()

        self.assertEqual(result, (False, "EL USUARIO NO EXISTE"))
        mock_session_manager.log_out.assert_called_once()

    @patch('src.modelo.service.auth_service.login.UserServiceData')
    @patch('src.modelo.service.auth_service.login.SessionManager')
    def test_login_wrong_password(self, mock_session_manager, mock_user_service_data):
        mock_user_service_data.is_user_with_alias_exits.return_value = True
        mock_user = MagicMock()
        mock_user_service_data.recover_user_for_alias.return_value = mock_user

        mock_instance = MagicMock()
        mock_instance.validar_usuario.return_value = False
        mock_session_manager.get_instance.return_value = mock_instance

        login = LoginIn('validuser', 'wrongpass')
        result = login.process_login()

        self.assertEqual(result, (False, "CONTRASEÑA INCORRECTA"))
        mock_session_manager.log_out.assert_called()

    @patch('src.modelo.service.auth_service.login.UserServiceData')
    @patch('src.modelo.service.auth_service.login.SessionManager')
    def test_login_successful(self, mock_session_manager, mock_user_service_data):
        mock_user_service_data.is_user_with_alias_exits.return_value = True
        mock_user = MagicMock()
        mock_user_service_data.recover_user_for_alias.return_value = mock_user

        mock_instance = MagicMock()
        mock_instance.validar_usuario.return_value = True
        mock_session_manager.get_instance.return_value = mock_instance

        login = LoginIn('validuser', 'correctpass')
        result = login.process_login()

        self.assertEqual(result, (True, "USER LOGIN SUCCESSFUL"))
        mock_session_manager.log_out.assert_called_once()

if __name__ == '__main__':
    unittest.main()