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

    @patch('src.controlador.task_controller.TaskServiceData.edit_disponible_from_user')
    @patch('src.controlador.task_controller.UserServiceData.recover_id_user_for_alias')
    def test_edit_disponible_success(self, mock_recover_id, mock_edit_disponible):
        mock_recover_id.return_value = 10

        result = TaskController.edit_disponible_to_task_in_group(5, "usuario1", True)

        self.assertTrue(result['success'])
        self.assertIn("Se editó el apartado disponible", result['response'])
        mock_recover_id.assert_called_once_with("usuario1")
        mock_edit_disponible.assert_called_once_with(id_usuario=10, id_tarea=5, disponible=True)

    @patch('src.controlador.task_controller.TaskServiceData.edit_disponible_from_user', side_effect=Exception("Error"))
    @patch('src.controlador.task_controller.UserServiceData.recover_id_user_for_alias')
    def test_edit_disponible_error(self, mock_recover_id, mock_edit_disponible):
        mock_recover_id.return_value = 10

        result = TaskController.edit_disponible_to_task_in_group(5, "usuario1", False)

        self.assertFalse(result['success'])
        self.assertIn("No se puedo editar el apartado disponible de un usuario. \nError", result['response'])

    @patch('src.controlador.task_controller.TaskServiceData.edit_type_check_from_group')
    @patch('src.controlador.task_controller.UserServiceData.recover_id_user_for_alias')
    def test_edit_type_check_success(self, mock_recover_id, mock_edit_type_check):
        mock_recover_id.return_value = 7

        result = TaskController.edit_type_check_to_task(15, "usuario2", "auto")

        self.assertTrue(result['success'])
        self.assertIn("Se actualizó el tipo de check", result['response'])
        mock_edit_type_check.assert_called_once_with(7, 15, "auto")

    @patch('src.controlador.task_controller.TaskServiceData.edit_type_check_from_group',
           side_effect=Exception("Error tipo check"))
    @patch('src.controlador.task_controller.UserServiceData.recover_id_user_for_alias')
    def test_edit_type_check_error(self, mock_recover_id, mock_edit_type_check):
        mock_recover_id.return_value = 8

        result = TaskController.edit_type_check_to_task(20, "usuario3", "manual")

        self.assertFalse(result['success'])
        self.assertIn("No se puedo actualizar el tipo de check", result['response'])

    @patch('src.controlador.task_controller.TaskServiceData.delete_relation_task_member_group')
    @patch('src.controlador.task_controller.UserServiceData.recover_id_user_for_alias')
    def test_delete_user_of_task_success(self, mock_recover_id, mock_delete):
        mock_recover_id.return_value = 11

        result = TaskController.delete_user_of_task_group("usuarioX", 30)

        self.assertTrue(result['success'])
        self.assertIn("Se quitó al usuario usuarioX", result['response'])
        mock_delete.assert_called_once_with(11, 30)

    @patch('src.controlador.task_controller.TaskServiceData.delete_relation_task_member_group',
           side_effect=Exception("Error eliminación"))
    @patch('src.controlador.task_controller.UserServiceData.recover_id_user_for_alias')
    def test_delete_user_of_task_error(self, mock_recover_id, mock_delete):
        mock_recover_id.return_value = 12

        result = TaskController.delete_user_of_task_group("usuarioY", 31)

        self.assertFalse(result['success'])
        self.assertIn("No se pudo quitar al usuario usuarioY", result['response'])

    @patch('src.controlador.task_controller.SessionManager.get_id_user', return_value=50)
    @patch('src.controlador.task_controller.GroupServiceData.get_rol_in_group', return_value=Rol.miembro)
    @patch('src.controlador.task_controller.TaskServiceData.get_id_group_of_task', return_value=99)
    def test_tarea_con_grupo_sin_permisos(self, mock_get_group, mock_get_rol, mock_get_user):
        result = TaskController.event_delete_task(1)
        self.assertFalse(result[0])
        self.assertIn("No se tienen los permisos", result[1])
        mock_get_rol.assert_called_once()

    @patch('src.controlador.task_controller.TaskServiceData.delete_relation_task')
    @patch('src.controlador.task_controller.SessionManager.get_id_user', return_value=10)
    @patch('src.controlador.task_controller.GroupServiceData.get_rol_in_group', side_effect=Exception("No tiene rol"))
    @patch('src.controlador.task_controller.TaskServiceData.get_id_group_of_task', return_value=88)
    def test_tarea_con_grupo_sin_rol_borra_relacion(self, mock_get_group, mock_get_rol, mock_get_user,
                                                    mock_delete_relation):
        result = TaskController.event_delete_task(3)
        self.assertTrue(result[0])
        self.assertEqual(result[1], "Tarea Eliminada")
        mock_delete_relation.assert_called_once_with(id_usuario=10, id_tarea=3)

    @patch('src.controlador.task_controller.TaskServiceData.delete_relation_task', side_effect=Exception("Fallo grave"))
    @patch('src.controlador.task_controller.SessionManager.get_id_user', return_value=20)
    @patch('src.controlador.task_controller.GroupServiceData.get_rol_in_group', side_effect=Exception("Error rol"))
    @patch('src.controlador.task_controller.TaskServiceData.get_id_group_of_task', return_value=99)
    def test_error_eliminar_relacion(self, *_):
        result = TaskController.event_delete_task(99)
        self.assertFalse(result[0])
        self.assertIn("No se pudo eliminar la tarea", result[1])

    @patch('src.controlador.task_controller.TaskServiceData.soft_delete_task')
    @patch('src.controlador.task_controller.TaskServiceData.get_id_group_of_task', return_value=None)
    def test_soft_delete_exitoso(self, mock_get_group, mock_soft_delete):
        result = TaskController.event_delete_task(55)
        self.assertTrue(result[0])
        self.assertEqual(result[1], "Tarea eliminada")
        mock_soft_delete.assert_called_once_with(id_tarea=55)

    @patch('src.controlador.task_controller.TaskServiceData.soft_delete_task', side_effect=Exception("Error DB"))
    @patch('src.controlador.task_controller.TaskServiceData.get_id_group_of_task', return_value=None)
    def test_soft_delete_falla(self, mock_get_group, mock_soft_delete):
        result = TaskController.event_delete_task(66)
        self.assertFalse(result[0])
        self.assertIn("No se pudo eliminar la tarea", result[1])

    @patch('src.controlador.task_controller.TaskServiceData.add_members_to_task_group')
    def test_add_all_valid_members(self, mock_add_members):
        mock_add_members.return_value = (["user1", "user2"], [])

        alias_users = [["user1", True], ["user2", True]]
        result = TaskController.add_member_group_to_task(alias_users, id_tarea=10)

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['usuarios_agregados'], "all")
        self.assertIsNone(result['data']['usuarios_invalidos'])
        self.assertIn("Se agregaron", result['response'])

        mock_add_members.assert_called_once_with(id_tarea=10, alias_users_permitions=alias_users)

    @patch('src.controlador.task_controller.TaskServiceData.add_members_to_task_group')
    def test_add_some_valid_some_invalid(self, mock_add_members):
        mock_add_members.return_value = (["user1"], [("user2", "ya existe")])

        alias_users = [["user1", True], ["user2", True]]
        result = TaskController.add_member_group_to_task(alias_users, id_tarea=15)

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['usuarios_agregados'], [{'alias': 'user1'}])
        self.assertEqual(result['data']['usuarios_invalidos'], [{'alias': 'user2', 'fail': 'ya existe'}])

    @patch('src.controlador.task_controller.TaskServiceData.add_members_to_task_group',
           side_effect=Exception("Error general"))
    def test_add_members_exception(self, mock_add_members):
        alias_users = [["user1", True], ["user2", False]]
        result = TaskController.add_member_group_to_task(alias_users, id_tarea=99)

        self.assertFalse(result['success'])
        self.assertIsNone(result['data']['usuarios_agregados'])
        self.assertIsNone(result['data']['usuarios_invalidos'])
        self.assertIn("No se agregaron", result['response'])

    @patch('src.controlador.task_controller.TaskController.event_update_task_session_manager')
    @patch('src.controlador.task_controller.GroupServiceData.get_rol_in_group')
    @patch('src.controlador.task_controller.TaskServiceData.get_id_group_of_task')
    @patch('src.controlador.task_controller.SessionManager.get_id_user')
    def test_event_edit_task_session_manager_success(self, mock_user, mock_group, mock_rol, mock_update):
        mock_user.return_value = 1
        mock_group.return_value = 5
        mock_rol.return_value = 'editor'
        mock_update.return_value = (True, "Actualizado")

        result = TaskController.event_edit_task_session_manager(1, "Tarea", "2025-07-03", 3, "Detalles")
        self.assertEqual(result, (True, "Actualizado"))

    def test_event_edit_task_session_manager_invalid_fields(self):
        result = TaskController.event_edit_task_session_manager(1, "", "", "", "")
        self.assertEqual(result, (False, "No se puede dejar vació ningún campo."))

    @patch('src.controlador.task_controller.GroupServiceData.get_rol_in_group')
    @patch('src.controlador.task_controller.SessionManager.get_id_user')
    @patch('src.controlador.task_controller.TaskServiceData.get_id_group_of_task')
    def test_event_edit_task_session_manager_no_permission(self, mock_group, mock_user, mock_rol):
        mock_user.return_value = 1
        mock_group.return_value = 10
        mock_rol.return_value = Rol.miembro

        result = TaskController.event_edit_task_session_manager(1, "Tarea", "2025-07-03", 3, "Detalles")
        self.assertEqual(result, (False, "No se tienen los permisos para editar la tarea"))

    @patch('src.controlador.task_controller.RegisterTask')
    @patch('src.controlador.task_controller.UserServiceData.recover_id_user_for_alias')
    @patch('src.controlador.task_controller.TaskController._TaskController__create_tarea')
    @patch('src.controlador.task_controller.GroupServiceData.get_rol_in_group')
    @patch('src.controlador.task_controller.SessionManager.get_id_user')
    def test_event_register_task_group_success(self, mock_user, mock_rol, mock_create, mock_recover_id, mock_register):
        mock_user.return_value = 1
        mock_rol.return_value.name = "master"
        mock_create.return_value = (True, "tarea_obj")
        mock_recover_id.return_value = 11
        mock_register.return_value.register_task.return_value = (True, "Registrado")

        result = TaskController.event_register_task_group(1, "Tarea", "2025-07-03", 2, "Detalles", False,
                                                          [["user1", True]])
        self.assertEqual(result, (True, "Registrado"))

    @patch('src.controlador.task_controller.GroupServiceData.get_rol_in_group')
    @patch('src.controlador.task_controller.SessionManager.get_id_user')
    def test_event_register_task_group_no_permission(self, mock_user, mock_rol):
        mock_user.return_value = 1
        mock_rol.return_value.name = "miembro"
        result = TaskController.event_register_task_group(1, "Tarea", "2025-07-03", 2, "Detalles")
        self.assertEqual(result, (False, "No se tienen los permisos para realizar estos cambios."))

    @patch('src.controlador.task_controller.TaskServiceData.add_group_to_task_exits')
    def test_event_add_group_task_exits_success(self, mock_add_group):
        mock_add_group.return_value = None
        result = TaskController.event_add_group_task_exits(1, 2, [['user1', True]])
        self.assertEqual(result, (True, "Se agregó el grupo a la tarea."))

    @patch('src.controlador.task_controller.TaskServiceData.add_group_to_task_exits', side_effect=Exception("Falló"))
    def test_event_add_group_task_exits_fail(self, mock_add_group):
        result = TaskController.event_add_group_task_exits(1, 2, [['user1', True]])
        self.assertFalse(result[0])
        self.assertIn("No se pudo agregar el grupo a la tarea", result[1])

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_create_tarea_fecha_exception(self, mock_convert_date):
        mock_convert_date.side_effect = Exception("fecha inválida")
        success, msg = TaskController._TaskController__create_tarea("Mi tarea", "fecha-mal", 3, "detalle")
        self.assertFalse(success)
        self.assertIn("Fecha no valida", msg)

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_create_tarea_prioridad_fuera_de_rango(self, mock_convert_date):
        mock_convert_date.return_value = datetime(2025, 7, 1)
        success, msg = TaskController._TaskController__create_tarea("Mi tarea", "2025-07-01", 6, "detalle")
        self.assertFalse(success)
        self.assertIn("Prioridad no válida", msg)

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_create_tarea_prioridad_value_error(self, mock_convert_date):
        mock_convert_date.return_value = datetime(2025, 7, 1)
        success, msg = TaskController._TaskController__create_tarea("Mi tarea", "2025-07-01", "abc", "detalle")
        self.assertFalse(success)
        self.assertIsInstance(msg, ValueError)

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_create_tarea_prioridad_type_error(self, mock_convert_date):
        mock_convert_date.return_value = datetime(2025, 7, 1)
        success, msg = TaskController._TaskController__create_tarea("Mi tarea", "2025-07-01", None, "detalle")
        self.assertFalse(success)
        self.assertIsInstance(msg, TypeError)

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_validar_datos_fecha_invalida(self, mock_convert_date):
        mock_convert_date.side_effect = Exception("fecha inválida")
        success, msg = TaskController.validar_datos("fecha-mal", 3)
        self.assertFalse(success)
        self.assertIn("Fecha no valida", msg)

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_validar_datos_prioridad_fuera_de_rango(self, mock_convert_date):
        mock_convert_date.return_value = datetime(2025, 7, 1)
        success, msg = TaskController.validar_datos("2025-07-01", 0)
        self.assertFalse(success)
        self.assertIn("Prioridad no válida", msg)

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_validar_datos_prioridad_value_error(self, mock_convert_date):
        mock_convert_date.return_value = datetime(2025, 7, 1)
        success, msg = TaskController.validar_datos("2025-07-01", "xyz")
        self.assertFalse(success)
        self.assertIsInstance(msg, ValueError)

    @patch("src.controlador.task_controller.DataFormat.convertir_data_to_date")
    def test_validar_datos_prioridad_type_error(self, mock_convert_date):
        mock_convert_date.return_value = datetime(2025, 7, 1)
        success, msg = TaskController.validar_datos("2025-07-01", None)
        self.assertFalse(success)
        self.assertIsInstance(msg, TypeError)

    @patch("src.controlador.task_controller.SessionManager.get_id_user", return_value=1)
    @patch("src.controlador.task_controller.TaskServiceData.get_task_user_archivade")
    def test_recover_task_archivate_success(self, mock_get_tasks, mock_user):
        mock_get_tasks.return_value = ["tarea1", "tarea2"]

        result = TaskController.recover_task_archivate()

        self.assertTrue(result['success'])
        self.assertIn("Se recuperaron los datos", result['response'])
        self.assertEqual(result['data']['tareas'], ["tarea1", "tarea2"])

    @patch("src.controlador.task_controller.SessionManager.get_id_user", return_value=1)
    @patch("src.controlador.task_controller.TaskServiceData.get_task_user_archivade",
           side_effect=Exception("Error de recuperación"))
    def test_recover_task_archivate_error(self, mock_get_tasks, mock_user):
        result = TaskController.recover_task_archivate()

        self.assertFalse(result['success'])
        self.assertIn("No se recuperaron los datos", result['response'])
        self.assertIsNone(result['data']['tareas'])

    @patch("src.controlador.task_controller.DataFormat.convert_to_dict_tarea_to_edit")
    @patch("src.controlador.task_controller.SessionManager.get_id_user", return_value=1)
    @patch("src.controlador.task_controller.TaskServiceData.get_task_data_for_edit")
    def test_recover_all_data_task_to_view_details_success(self, mock_get_data, mock_user, mock_convert):
        mock_get_data.return_value = {"Nombre": "Tarea"}
        mock_convert.return_value = {"Nombre": "Tarea"}

        result = TaskController.recover_all_data_task_to_view_details(5)

        self.assertTrue(result['success'])
        self.assertIn("Se recuperaron los datos de la tarea", result['response'])
        self.assertEqual(result['data']['Nombre'], "Tarea")

    @patch("src.controlador.task_controller.SessionManager.get_id_user", return_value=1)
    @patch("src.controlador.task_controller.TaskServiceData.get_task_data_for_edit", side_effect=Exception("Error"))
    def test_recover_all_data_task_to_view_details_error(self, mock_get_data, mock_user):
        result = TaskController.recover_all_data_task_to_view_details(5)

        self.assertFalse(result['success'])
        self.assertIn("No se pudieron recuperar los datos de la tarea", result['response'])
        self.assertIsNone(result['data'])

    @patch("src.controlador.task_controller.SessionManager.get_id_user", return_value=1)
    @patch("src.controlador.task_controller.TaskServiceData.get_tasks_user_list_date")
    def test_recover_task_date_success(self, mock_get_tasks, mock_user):
        mock_get_tasks.return_value = ["TareaFecha"]
        fecha = datetime(2025, 7, 3)

        result = TaskController.recover_task_date(fecha)

        self.assertTrue(result['success'])
        self.assertIn("Tareas recuperadas", result['response'])
        self.assertEqual(result['data']['tareas'], ["TareaFecha"])

    @patch("src.controlador.task_controller.SessionManager.get_id_user", return_value=1)
    @patch("src.controlador.task_controller.TaskServiceData.get_tasks_user_list_date",
           side_effect=Exception("Error fecha"))
    def test_recover_task_date_error(self, mock_get_tasks, mock_user):
        fecha = datetime(2025, 7, 3)
        result = TaskController.recover_task_date(fecha)

        self.assertFalse(result['success'])
        self.assertIn("No se pudo recuperar las tareas", result['response'])
        self.assertIsNone(result['data']['tareas'])


if __name__ == '__main__':
    unittest.main()