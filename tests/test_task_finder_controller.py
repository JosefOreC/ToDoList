import unittest
from unittest.mock import patch, MagicMock
from src.controlador.task_controller import TaskController
from datetime import date

class TestTaskController(unittest.TestCase):

    @patch('src.controlador.task_controller.TaskServiceData.get_tasks_session_user_list_today')
    def test_recover_tasks_today_success(self, mock_get_tasks):
        mock_get_tasks.return_value = ['Tarea 1', 'Tarea 2']
        response = TaskController.recover_tasks_today()
        self.assertTrue(response['success'])
        self.assertEqual(response['data']['tareas'], ['Tarea 1', 'Tarea 2'])

    @patch('src.controlador.task_controller.RegisterTask')
    @patch('src.controlador.task_controller.DataFormat.convertir_data_to_date')
    def test_event_register_task_user_success(self, mock_convert_date, mock_register_task):
        mock_convert_date.return_value = date.today()
        mock_instance = MagicMock()
        mock_instance.register_task.return_value = (True, "Tarea registrada")
        mock_register_task.return_value = mock_instance

        result, message = TaskController.event_register_task_user(
            "Comprar pan", "2025-07-01", 3, "Ir a la panadería"
        )
        self.assertTrue(result)
        self.assertEqual(message, "Tarea registrada")

    @patch('src.controlador.task_controller.DataFormat.convertir_data_to_date')
    def test_create_tarea_prioridad_fuera_de_rango(self, mock_convert_date):
        mock_convert_date.return_value = date.today()
        success, result = TaskController._TaskController__create_tarea(
            "Tarea X", "2025-06-30", 6, "Detalle"
        )
        self.assertFalse(success)
        self.assertIn("Prioridad no válida", result)

    @patch('src.controlador.task_controller.DataFormat.convertir_data_to_date')
    def test_validar_datos_correctos(self, mock_convert_date):
        mock_convert_date.return_value = date.today()
        result, msg = TaskController.validar_datos("2025-07-01", 4)
        self.assertTrue(result)
        self.assertEqual(msg, "Datos validos")

    @patch('src.controlador.task_controller.DataFormat.convertir_data_to_date')
    def test_validar_datos_prioridad_incorrecta(self, mock_convert_date):
        mock_convert_date.return_value = date.today()
        result, msg = TaskController.validar_datos("2025-07-01", "invalida")
        self.assertFalse(result)
        self.assertIn("invalid literal", str(msg))  # msg es Exception

if __name__ == '__main__':
    unittest.main()
