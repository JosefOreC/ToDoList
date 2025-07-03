import unittest
from unittest.mock import patch, MagicMock
from src.controlador.main_view_controller import MainViewController


class TestMainViewController(unittest.TestCase):

    @patch('src.controlador.main_view_controller.SessionManager')
    def test_log_out(self, mock_session_manager):
        # Simulamos el cierre de sesión
        result = MainViewController.log_out()
        mock_session_manager.log_out.assert_called_once()
        self.assertTrue(result[0])
        self.assertEqual(result[1], 'Se cerró sesión con exito')

    @patch('src.controlador.main_view_controller.DataFormat.convert_to_dict_task_data')
    @patch('src.controlador.main_view_controller.TaskController.recover_tasks_today')
    def test_recover_task_today_with_format(self, mock_recover_today, mock_format):
        mock_recover_today.return_value = {
            'success': True,
            'response': 'Tareas recuperadas',
            'data': {'tareas': ['mock_task_data']}
        }
        mock_format.return_value = ['formatted_task_data']

        response = MainViewController.recover_task_today_with_format()
        mock_format.assert_called_once_with(['mock_task_data'])
        self.assertEqual(response['data']['tareas'], ['formatted_task_data'])

    @patch('src.controlador.main_view_controller.DataFormat.convert_to_dict_task_data')
    @patch('src.controlador.main_view_controller.TaskController.recover_task_date')
    def test_recover_task_for_date(self, mock_recover_date, mock_format):
        mock_recover_date.return_value = {
            'success': True,
            'response': 'Tareas de la fecha recuperadas',
            'data': {'tareas': ['raw_task']}
        }
        mock_format.return_value = ['formatted_task']

        response = MainViewController.recover_task_for_date("2025-06-27")
        mock_format.assert_called_once_with(['raw_task'])
        self.assertEqual(response['data']['tareas'], ['formatted_task'])

    @patch('src.controlador.main_view_controller.DataFormat.convert_to_dict_task_data')
    @patch('src.controlador.main_view_controller.TaskController.recover_task_archivate')
    def test_recover_task_archivade(self, mock_archivate, mock_format):
        mock_archivate.return_value = {
            'success': True,
            'response': 'Tareas archivadas recuperadas',
            'data': {'tareas': ['archived_task']}
        }
        mock_format.return_value = ['formatted_archived']

        response = MainViewController.recover_task_archivade()
        mock_format.assert_called_once_with(['archived_task'])
        self.assertEqual(response['data']['tareas'], ['formatted_archived'])


if __name__ == '__main__':
    unittest.main()
