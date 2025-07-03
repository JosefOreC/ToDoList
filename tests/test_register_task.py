import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.modelo.service.task_service.register_task import RegisterTask
from src.modelo.entities.tarea import Tarea


class TestRegisterTask(unittest.TestCase):

    def setUp(self):
        self.fake_task = Tarea(IDTarea=1, Nombre="Test", Fecha_programada=date.today(), Prioridad=2,
                               Detalle="Detalles", Activo=True)

    @patch("src.modelo.service.task_service.register_task.SessionManager.get_instance")
    @patch("src.modelo.service.task_service.register_task.TaskServiceData.insert_task_user")
    def test_register_individual_task(self, mock_insert, mock_session):
        mock_user = MagicMock()
        mock_user.usuario.IDUsuario = 5
        mock_session.return_value = mock_user
        mock_insert.return_value = None

        rt = RegisterTask(tarea=self.fake_task)
        result = rt.register_task()

        self.assertTrue(result[0])
        self.assertEqual(len(rt.relaciones), 1)
        self.assertEqual(rt.relaciones[0].IDUsuario, 5)

    @patch("src.modelo.service.task_service.register_task.GroupServiceData.get_all_members")
    @patch("src.modelo.service.task_service.register_task.TaskServiceData.insert_task_user")
    def test_register_group_task_all(self, mock_insert, mock_get_members):
        mock_get_members.return_value = [1, 2, 3]
        mock_insert.return_value = None

        rt = RegisterTask(tarea=self.fake_task, id_grupo=10, miembro_disponible='all')
        result = rt.register_task()

        self.assertTrue(result[0])
        self.assertEqual(len(rt.relaciones), 3)
        self.assertTrue(all(rel.Disponible for rel in rt.relaciones))

    @patch("src.modelo.service.task_service.register_task.TaskServiceData.insert_task_user")
    def test_register_group_task_custom(self, mock_insert):
        miembros = [[10, True], [11, False]]
        mock_insert.return_value = None

        rt = RegisterTask(tarea=self.fake_task, id_grupo=7, miembro_disponible=miembros)
        result = rt.register_task()

        self.assertTrue(result[0])
        self.assertEqual(len(rt.relaciones), 2)
        self.assertTrue(rt.relaciones[0].Disponible)
        self.assertFalse(rt.relaciones[1].Disponible)

    @patch("src.modelo.service.task_service.register_task.SessionManager.get_instance")
    @patch("src.modelo.service.task_service.register_task.TaskServiceData.insert_task_user", side_effect=Exception("DB Error"))
    def test_register_task_save_error(self, mock_insert, mock_session):
        mock_user = MagicMock()
        mock_user.usuario.IDUsuario = 8
        mock_session.return_value = mock_user

        rt = RegisterTask(tarea=self.fake_task)
        result = rt.register_task()

        self.assertFalse(result[0])
        self.assertEqual(str(result[1]), "DB Error")


if __name__ == "__main__":
    unittest.main()
