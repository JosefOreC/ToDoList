import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Agregar el directorio src al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controlador.task_controller import TaskController

class TestTaskController(unittest.TestCase):

    @patch('controlador.task_controller.RegisterTask')
    @patch('controlador.task_controller.DataFormat')
    @patch('controlador.task_controller.SessionManager')
    def test_register_task_success(self, mock_session_manager, mock_data_format, mock_register_task):
        mock_data_format.convertir_fecha.return_value = "2023-10-01"
        mock_session_manager.get_instance.return_value.usuario.IDUsuario = 1
        mock_register_task.return_value.register_task.return_value = (True, "Tarea registrada con éxito")

        result = TaskController.event_register_task_user("Tarea de prueba", "2023-10-01", 3, "Detalles de la tarea")
        self.assertEqual(result, (True, "Tarea registrada con éxito"))

    @patch('controlador.task_controller.DataFormat')
    @patch('controlador.task_controller.SessionManager')
    def test_register_task_invalid_priority(self, mock_session_manager, mock_data_format):
        mock_data_format.convertir_fecha.return_value = "2023-10-01"
        mock_session_manager.get_instance.return_value.usuario.IDUsuario = 1

        result = TaskController.event_register_task_user("Tarea de prueba", "2023-10-01", 6, "Detalles de la tarea")
        self.assertEqual(result, (False, "Prioridad no válida, tiene que estar el 1 al 5."))

    @patch('controlador.task_controller.RegisterTask')
    @patch('controlador.task_controller.DataFormat')
    @patch('controlador.task_controller.SessionManager')
    def test_register_task_missing_fields(self, mock_session_manager, mock_data_format, mock_register_task):
        mock_data_format.convertir_fecha.return_value = "2023-10-01"
        mock_session_manager.get_instance.return_value.usuario.IDUsuario = 1
        mock_register_task.return_value.register_task.return_value = (False, "No se puede dejar vació ningún campo.")

        result = TaskController.event_register_task_user("", "2023-10-01", 3, "")
        self.assertEqual(result, (False, "No se puede dejar vació ningún campo."))

    @patch('controlador.task_controller.DataFormat')
    @patch('controlador.task_controller.SessionManager')
    def test_register_task_invalid_date(self, mock_session_manager, mock_data_format):
        mock_data_format.convertir_fecha.side_effect = Exception("Error Formato de fecha no soportado")
        mock_session_manager.get_instance.return_value.usuario.IDUsuario = 1

        result = TaskController.event_register_task_user("Tarea de prueba", "invalid-date", 3, "Detalles de la tarea")
        self.assertEqual(result[0], False)
        self.assertIn("Fecha no valida", result[1])

    @patch('controlador.task_controller.SessionManager')
    def test_event_update_task_user(self, mock_session_manager):
        mock_session_manager.get_instance.return_value.usuario.IDUsuario = 1

        with patch('controlador.task_controller.TaskServiceData.update_task_user') as mock_update:
            result = TaskController.event_update_task_user(1, 1, nombre="Tarea Actualizada")
            self.assertEqual(result, (True, 'Se guardaron los cambiós con exito'))
            mock_update.assert_called_once()

    @patch('controlador.task_controller.SessionManager')
    def test_event_delete_task(self, mock_session_manager):
        mock_session_manager.get_instance.return_value.usuario.IDUsuario = 1

        with patch('controlador.task_controller.TaskServiceData.soft_delete_task') as mock_delete:
            result = TaskController.event_delete_task(1)
            self.assertEqual(result, (True, "Tarea eliminada"))
            mock_delete.assert_called_once_with(id_tarea=1)

if __name__ == '__main__':
    unittest.main()