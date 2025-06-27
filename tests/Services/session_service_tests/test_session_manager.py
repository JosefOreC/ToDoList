import unittest
import bcrypt
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.entities.usuario import Usuario


class FakeUsuario:
    def __init__(self, id_usuario, nombres, apellidos, alias, password_claro):
        self.IDUsuario = id_usuario
        self.Nombres = nombres
        self.Apellidos = apellidos
        self.Alias = alias
        self.Password = bcrypt.hashpw(password_claro.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


class TestSessionManager(unittest.TestCase):

    def setUp(self):
        self.fake_user = FakeUsuario(
            id_usuario=42,
            nombres="Juan",
            apellidos="Pérez",
            alias="jperez",
            password_claro="secreto123"
        )
        SessionManager.log_out()

    def tearDown(self):
        SessionManager.log_out()

    def test_get_instance_creates_and_returns_singleton(self):
        sm1 = SessionManager.get_instance(self.fake_user)
        sm2 = SessionManager.get_instance()

        self.assertIs(sm1, sm2)
        self.assertEqual(sm1.usuario.IDUsuario, 42)

    def test_get_instance_raises_exception_without_user(self):
        with self.assertRaises(Exception) as cm:
            SessionManager.get_instance()

        self.assertIn("No existe un usuario logueado", str(cm.exception))

    def test_log_out_clears_instance(self):
        SessionManager.get_instance(self.fake_user)
        SessionManager.log_out()

        with self.assertRaises(Exception):
            SessionManager.get_instance()

    def test_get_password_returns_hashed_password(self):
        sm = SessionManager.get_instance(self.fake_user)
        self.assertTrue(sm.get_password().startswith("$2b$"))  # bcrypt hash prefix

    def test_validar_usuario_correct_password(self):
        sm = SessionManager.get_instance(self.fake_user)
        self.assertTrue(sm.validar_usuario("secreto123"))

    def test_validar_usuario_wrong_password(self):
        sm = SessionManager.get_instance(self.fake_user)
        self.assertFalse(sm.validar_usuario("incorrecto"))

    def test_get_id_user_returns_correct_id(self):
        SessionManager.get_instance(self.fake_user)
        self.assertEqual(SessionManager.get_id_user(), 42)

    def test_get_data_returns_user_info(self):
        sm = SessionManager.get_instance(self.fake_user)
        data = sm.get_data()

        self.assertEqual(data["nombres"], "Juan")
        self.assertEqual(data["apellidos"], "Pérez")
        self.assertEqual(data["alias"], "jperez")


if __name__ == '__main__':
    unittest.main()
