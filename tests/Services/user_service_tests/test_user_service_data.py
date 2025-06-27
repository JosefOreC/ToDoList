import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError
from src.modelo.entities.modelo import Usuario
from src.modelo.service.user_service.user_service_data import UserServiceData

class TestUserServiceData(unittest.TestCase):

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_recover_user_for_alias(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = Usuario(IDUsuario=1, Alias='test_alias')

        usuario = UserServiceData.recover_user_for_alias('test_alias')

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.Alias, 'test_alias')

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_get_user_for_id_user(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = Usuario(IDUsuario=1, Alias='test_alias')

        usuario = UserServiceData.get_user_for_id_user(1)

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.IDUsuario, 1)

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_recover_id_user_for_alias(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = (1,)

        id_usuario = UserServiceData.recover_id_user_for_alias('test_alias')

        self.assertEqual(id_usuario, 1)

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_is_user_with_alias_exists(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = 1

        exists = UserServiceData.is_user_with_alias_exits('test_alias')

        self.assertTrue(exists)

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_insert_new_user(self, mock_session):
        mock_session.add_all = MagicMock()
        mock_session.commit = MagicMock()

        usuario = Usuario(IDUsuario=1, Alias='test_alias')

        UserServiceData.insert_new_user(usuario)

        mock_session.add_all.assert_called()
        mock_session.commit.assert_called()

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_insert_new_user_integrity_error(self, mock_session):
        mock_session.add_all = MagicMock()
        mock_session.commit = MagicMock(side_effect=IntegrityError('Integrity error', params=None, orig=None))
        mock_session.rollback = MagicMock()

        usuario = Usuario(IDUsuario=1, Alias='test_alias')

        with self.assertRaises(Exception) as context:
            UserServiceData.insert_new_user(usuario)

        self.assertEqual(str(context.exception), "El alias ya está ocupado.")
        mock_session.rollback.assert_called()

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_update_user(self, mock_session):
        mock_session.commit = MagicMock()

        usuario = Usuario(IDUsuario=1, Alias='test_alias', Nombres='Antiguo Nombre')  # Crear un objeto Usuario
        UserServiceData.update_user(usuario, nombres='Nuevo Nombre')

        self.assertEqual(usuario.Nombres, 'Nuevo Nombre')  # Verifica que el nombre se haya actualizado
        mock_session.commit.assert_called()

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_update_user_integrity_error(self, mock_session):
        mock_session.commit = MagicMock(side_effect=IntegrityError('Integrity error', params=None, orig=None))
        mock_session.rollback = MagicMock()

        usuario = Usuario(IDUsuario=1, Alias='test_alias')

        with self.assertRaises(Exception) as context:
            UserServiceData.update_user(usuario, alias='nuevo_alias')

        self.assertEqual(str(context.exception), "El alias ya está ocupado.")
        mock_session.rollback.assert_called()

    @patch('src.modelo.service.user_service.user_service_data.session')
    def test_soft_delete_user(self, mock_session):
        mock_session.commit = MagicMock()
        usuario = Usuario(IDUsuario=1, Estado=True)
        mock_session.query.return_value.filter_by.return_value.first.return_value = usuario

        UserServiceData.soft_delete_user(1)

        self.assertFalse(usuario.Estado)  # Verifica que el estado del usuario se haya cambiado a False
        mock_session.commit.assert_called()

if __name__ == '__main__':
    unittest.main()