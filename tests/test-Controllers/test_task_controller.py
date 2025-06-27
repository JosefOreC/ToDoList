import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.controlador.task_controller import TaskController


class TestTaskController(unittest.TestCase):

    def setUp(self):
        # Configuración común para las pruebas
        self.mock_task_service = MagicMock()
        self.mock_data_format = MagicMock()
        self.mock_register_task = MagicMock()

        # Patches para los módulos externos
        self.patcher_task_service = patch('src.controlador.task_controller.TaskServiceData', self.mock_task_service)
        self.patcher_data_format = patch('src.controlador.task_controller.DataFormat', self.mock_data_format)
        self.patcher_register_task = patch('src.controlador.task_controller.RegisterTask', self.mock_register_task)

        self.patcher_task_service.start()
        self.patcher_data_format.start()
        self.patcher_register_task.start()

        self.addCleanup(self.patcher_task_service.stop)
        self.addCleanup(self.patcher_data_format.stop)
        self.addCleanup(self.patcher_register_task.stop)

    def test_recover_tasks_today_success(self):
        """Prueba la recuperación exitosa de tareas para hoy"""
        self.mock_task_service.get_tasks_session_user_list_today.return_value = ['Tarea 1', 'Tarea 2']

        response = TaskController.recover_tasks_today()

        self.assertTrue(response['success'])
        self.assertEqual(response['data']['tareas'], ['Tarea 1', 'Tarea 2'])
        self.mock_task_service.get_tasks_session_user_list_today.assert_called_once()

    def test_recover_tasks_today_empty(self):
        """Prueba cuando no hay tareas para hoy"""
        self.mock_task_service.get_tasks_session_user_list_today.return_value = []

        response = TaskController.recover_tasks_today()

        self.assertTrue(response['success'])
        self.assertEqual(response['data']['tareas'], [])

    def test_recover_tasks_today_error(self):
        """Prueba el manejo de errores al recuperar tareas"""
        self.mock_task_service.get_tasks_session_user_list_today.side_effect = Exception("Error de base de datos")

        response = TaskController.recover_tasks_today()

        self.assertFalse(response['success'])
        self.assertIn("Error de base de datos", response['response'])

    def test_event_register_task_user_success(self):
        """Prueba el registro exitoso de una tarea"""
        self.mock_data_format.convertir_data_to_date.return_value = date(2025, 7, 1)
        mock_task_instance = MagicMock()
        mock_task_instance.register_task.return_value = (True, "Tarea registrada")
        self.mock_register_task.return_value = mock_task_instance

        result, message = TaskController.event_register_task_user(
            "Comprar pan", "2025-07-01", 3, "Ir a la panadería"
        )

        self.assertTrue(result)
        self.assertEqual(message, "Tarea registrada")
        self.mock_register_task.assert_called_once()
        mock_task_instance.register_task.assert_called_once()

    def test_event_register_task_user_invalid_date(self):
        """Prueba con fecha inválida"""
        self.mock_data_format.convertir_data_to_date.side_effect = ValueError("Formato de fecha inválido")

        result, message = TaskController.event_register_task_user(
            "Tarea", "fecha-invalida", 2, "Detalle"
        )

        self.assertFalse(result)
        self.assertIn("Formato de fecha inválido", message)

    def test_event_register_task_user_priority_out_of_range(self):
        """Prueba con prioridad fuera de rango"""
        self.mock_data_format.convertir_data_to_date.return_value = date.today()

        result, message = TaskController.event_register_task_user(
            "Tarea", "2025-07-01", 6, "Detalle"
        )

        self.assertFalse(result)
        self.assertIn("Prioridad no válida", message)

    def test_get_tasks_of_group_date_success(self):
        """Prueba la obtención exitosa de tareas de grupo por fecha"""
        self.mock_task_service.get_tasks_of_group_date.return_value = ['Tarea G1', 'Tarea G2']
        self.mock_data_format.convert_to_dict_task_data.return_value = {'tarea1': 'data1', 'tarea2': 'data2'}

        response = TaskController.get_tasks_of_group_date(date(2025, 7, 1), 1)

        self.assertTrue(response['success'])
        self.assertEqual(response['data']['tareas'], {'tarea1': 'data1', 'tarea2': 'data2'})

    def test_get_tasks_of_group_date_empty(self):
        """Prueba cuando no hay tareas para la fecha y grupo"""
        self.mock_task_service.get_tasks_of_group_date.return_value = []

        response = TaskController.get_tasks_of_group_date(date(2025, 7, 1), 1)

        self.assertTrue(response['success'])
        self.assertEqual(response['data']['tareas'], [])

    def test_update_state_task_success(self):
        """Prueba la actualización exitosa del estado de una tarea"""
        self.mock_task_service.update_state_task.return_value = True

        result = TaskController.update_state_task(1, True)

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Se actualizó el estado de la tarea.")
        self.mock_task_service.update_state_task.assert_called_once_with(1, True)

    def test_update_state_task_failure(self):
        """Prueba el fallo al actualizar el estado de una tarea"""
        self.mock_task_service.update_state_task.return_value = False

        result = TaskController.update_state_task(1, True)

        self.assertFalse(result['success'])
        self.assertEqual(result['response'], "No se pudo actualizar el estado de la tarea.")

    def test_delete_task_success(self):
        """Prueba la eliminación exitosa de una tarea"""
        self.mock_task_service.delete_task.return_value = True

        result = TaskController.delete_task(1)

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Se eliminó la tarea correctamente.")

    def test_delete_task_failure(self):
        """Prueba el fallo al eliminar una tarea"""
        self.mock_task_service.delete_task.return_value = False

        result = TaskController.delete_task(1)

        self.assertFalse(result['success'])
        self.assertEqual(result['response'], "No se pudo eliminar la tarea.")

    def test_validar_datos_correctos(self):
        """Prueba la validación de datos correctos"""
        self.mock_data_format.convertir_data_to_date.return_value = date(2025, 7, 1)

        result, msg = TaskController.validar_datos("2025-07-01", 3)

        self.assertTrue(result)
        self.assertEqual(msg, "Datos validos")

    def test_validar_datos_fecha_invalida(self):
        """Prueba con fecha inválida"""
        self.mock_data_format.convertir_data_to_date.side_effect = ValueError("Fecha inválida")

        result, msg = TaskController.validar_datos("fecha-invalida", 3)

        self.assertFalse(result)
        self.assertIn("Fecha inválida", str(msg))

    def test_validar_datos_prioridad_invalida(self):
        """Prueba con prioridad inválida"""
        result, msg = TaskController.validar_datos("2025-07-01", "no-numero")

        self.assertFalse(result)
        self.assertIn("invalid literal", str(msg))


if __name__ == '__main__':
    unittest.main()