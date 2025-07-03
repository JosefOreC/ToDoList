import unittest
from unittest.mock import patch, MagicMock
import bcrypt
from src.modelo.service.auth_service.recover_password import RecoverPassword


class TestRecoverPassword(unittest.TestCase):

    @patch('src.modelo.service.auth_service.recover_password.DataFormat')
    @patch('src.modelo.service.auth_service.recover_password.UserServiceData')
    def test_recover_basic_data_user(self, mock_user_service_data, mock_data_format):
        mock_user_service_data.recover_basic_data_user.return_value = 'raw_data'
        mock_data_format.convert_to_dict_basic_data_user.return_value = {'respuesta': 'hashed_answer'}

        rp = RecoverPassword('usuario1')

        mock_user_service_data.recover_basic_data_user.assert_called_once_with('usuario1')
        mock_data_format.convert_to_dict_basic_data_user.assert_called_once_with('raw_data')
        self.assertEqual(rp.data_basic, {'respuesta': 'hashed_answer'})

    @patch('src.modelo.service.auth_service.recover_password.DataFormat')
    @patch('src.modelo.service.auth_service.recover_password.UserServiceData')
    def test_is_answer_correct_true(self, mock_user_service_data, mock_data_format):
        # Generar un hash válido para 'respuesta'
        original_answer = 'respuesta'
        hashed = bcrypt.hashpw(original_answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        mock_user_service_data.recover_basic_data_user.return_value = 'raw_data'
        mock_data_format.convert_to_dict_basic_data_user.return_value = {'respuesta': hashed}

        rp = RecoverPassword('usuario1')
        self.assertTrue(rp.is_answer_correct(original_answer))

    @patch('src.modelo.service.auth_service.recover_password.DataFormat')
    @patch('src.modelo.service.auth_service.recover_password.UserServiceData')
    def test_is_answer_correct_false(self, mock_user_service_data, mock_data_format):
        # Generar un hash válido para 'respuesta'
        hashed = bcrypt.hashpw(b'respuesta', bcrypt.gensalt()).decode('utf-8')

        mock_user_service_data.recover_basic_data_user.return_value = 'raw_data'
        mock_data_format.convert_to_dict_basic_data_user.return_value = {'respuesta': hashed}

        rp = RecoverPassword('usuario1')
        self.assertFalse(rp.is_answer_correct('otrarespuesta'))

    @patch('src.modelo.service.auth_service.recover_password.UserServiceData')
    @patch('src.modelo.service.auth_service.recover_password.DataFormat')
    def test_change_password(self, mock_data_format, mock_user_service_data):
        mock_user_service_data.recover_basic_data_user.return_value = 'raw_data'
        mock_data_format.convert_to_dict_basic_data_user.return_value = {'respuesta': 'respuesta_hashed'}

        rp = RecoverPassword('usuario1')
        rp.change_password('nueva_contraseña')

        mock_user_service_data.update_user.assert_called_once_with('usuario1', password='nueva_contraseña')


if __name__ == '__main__':
    unittest.main()
