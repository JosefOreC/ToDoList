import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.modelo.service.task_service.task_finder import TaskFinder


class TestTaskFinder(unittest.TestCase):

    @patch("src.modelo.service.task_service.task_finder.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_finder.session")
    def test_search_for_task_by(self, mock_session, mock_convertir_date):
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_query.join.return_value = mock_filter
        mock_filter.filter.return_value.all.return_value = [("mocked_result",)]

        mock_session.query.return_value = mock_query
        mock_convertir_date.side_effect = lambda x: date(2025, 7, 3)

        result = TaskFinder.search_for_task_by(
            id_usuario=1,
            id_grupo=2,
            nombre="Tarea",
            realizado=True,
            fecha_ini="2025-07-01",
            fecha_fin="2025-07-05",
            archivado=False,
            prioridad=[1, 2]
        )

        self.assertEqual(result, [("mocked_result",)])
        self.assertTrue(mock_session.query.called)
        self.assertTrue(mock_filter.filter.called)
        self.assertTrue(mock_convertir_date.called)

if __name__ == "__main__":
    unittest.main()
