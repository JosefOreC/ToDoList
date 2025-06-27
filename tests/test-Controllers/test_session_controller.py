import unittest
from unittest.mock import patch, MagicMock
from src.controlador.session_controller import SessionController

class TestSessionController(unittest.TestCase):

    @patch('src.controlador.session_controller.SessionManager')
    def test_get_alias_user(self, MockSessionManager):
        mock_usuario = MagicMock()
        mock_usuario.Alias = "usuario_test"
        MockSessionManager.get_instance.return_value.usuario = mock_usuario

        alias = SessionController.get_alias_user()
        self.assertEqual(alias, "usuario_test")

    @patch('src.controlador.session_controller.SessionManager')
    def test_get_grupos_session_manager(self, MockSessionManager):
        mock_usuario = MagicMock()
        mock_usuario.grupos_relacion = ["Grupo1", "Grupo2"]
        MockSessionManager.get_instance.return_value.usuario = mock_usuario

        grupos = SessionController.get_grupos_session_manager()
        self.assertEqual(grupos, ["Grupo1", "Grupo2"])

    @patch('src.controlador.session_controller.SessionManager')
    def test_get_grupos_master_session_manager(self, MockSessionManager):
        mock_usuario = MagicMock()
        mock_usuario.grupos_master = ["Master1"]
        MockSessionManager.get_instance.return_value.usuario = mock_usuario

        grupos_master = SessionController.get_grupos_master_session_manager()
        self.assertEqual(grupos_master, ["Master1"])

    @patch('src.controlador.session_controller.SessionManager')
    def test_get_tasks_session_manager(self, MockSessionManager):
        mock_usuario = MagicMock()
        mock_usuario.usuario_tareas = ["Tarea1", "Tarea2"]
        MockSessionManager.get_instance.return_value.usuario = mock_usuario

        tareas = SessionController.get_tasks_session_manager()
        self.assertEqual(tareas, ["Tarea1", "Tarea2"])

if __name__ == '__main__':
    unittest.main()
