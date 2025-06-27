import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.modelo.entities.modelo import Tarea, UsuarioTarea
from src.modelo.service.task_service.task_service_data import TaskServiceData

class TestTaskServiceData(unittest.TestCase):

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_insert_task_user(self, mock_session):
        mock_tarea = Tarea(IDTarea=1)
        relaciones = [UsuarioTarea(IDUsuario=1), UsuarioTarea(IDUsuario=2)]

        TaskServiceData.insert_task_user(mock_tarea, relaciones)

        mock_session.add_all.assert_any_call([mock_tarea])
        for relacion in relaciones:
            self.assertEqual(relacion.IDTarea, mock_tarea.IDTarea)
        mock_session.add_all.assert_called_with(relaciones)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.UpdateTask")
    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_update_task_user(self, mock_session, mock_update_task):
        updater = MagicMock()
        mock_update_task.return_value = updater

        TaskServiceData.update_task_user(1, 1, nombre="Test", realizado=True)

        updater.update_name.assert_called_with("Test")
        updater.update_realizado.assert_called_with(True)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_delete_relation_task(self, mock_session):
        mock_instance = MagicMock()
        mock_session.query().filter_by().first.return_value = mock_instance

        TaskServiceData.delete_relation_task(1, 1)

        mock_session.delete.assert_called_with(mock_instance)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_tasks_user_list_date_invalid_range(self, mock_session, mock_convert):
        mock_convert.side_effect = lambda x: date(2024, 1, 2) if x == "2024-01-02" else date(2024, 1, 1)
        with self.assertRaises(Exception):
            TaskServiceData.get_tasks_user_list_date(1, "2024-01-02", "2024-01-01")

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_task(self, mock_session):
        TaskServiceData.get_task(1)
        mock_session.query().filter_by.assert_called_with(IDTarea=1)

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_relations_of_task(self, mock_session):
        TaskServiceData.get_relations_of_task(1)
        mock_session.query().filter_by.assert_called_with(IDTarea=1)

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_id_group_of_task(self, mock_session):
        mock_session.query().filter_by().first.return_value = [5]
        grupo_id = TaskServiceData.get_id_group_of_task(1)
        self.assertEqual(grupo_id, 5)

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_is_editable_task_for_user(self, mock_session):
        mock_session.query().filter_by().first.return_value = [True]
        result = TaskServiceData.is_editable_task_for_user(1, 1)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
