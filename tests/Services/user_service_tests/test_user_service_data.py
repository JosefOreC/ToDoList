import unittest
from unittest.mock import MagicMock, patch
from src.modelo.entities.modelo import Usuario
from src.modelo.service.user_service.update_user import UpdateUser


class TestUpdateUser(unittest.TestCase):

    def setUp(self):
        self.usuario_mock = MagicMock(spec=Usuario)
        self.usuario_mock.IDUsuario = 1
        self.usuario_mock.Nombres = "Juan"
        self.usuario_mock.Apellidos = "Perez"
        self.usuario_mock.Alias = "jperez"
        self.usuario_mock.Password = "hashed_pwd"
        self.usuario_mock.Estado = True

        # Parchar session.query para que devuelva el usuario mock
        patcher = patch("src.modelo.service.user_service.update_user.session.query")
        self.addCleanup(patcher.stop)
        self.mock_query = patcher.start()
        self.mock_query.return_value.filter_by.return_value.first.return_value = self.usuario_mock

    def test_update_nombres(self):
        updater = UpdateUser(self.usuario_mock)
        updater.update_nombres("Carlos")
        self.assertEqual(self.usuario_mock.Nombres, "Carlos")

    def test_update_apellidos(self):
        updater = UpdateUser(self.usuario_mock)
        updater.update_apellidos("Gomez")
        self.assertEqual(self.usuario_mock.Apellidos, "Gomez")

    def test_update_alias(self):
        updater = UpdateUser(self.usuario_mock)
        updater.update_alias("cgomez")
        self.assertEqual(self.usuario_mock.Alias, "cgomez")

    def test_update_estado(self):
        updater = UpdateUser(self.usuario_mock)
        updater.update_estado(False)
        self.assertFalse(self.usuario_mock.Estado)

    def test_update_password(self):
        updater = UpdateUser(self.usuario_mock)
        updater.update_password("nueva_clave")
        self.assertNotEqual(self.usuario_mock.Password, "nueva_clave")
        self.assertTrue(self.usuario_mock.Password.startswith("$2b$"))  # bcrypt hash prefix


if __name__ == '__main__':
    unittest.main()
