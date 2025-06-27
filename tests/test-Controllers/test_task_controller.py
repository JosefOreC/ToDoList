import unittest
from unittest.mock import patch, MagicMock
from datetime import date, datetime
from src.controlador.task_controller import TaskController
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.entities.rol import Rol
from src.modelo.entities.tarea import Tarea


class TestTaskController(unittest.TestCase):

    def setUp(self):
        # Configurar mocks para todas las dependencias
        self.mock_session_manager = MagicMock(spec=SessionManager)
        self.mock_session_instance = MagicMock()
        self.mock_user = MagicMock()
        self.mock_user.IDUsuario = 1
        self.mock_user.Alias = "test_user"

        # Configurar SessionManager
        self.mock_session_manager.get_instance.return_value = self.mock_session_instance
        self.mock_session_instance.usuario = self.mock_user
        self.mock_session_manager.get_id_user.return_value = 1

        # Mocks para otros servicios
        self.mock_task_service = MagicMock()
        self.mock_group_service = MagicMock()
        self.mock_user_service = MagicMock()
        self.mock_data_format = MagicMock()
        self.mock_register_task = MagicMock()

        # Aplicar patches
        self.patchers = [
            patch('src.controlador.task_controller.SessionManager', self.mock_session_manager),
            patch('src.controlador.task_controller.TaskServiceData', self.mock_task_service),
            patch('src.controlador.task_controller.GroupServiceData', self.mock_group_service),
            patch('src.controlador.task_controller.UserServiceData', self.mock_user_service),
            patch('src.controlador.task_controller.DataFormat', self.mock_data_format),
            patch('src.controlador.task_controller.RegisterTask', self.mock_register_task)
        ]

        for patcher in self.patchers:
            patcher.start()

        # Configurar comportamientos comunes
        self.mock_data_format.convertir_data_to_date.return_value = date(2025, 1, 1)
        self.mock_data_format.convert_to_dict_task_data_groups.return_value = {'task': 'data'}
        self.mock_group_service.get_rol_in_group.return_value = Rol.editor

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()

    def test_recover_tasks_today_success(self):
        """Prueba recuperación exitosa de tareas para hoy"""
        self.mock_task_service.get_tasks_session_user_list_today.return_value = ['task1', 'task2']

        result = TaskController.recover_tasks_today()

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['tareas'], ['task1', 'task2'])

    def test_recover_tasks_today_empty(self):
        """Prueba cuando no hay tareas para hoy"""
        self.mock_task_service.get_tasks_session_user_list_today.return_value = []

        result = TaskController.recover_tasks_today()

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['tareas'], None)

    def test_recover_tasks_today_error(self):
        """Prueba manejo de errores al recuperar tareas"""
        self.mock_task_service.get_tasks_session_user_list_today.side_effect = Exception("DB Error")

        result = TaskController.recover_tasks_today()

        self.assertFalse(result['success'])
        self.assertIn("DB Error", result['response'])

    def test_recover_task_archivate_success(self):
        """Prueba recuperación de tareas archivadas"""
        self.mock_task_service.get_task_user_archivade.return_value = ['archived1', 'archived2']

        result = TaskController.recover_task_archivate()

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['tareas'], ['archived1', 'archived2'])

    def test_recover_task_date_success(self):
        """Prueba recuperación de tareas por fecha"""
        test_date = datetime(2025, 1, 1)
        self.mock_task_service.get_tasks_user_list_date.return_value = ['task1', 'task2']

        result = TaskController.recover_task_date(test_date)

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['tareas'], ['task1', 'task2'])

    def test_event_register_task_user_success(self):
        """Prueba registro exitoso de tarea de usuario"""
        mock_task = MagicMock(spec=Tarea)
        mock_register = MagicMock()
        mock_register.register_task.return_value = (True, "Success")
        self.mock_register_task.return_value = mock_register

        result, message = TaskController.event_register_task_user(
            "Test", "2025-01-01", 3, "Details"
        )

        self.assertTrue(result)
        self.assertEqual(message, "Success")

    def test_event_register_task_user_invalid_date(self):
        """Prueba con fecha inválida"""
        self.mock_data_format.convertir_data_to_date.side_effect = ValueError("Invalid date")

        result, message = TaskController.event_register_task_user(
            "Test", "invalid", 3, "Details"
        )

        self.assertFalse(result)
        self.assertIn("Invalid date", message)

    def test_event_register_task_user_invalid_priority(self):
        """Prueba con prioridad inválida"""
        result, message = TaskController.event_register_task_user(
            "Test", "2025-01-01", 6, "Details"
        )

        self.assertFalse(result)
        self.assertIn("Prioridad no válida", message)

    def test_validar_datos_valid(self):
        """Prueba validación de datos correctos"""
        result, message = TaskController.validar_datos("2025-01-01", 3)

        self.assertTrue(result)
        self.assertEqual(message, "Datos validos")

    def test_event_update_task_user_success(self):
        """Prueba actualización exitosa de tarea"""
        self.mock_task_service.update_task_user.return_value = None

        result, message = TaskController.event_update_task_user(
            1, 1, "New Name", "2025-01-01", 3, True, True, "Details"
        )

        self.assertTrue(result)
        self.assertEqual(message, "Se guardaron los cambiós con exito")

    def test_event_update_task_session_manager_success(self):
        """Prueba actualización desde sesión"""
        self.mock_task_service.update_task_user.return_value = None

        result, message = TaskController.event_update_task_session_manager(
            1, "New Name", "2025-01-01", 3, True, True, "Details"
        )

        self.assertTrue(result)
        self.assertEqual(message, "Se guardaron los cambiós con exito")

    def test_event_check_in_task_success(self):
        """Prueba check-in de tarea exitoso"""
        self.mock_task_service.is_editable_task_for_user.return_value = True
        self.mock_task_service.update_task_user.return_value = None

        result, message = TaskController.event_check_in_task(1, True)

        self.assertTrue(result)
        self.assertIn("exito", message)

    def test_event_edit_task_session_manager_success(self):
        """Prueba edición de tarea exitosa"""
        self.mock_task_service.get_id_group_of_task.return_value = None
        self.mock_task_service.update_task_user.return_value = None

        result, message = TaskController.event_edit_task_session_manager(
            1, "New", "2025-01-01", 3, "Details"
        )

        self.assertTrue(result)
        self.assertIn("exito", message)

    def test_event_register_task_group_success(self):
        """Prueba registro de tarea grupal exitoso"""
        self.mock_group_service.get_rol_in_group.return_value = Rol.editor
        mock_task = MagicMock(spec=Tarea)
        mock_register = MagicMock()
        mock_register.register_task.return_value = (True, "Success")
        self.mock_register_task.return_value = mock_register

        result, message = TaskController.event_register_task_group(
            1, "Test", "2025-01-01", 3, "Details", False, 'all'
        )

        self.assertTrue(result)
        self.assertEqual(message, "Success")

    def test_event_archive_task_success(self):
        """Prueba archivado exitoso de tarea"""
        self.mock_task_service.update_task_user.return_value = None

        result = TaskController.event_archive_task(1)

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Tarea Archivada")

    def test_event_delete_task_success(self):
        """Prueba eliminación exitosa de tarea"""
        self.mock_task_service.get_id_group_of_task.return_value = None
        self.mock_task_service.soft_delete_task.return_value = None

        result, message = TaskController.event_delete_task(1)

        self.assertTrue(result)
        self.assertEqual(message, "Tarea eliminada")

    def test_get_tasks_of_group_date_success(self):
        """Prueba obtención de tareas grupales por fecha"""
        self.mock_task_service.get_all_task_of_group_date.return_value = ['task1', 'task2']

        result = TaskController.get_tasks_of_group_date(date(2025, 1, 1), 1)

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['tareas'], {'task': 'data'})

    def test_event_unarchive_task_success(self):
        """Prueba desarchivado exitoso de tarea"""
        self.mock_task_service.update_task_user.return_value = None

        result = TaskController.event_unarchive_task(1)

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], 'Se archivó la tarea')


if __name__ == '__main__':
    unittest.main()