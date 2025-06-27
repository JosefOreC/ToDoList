import unittest
from unittest.mock import patch, MagicMock
from src.controlador.user_controller import UserController

class TestUserController(unittest.TestCase):

    @patch('src.controlador.user_controller.SessionManager')
    @patch('src.controlador.user_controller.UserServiceData.update_user')
    def test_event_update_user_success(self, mock_update_user, mock_session_manager):
        usuario_mock = MagicMock()
        mock_session_manager.get_instance.return_value.usuario = usuario_mock

        result, message = UserController.event_update_user(nombres="Juan", apellidos="Perez")
        self.assertTrue(result)
        self.assertEqual(message, 'Se guardaron los cambios.')
        mock_update_user.assert_called_once()

    @patch('src.controlador.user_controller.UserServiceData.update_user', side_effect=Exception("Error"))
    @patch('src.controlador.user_controller.SessionManager')
    def test_event_update_user_failure(self, mock_session_manager, mock_update_user):
        usuario_mock = MagicMock()
        mock_session_manager.get_instance.return_value.usuario = usuario_mock

        result, message = UserController.event_update_user(nombres="Juan")
        self.assertFalse(result)
        self.assertIn("No se pudieron guardar los cambios", message)

    def test_event_update_user_no_changes(self):
        result, message = UserController.event_update_user()
        self.assertFalse(result)
        self.assertEqual(message, "No se hizo ningún cambio")

    @patch('src.controlador.user_controller.SessionManager')
    def test_get_data_session_manager(self, mock_session_manager):
        mock_session_manager.get_instance.return_value.get_data.return_value = {"alias": "juan"}
        data = UserController.get_data_session_manager()
        self.assertEqual(data["alias"], "juan")

if __name__ == '__main__':
    unittest.main()
