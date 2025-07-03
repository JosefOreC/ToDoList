import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.modelo.service.task_service.task_finder import TaskFinder


class TestTaskFinder(unittest.TestCase):

    @patch("src.modelo.service.task_service.task_finder.session.query")
    def test_search_by_name(self, mock_query):
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = ["resultado"]
        result = TaskFinder.search_for_tasks_by_name(1, "test")
        self.assertEqual(result, ["resultado"])

    @patch("src.modelo.service.task_service.task_finder.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_finder.session.query")
    def test_search_by_date(self, mock_query, mock_convert):
        mock_convert.side_effect = lambda x: date(2024, 1, 1)
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = ["tarea"]
        result = TaskFinder.search_for_task_by_date(1, "2024-01-01")
        self.assertEqual(result, ["tarea"])

    @patch("src.modelo.service.task_service.task_finder.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_finder.session.query")
    def test_search_by_date_and_name(self, mock_query, mock_convert):
        mock_convert.side_effect = lambda x: date(2024, 2, 1)
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = ["filtrado"]
        result = TaskFinder.search_for_task_by_date_and_name(1, "Plan", "2024-02-01")
        self.assertEqual(result, ["filtrado"])

    @patch("src.modelo.service.task_service.task_finder.session.query")
    def test_search_by_check(self, mock_query):
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = ["hecho"]
        result = TaskFinder.search_for_task_by_check(1, True)
        self.assertEqual(result, ["hecho"])

    @patch("src.modelo.service.task_service.task_finder.session.query")
    def test_search_by_check_and_name(self, mock_query):
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = ["checkname"]
        result = TaskFinder.search_for_task_by_check_name(1, "report", False)
        self.assertEqual(result, ["checkname"])

    @patch("src.modelo.service.task_service.task_finder.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_finder.session.query")
    def test_search_by_check_and_date(self, mock_query, mock_convert):
        mock_convert.side_effect = lambda x: date(2024, 3, 1)
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = ["checkdate"]
        result = TaskFinder.search_for_task_by_check_date(1, True, "2024-03-01")
        self.assertEqual(result, ["checkdate"])

    @patch("src.modelo.service.task_service.task_finder.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_finder.session.query")
    def test_search_by_group_and_date_name_check(self, mock_query, mock_convert):
        mock_convert.side_effect = lambda x: date(2024, 4, 1)
        mock_query.return_value.join.return_value.filter.return_value.all.return_value = ["grouped"]
        result = TaskFinder.search_for_task_by_check_date_name_group(1, 2, "proyecto", True, "2024-04-01")
        self.assertEqual(result, ["grouped"])

    def test_missing_date_exception(self):
        with self.assertRaises(Exception) as context:
            TaskFinder.search_for_task_by_date(1)
        self.assertIn("No existen los datos necesarios para la busqueda", str(context.exception))

    @patch('src.modelo.service.task_service.task_finder.session')
    @patch('src.modelo.service.task_service.task_finder.DataFormat.convertir_data_to_date')
    def test_search_success_with_both_dates(self, mock_convert_date, mock_session):
        mock_convert_date.side_effect = lambda x: x  # Simula que devuelve la fecha tal cual
        mock_query = MagicMock()
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = ['result']

        result = TaskFinder.search_for_task_by_check_date_name(
            id_usuario=1,
            nombre="Tarea",
            realizado=True,
            fecha_ini=date(2025, 7, 1),
            fecha_fin=date(2025, 7, 3),
            archivado=False
        )

        self.assertEqual(result, ['result'])
        mock_convert_date.assert_any_call(date(2025, 7, 1))
        mock_convert_date.assert_any_call(date(2025, 7, 3))

    def test_search_fail_missing_dates(self):
        with self.assertRaises(Exception) as context:
            TaskFinder.search_for_task_by_check_date_name(
                id_usuario=1,
                nombre="Tarea",
                realizado=False,
                fecha_ini=None,
                fecha_fin=None
            )
        self.assertIn("No existen los datos necesarios", str(context.exception))

if __name__ == "__main__":
    unittest.main()
