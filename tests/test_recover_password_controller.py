import unittest
from unittest.mock import patch, MagicMock
from src.controlador.recover_password_controller import RecoverPasswordController


class TestRecoverPasswordController(unittest.TestCase):

    @patch('src.controlador.recover_password_controller.RecoverPassword')
    def test_start_recover_password_success(self, mock_recover_password):
        # Simula el atributo data_basic del objeto
        mock_instance = MagicMock()
        mock_instance.data_basic = {'alias': 'user1', 'respuesta': 'azul', 'pregunta': 'color favorito'}
        mock_recover_password.return_value = mock_instance

        response = RecoverPasswordController.start_recover_password("user1")

        self.assertTrue(response['success'])
        self.assertEqual(response['data'], mock_instance.data_basic)

    @patch('src.controlador.recover_password_controller.RecoverPassword', side_effect=Exception("Error"))
    def test_start_recover_password_error(self, _):
        response = RecoverPasswordController.start_recover_password("user_error")

        self.assertFalse(response['success'])
        self.assertIn("No se pudieron recuperar los datos", response['response'])

    def test_is_response_correct_success(self):
        # Preparar instancia simulada
        mock_instance = MagicMock()
        mock_instance.is_answer_correct.return_value = True
        RecoverPasswordController._RecoverPasswordController__recuperacion = mock_instance

        response = RecoverPasswordController.is_response_correct("azul")

        self.assertTrue(response['success'])
        self.assertTrue(response['data']['success'])
        self.assertEqual(response['data']['result'], "Respuesta correcta.")

    def test_is_response_correct_failure(self):
        # Simula excepción en el método
        mock_instance = MagicMock()
        mock_instance.is_answer_correct.side_effect = Exception("Error")
        RecoverPasswordController._RecoverPasswordController__recuperacion = mock_instance

        response = RecoverPasswordController.is_response_correct("incorrecta")

        self.assertFalse(response['success'])
        self.assertFalse(response['data']['success'])
        self.assertEqual(response['data']['result'], "Respuesta incorrecta.")

    def test_change_password_success(self):
        mock_instance = MagicMock()
        RecoverPasswordController._RecoverPasswordController__recuperacion = mock_instance

        response = RecoverPasswordController.change_password("nueva", "nueva")

        self.assertTrue(response['success'])
        self.assertEqual(response['response'], "Se cambió la contraseña.")
        self.assertIsNone(RecoverPasswordController._RecoverPasswordController__recuperacion)

    def test_change_password_empty_fields(self):
        response = RecoverPasswordController.change_password("", "")
        self.assertFalse(response['success'])
        self.assertIn("campos vacios", response['response'])

    def test_change_password_exception(self):
        mock_instance = MagicMock()
        mock_instance.change_password.side_effect = Exception("Fallo")
        RecoverPasswordController._RecoverPasswordController__recuperacion = mock_instance

        response = RecoverPasswordController.change_password("pass", "pass")
        self.assertFalse(response['success'])
        self.assertIn("No se pudo cambiar la contraseña", response['response'])
        self.assertIsNone(RecoverPasswordController._RecoverPasswordController__recuperacion)


if __name__ == '__main__':
    unittest.main()
