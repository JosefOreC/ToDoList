import unittest
from unittest.mock import patch, MagicMock
from src.controlador.group_controller import GroupController


class TestGroupController(unittest.TestCase):

    @patch('src.controlador.group_controller.SessionManager.get_instance')
    @patch('src.controlador.group_controller.RegisterGroup')
    @patch('src.controlador.group_controller.UserServiceData.recover_id_user_for_alias')
    def test_register_group_success(self, mock_recover_id, mock_register_group_class, mock_session_manager):
        # Simular sesión del usuario
        mock_session_manager.return_value.usuario.IDUsuario = 1

        # Simular IDs de usuarios recuperados
        mock_recover_id.side_effect = [2, 3]

        # Simular instancia de RegisterGroup
        mock_register_instance = MagicMock()
        mock_register_group_class.return_value = mock_register_instance

        result = GroupController.register_group(
            nombre="Grupo de prueba",
            descripcion="Descripción de prueba",
            miembros_alias=["usuario1", "usuario2"]
        )

        self.assertEqual(result, (True, "Se agregó el grupo con éxito"))
        mock_register_instance.register_group.assert_called_once()

    @patch('src.controlador.group_controller.UserServiceData.is_user_with_alias_exits')
    @patch('src.controlador.group_controller.SessionManager.get_instance')
    def test_is_user_exits_same_user(self, mock_session_manager, mock_is_user):
        mock_session_manager.return_value.usuario.Alias = 'mi_alias'
        result = GroupController.is_user_exits('mi_alias')
        self.assertFalse(result[0])
        self.assertIn('porque es el que está creando el grupo', result[1])

    @patch('src.controlador.group_controller.UserServiceData.is_user_with_alias_exits')
    @patch('src.controlador.group_controller.SessionManager.get_instance')
    def test_is_user_exits_found(self, mock_session_manager, mock_is_user):
        mock_session_manager.return_value.usuario.Alias = 'master'
        mock_is_user.return_value = True
        result = GroupController.is_user_exits('otro_alias')
        self.assertTrue(result[0])
        self.assertEqual(result[1], "Usuario existente.")

    @patch('src.controlador.group_controller.UserServiceData.is_user_with_alias_exits')
    @patch('src.controlador.group_controller.SessionManager.get_instance')
    def test_is_user_exits_not_found(self, mock_session_manager, mock_is_user):
        mock_session_manager.return_value.usuario.Alias = 'master'
        mock_is_user.return_value = False
        result = GroupController.is_user_exits('otro_alias')
        self.assertFalse(result[0])
        self.assertEqual(result[1], "Usuario no existente.")


if __name__ == '__main__':
    unittest.main()
