import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from sqlalchemy.exc import IntegrityError
from src.controlador.group_controller import GroupController
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.entities.rol import Rol
import bcrypt
class FakeUsuario:
    def __init__(self, id_usuario, nombres, apellidos, alias, password_claro):
        self.IDUsuario = id_usuario
        self.Nombres = nombres
        self.Apellidos = apellidos
        self.Alias = alias
        self.Password = bcrypt.hashpw(password_claro.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


class TestGroupController(unittest.TestCase):
    def tearDown(self):
        SessionManager.log_out()

    def setUp(self):
        # Crear usuario falso y asignarlo a la sesión
        self.fake_user = FakeUsuario(
            id_usuario=42,
            nombres="Juan",
            apellidos="Pérez",
            alias="jperez",
            password_claro="secreto123"
        )
        SessionManager.get_instance(self.fake_user)  # Aquí instancias el SessionManager real

        # Parches necesarios para los demás servicios
        self.patcher_register_group = patch('src.controlador.group_controller.RegisterGroup')
        self.patcher_user_service = patch('src.controlador.group_controller.UserServiceData')
        self.patcher_group_service = patch('src.controlador.group_controller.GroupServiceData')
        self.patcher_data_format = patch('src.controlador.group_controller.DataFormat')
        self.patcher_task_controller = patch('src.controlador.group_controller.TaskController')

        self.mock_register_group = self.patcher_register_group.start()
        self.mock_user_service = self.patcher_user_service.start()
        self.mock_group_service = self.patcher_group_service.start()
        self.mock_data_format = self.patcher_data_format.start()
        self.mock_task_controller = self.patcher_task_controller.start()

        # Configurar comportamiento común de los mocks
        self.mock_group_service.get_rol_in_group.return_value = Rol.master
        self.mock_user_service.recover_id_user_for_alias.return_value = 2
        self.mock_user_service.is_user_with_alias_exits.return_value = True
        self.mock_group_service.is_user_in_group.return_value = False

        self.addCleanup(self.patcher_register_group.stop)
        self.addCleanup(self.patcher_user_service.stop)
        self.addCleanup(self.patcher_group_service.stop)
        self.addCleanup(self.patcher_data_format.stop)
        self.addCleanup(self.patcher_task_controller.stop)


    def test_register_group_success(self):
        """Prueba el registro exitoso de un grupo"""
        self.mock_register_group.create_primitive_group.return_value = "group_object"
        mock_instance = MagicMock()
        mock_instance.register_group.return_value = None
        self.mock_register_group.return_value = mock_instance

        success, message = GroupController.register_group("Test Group", "Description", ["member1"])

        self.assertTrue(success)
        self.assertEqual(message, "Se agregó el grupo con éxito")
        self.mock_register_group.create_primitive_group.assert_called_once_with(
            "Test Group", id_master=42, descripcion="Description"
        )
        self.mock_register_group.return_value.register_group.assert_called_once()

    def test_register_group_integrity_error(self):
        """Prueba el manejo de IntegrityError al registrar grupo"""
        self.mock_register_group.create_primitive_group.return_value = "group_object"
        mock_instance = MagicMock()
        mock_instance.register_group.side_effect = IntegrityError("", "", "")
        self.mock_register_group.return_value = mock_instance

        success, message = GroupController.register_group("Test Group", "Description", ["member1"])

        self.assertFalse(success)
        self.assertEqual(message, "No se pudo guardar el grupo. \n Ya existe un grupo con el mismo nombre.")

    def test_is_user_exits_not_self(self):
        """Prueba que no se pueda agregar al usuario actual como miembro"""
        result, message = GroupController.is_user_exits("test_user")

        self.assertTrue(result)
        self.assertIn("Usuario existente.", message)

    def test_is_user_exits_true(self):
        """Prueba la verificación de usuario existente"""
        result, message = GroupController.is_user_exits("other_user")

        self.assertTrue(result)
        self.assertEqual(message, "Usuario existente.")

    def test_add_members_to_group_success(self):
        """Prueba agregar miembros a un grupo exitosamente"""
        success, message = GroupController.add_members_to_group(1, ["new_member"])

        self.assertTrue(success)
        self.assertEqual(message, "Se guardaron los nuevos miembros correctamente.")
        self.mock_group_service.add_members_in_group.assert_called_once()

    def test_add_members_to_group_no_permission(self):
        """Prueba que no se puedan agregar miembros sin permisos"""
        self.mock_group_service.get_rol_in_group.return_value = Rol.editor

        success, message = GroupController.add_members_to_group(1, ["new_member"])

        self.assertFalse(success)
        self.assertEqual(message, "No se tienen los permisos para realizar estos cambios.")

    def test_get_all_groups_of_session_manager_success(self):
        """Prueba la obtención exitosa de todos los grupos del usuario"""
        mock_groups = ["group1", "group2"]
        self.mock_group_service.get_all_user_groups.return_value = mock_groups
        self.mock_data_format.convert_to_dict_groups_data.return_value = {"formatted": "data"}

        result = GroupController.get_all_groups_of_session_manager()

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Se recuperaron los datos.")
        self.assertEqual(result['data']['grupos'], {"formatted": "data"})

    def test_get_data_to_view_success(self):
        """Prueba la obtención exitosa de datos para la vista"""
        self.mock_group_service.get_group_for_id.return_value = "group_data"
        self.mock_data_format.convert_to_dict_group_data.return_value = {"group": "data"}

        self.mock_task_controller.get_tasks_of_group_date.return_value = {
            'success': True,
            'data': {'tareas': ["task1", "task2"]}
        }

        self.mock_group_service.get_all_members_with_rol.return_value = ["member1", "member2"]
        self.mock_data_format.convert_to_dict_member_data_group.return_value = {"members": "data"}

        result = GroupController.get_data_to_view(1)

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Se recuperaron los datos")
        self.assertEqual(result['data']['grupo'], {"group": "data"})
        self.assertEqual(result['data']['tareas'], ["task1", "task2"])
        self.assertEqual(result['data']['miembros'], {"members": "data"})

    def test_set_rol_member_success(self):
        """Prueba el cambio exitoso de rol de un miembro"""
        result = GroupController.set_rol_member("member1", 1, Rol.editor)

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Se guardaron los cambios.")
        self.mock_group_service.change_rol_of_member.assert_called_once_with(1, 2, Rol.editor)

    def test_update_data_group_success(self):
        """Prueba la actualización exitosa de datos del grupo"""
        result = GroupController.update_data_group(1, "New Name", "New Desc")

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Se guardaron los cambios.")
        self.mock_group_service.update_group.assert_called_once_with(id_grupo=1, nombre="New Name",
                                                                     descripcion="New Desc")

    def test_out_of_group_success(self):
        """Prueba salir de un grupo exitosamente"""
        self.mock_group_service.out_member_group_session_manager.return_value = None

        result = GroupController.out_of_group(1, False, "new_master")

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Saliste del grupo correctamente")

    @patch('src.controlador.group_controller.SessionManager.get_instance')
    @patch('src.controlador.group_controller.GroupController.get_rol_in_group')
    def test_no_es_master(self, mock_get_rol, mock_get_session):
        # Simular sesión activa
        mock_session = MagicMock()
        mock_session.usuario.IDUsuario = 1
        mock_get_session.return_value = mock_session

        mock_get_rol.return_value = 'member'
        resultado = GroupController.set_rol_members(1, [['usuario1', 'admin']])
        self.assertEqual(resultado, (False, "No se tienen los permisos para realizar estos cambios."))

    @patch('src.controlador.group_controller.SessionManager.get_instance')
    @patch('src.controlador.group_controller.GroupController.set_rol_member')
    @patch('src.controlador.group_controller.GroupController.get_rol_in_group')
    def test_todos_los_cambios_correctos(self, mock_get_rol, mock_set_rol, mock_get_session):
        mock_get_rol.return_value = 'master'
        mock_set_rol.return_value = {'success': True}

        mock_session = MagicMock()
        mock_session.usuario.IDUsuario = 1
        mock_get_session.return_value = mock_session

        cambios = [['usuario1', 'admin'], ['usuario2', 'viewer']]
        resultado = GroupController.set_rol_members(1, cambios)

        self.assertEqual(resultado, {
            'success': True,
            'response': 'Se guardaron los cambios'
        })

    @patch('src.controlador.group_controller.SessionManager.get_instance')
    @patch('src.controlador.group_controller.GroupController.set_rol_member')
    @patch('src.controlador.group_controller.GroupController.get_rol_in_group')
    def test_algunos_cambios_fallidos(self, mock_get_rol, mock_set_rol, mock_get_session):
        mock_get_rol.return_value = 'master'

        # Simulación: usuario1 falla, usuario2 pasa
        def side_effect(alias_member, id_grupo, rol):
            if alias_member == 'usuario1':
                return {'success': False, 'response': f'Error con {alias_member}'}
            return {'success': True}

        mock_set_rol.side_effect = side_effect

        mock_session = MagicMock()
        mock_session.usuario.IDUsuario = 1
        mock_get_session.return_value = mock_session

        cambios = [['usuario1', 'admin'], ['usuario2', 'viewer']]
        resultado = GroupController.set_rol_members(1, cambios)

        self.assertEqual(resultado, {
            'success': False,
            'response': ['Error con usuario1']
        })

    @patch('src.controlador.group_controller.GroupServiceData.get_all_members')
    def test_get_all_members(self, mock_get_all):
        # Simular datos de retorno
        mock_get_all.return_value = [
            {'id': 1, 'alias': 'usuario1', 'rol': 'admin'},
            {'id': 2, 'alias': 'usuario2', 'rol': 'viewer'},
        ]

        resultado = GroupController.get_all_members(1)

        # Verifica que retorne lo mismo
        self.assertEqual(resultado, [
            {'id': 1, 'alias': 'usuario1', 'rol': 'admin'},
            {'id': 2, 'alias': 'usuario2', 'rol': 'viewer'},
        ])

        # Verifica que se llamó correctamente al metodo del servicio
        mock_get_all.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()