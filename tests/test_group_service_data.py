import unittest
from unittest.mock import patch, MagicMock
from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.service.task_service.task_service_data import TaskServiceData
from src.modelo.entities.modelo import Rol
from src.modelo.entities.grupo import Grupo
from src.modelo.entities.usuario_grupo import UsuarioGrupo
from sqlalchemy.exc import IntegrityError

class TestGroupServiceData(unittest.TestCase):

    @patch("src.modelo.service.group_service.group_service_data.session")
    def test_get_group_for_id(self, mock_session):
        fake_group = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = fake_group

        result = GroupServiceData.get_group_for_id(1)

        self.assertEqual(result, fake_group)
        mock_session.query.assert_called_once()

    @patch("src.modelo.service.group_service.group_service_data.session")
    def test_get_data_task_group_name_exists(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = ("Grupo 1",)

        result = GroupServiceData.get_data_task_group_name(1)

        self.assertEqual(result, "Grupo 1")

    def test_get_data_task_group_name_none(self):
        result = GroupServiceData.get_data_task_group_name(None)
        self.assertIsNone(result)

    @patch("src.modelo.service.group_service.group_service_data.session")
    def test_get_all_members(self, mock_session):
        mock_session.query.return_value.filter.return_value.all.return_value = [(1,), (2,), (3,)]

        result = GroupServiceData.get_all_members(5)

        self.assertEqual(result, [1, 2, 3])

    @patch("src.modelo.service.group_service.group_service_data.session")
    def test_is_user_in_group_true(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = (1,)

        result = GroupServiceData.is_user_in_group(10, 100)
        self.assertTrue(result)

    @patch("src.modelo.service.group_service.group_service_data.session")
    def test_is_user_in_group_false(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = GroupServiceData.is_user_in_group(10, 100)
        self.assertFalse(result)

    @patch("src.modelo.service.group_service.group_service_data.session")
    def test_get_all_members_with_rol(self, mock_session):
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [
            ("ana", Rol.editor), ("bob", Rol.master)
        ]

        result = GroupServiceData.get_all_members_with_rol(5)

        expected = [["ana", Rol.editor], ["bob", Rol.master]]
        self.assertEqual(result, expected)

    @patch("src.modelo.service.group_service.group_service_data.session")
    def test_get_cant_members_group(self, mock_session):
        mock_session.query.return_value.filter.return_value.all.return_value = [1, 2, 3]

        result = GroupServiceData.get_cant_members_group(99)
        self.assertEqual(result, 3)
        self.assertEqual(result, 3)

    @patch('src.modelo.service.task_service.task_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.task_service.task_service_data.SessionManager.get_id_user')
    @patch(
        'src.modelo.service.task_service.task_service_data.TaskServiceData._TaskServiceData__add_member_to_task_group')
    @patch('src.modelo.service.task_service.task_service_data.TaskServiceData.get_id_group_of_task')
    @patch('src.modelo.service.task_service.task_service_data.UserServiceData.recover_id_user_for_alias')
    @patch('src.modelo.service.task_service.task_service_data.GroupServiceData.is_user_in_group')
    def test_add_all_valid_members(self, mock_is_user_in_group, mock_recover_id, mock_get_group,
                                   mock_add_member, mock_get_id_user, mock_get_rol):
        mock_get_id_user.return_value = 1
        mock_get_group.return_value = 10
        mock_get_rol.return_value = Rol.master
        mock_recover_id.side_effect = lambda alias: {'user1': 11, 'user2': 12}[alias]
        mock_is_user_in_group.return_value = True

        alias_users = [['user1', True], ['user2', True]]

        result = TaskServiceData.add_members_to_task_group(5, alias_users)

        self.assertEqual(result[0], ['user1', 'user2'])
        self.assertEqual(result[1], [])

    @patch('src.modelo.service.task_service.task_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.task_service.task_service_data.SessionManager.get_id_user')
    @patch(
        'src.modelo.service.task_service.task_service_data.TaskServiceData._TaskServiceData__add_member_to_task_group')
    @patch('src.modelo.service.task_service.task_service_data.TaskServiceData.get_id_group_of_task')
    @patch('src.modelo.service.task_service.task_service_data.UserServiceData.recover_id_user_for_alias')
    @patch('src.modelo.service.task_service.task_service_data.GroupServiceData.is_user_in_group')
    def test_add_some_invalid_members(self, mock_is_user_in_group, mock_recover_id, mock_get_group,
                                      mock_add_member, mock_get_id_user, mock_get_rol):
        mock_get_id_user.return_value = 1
        mock_get_group.return_value = 10
        mock_get_rol.return_value = Rol.editor
        mock_recover_id.side_effect = lambda alias: {'user1': 11, 'user2': 12}[alias]
        mock_is_user_in_group.side_effect = lambda id_grupo, id_usuario: id_usuario != 12

        alias_users = [['user1', True], ['user2', True]]

        result = TaskServiceData.add_members_to_task_group(5, alias_users)

        self.assertEqual(result[0], ['user1', 'user2'])
        self.assertEqual(result[1], [['user2', 'No pertenece al grupo.']])


    @patch('src.modelo.service.task_service.task_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.task_service.task_service_data.SessionManager.get_id_user')
    @patch('src.modelo.service.task_service.task_service_data.TaskServiceData.get_id_group_of_task')
    def test_user_without_permission(self, mock_get_group, mock_get_id_user, mock_get_rol):
        mock_get_id_user.return_value = 1
        mock_get_group.return_value = 10
        mock_get_rol.return_value = Rol.miembro

        alias_users = [['user1', True]]

        with self.assertRaises(Exception) as context:
            TaskServiceData.add_members_to_task_group(5, alias_users)

        self.assertIn("No se tienen permisos", str(context.exception))

    @patch(
        'src.modelo.service.group_service.group_service_data.GroupServiceData._GroupServiceData__delete_member_group')
    @patch('src.modelo.service.group_service.group_service_data.session')
    @patch('src.modelo.service.group_service.group_service_data.SessionManager.get_id_user')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.get_cant_members_group')
    def test_out_member_group_as_master_without_new_master_raises(self, mock_get_cant, mock_get_rol,
                                                                  mock_get_id_user, mock_session, mock_delete):
        mock_get_id_user.return_value = 1
        mock_get_rol.return_value = Rol.master
        mock_get_cant.return_value = 3  # hay más de un miembro

        with self.assertRaises(Exception) as context:
            GroupServiceData.out_member_group_session_manager(id_grupo=10)

        self.assertIn("no se puede salir del grupo", str(context.exception).lower())

    @patch(
        'src.modelo.service.group_service.group_service_data.GroupServiceData._GroupServiceData__delete_member_group')
    @patch('src.modelo.service.group_service.group_service_data.session')
    @patch('src.modelo.service.group_service.group_service_data.SessionManager.get_id_user')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.get_cant_members_group')
    def test_out_member_group_as_master_with_new_master_success(self, mock_get_cant, mock_get_rol,
                                                                mock_get_id_user, mock_session, mock_delete):
        mock_get_id_user.return_value = 1
        mock_get_rol.return_value = Rol.master
        mock_get_cant.return_value = 3

        new_master_mock = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = new_master_mock

        try:
            GroupServiceData.out_member_group_session_manager(id_grupo=10, new_master=2)
        except Exception:
            self.fail("out_member_group_session_manager() raised Exception unexpectedly!")

        self.assertEqual(new_master_mock.rol, Rol.master)
        mock_session.commit.assert_called_once()
        mock_delete.assert_called_once()

    @patch(
        'src.modelo.service.group_service.group_service_data.GroupServiceData._GroupServiceData__delete_member_group')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.is_user_in_group')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.group_service.group_service_data.SessionManager.get_id_user')
    def test_expel_member_group_success(self, mock_get_id, mock_get_rol, mock_is_in_group, mock_delete):
        mock_get_id.return_value = 1
        mock_get_rol.return_value = Rol.master
        mock_is_in_group.return_value = True

        try:
            GroupServiceData.expel_member_group(id_grupo=5, id_usuario=2)
        except Exception:
            self.fail("expel_member_group() raised Exception unexpectedly!")

        mock_delete.assert_called_once()

    @patch('src.modelo.service.group_service.group_service_data.SessionManager.get_id_user')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.get_rol_in_group')
    def test_expel_member_group_without_permission_raises(self, mock_get_rol, mock_get_id):
        mock_get_id.return_value = 1
        mock_get_rol.return_value = Rol.miembro

        with self.assertRaises(Exception) as context:
            GroupServiceData.expel_member_group(id_grupo=5, id_usuario=2)

        self.assertIn("no se tienen permisos", str(context.exception).lower())

    @patch('src.modelo.service.group_service.group_service_data.SessionManager.get_id_user')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.is_user_in_group')
    def test_expel_member_group_user_not_in_group_raises(self, mock_is_in_group, mock_get_rol, mock_get_id):
        mock_get_id.return_value = 1
        mock_get_rol.return_value = Rol.master
        mock_is_in_group.return_value = False

        with self.assertRaises(Exception) as context:
            GroupServiceData.expel_member_group(id_grupo=5, id_usuario=2)

        self.assertIn("no está en el grupo", str(context.exception).lower())

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_insert_group_success(self, mock_session):
        grupo = Grupo(Nombre="Grupo Test", Descripcion="Descripción")
        rel1 = UsuarioGrupo(IDUsuario=1)
        rel2 = UsuarioGrupo(IDUsuario=2)

        # Simulamos que el IDGrupo se genera automáticamente después de flush
        def flush_side_effect():
            grupo.IDGrupo = 100

        mock_session.flush.side_effect = flush_side_effect

        try:
            GroupServiceData.insert_group(grupo, [rel1, rel2])
        except Exception:
            self.fail("insert_group() raised Exception unexpectedly!")

        # Validamos que se le asignó el ID al grupo en las relaciones
        self.assertEqual(rel1.IDGrupo, 100)
        self.assertEqual(rel2.IDGrupo, 100)

        # Validamos llamadas al session
        mock_session.add_all.assert_any_call([grupo])
        mock_session.add_all.assert_any_call([rel1, rel2])
        mock_session.commit.assert_called_once()

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_insert_group_integrity_error(self, mock_session):
        grupo = Grupo(Nombre="Grupo Duplicado", Descripcion="Otro")
        rels = [UsuarioGrupo(IDUsuario=1)]

        # Simular IntegrityError en flush
        mock_session.flush.side_effect = IntegrityError("Mock", "params", "orig")

        with self.assertRaises(Exception) as context:
            GroupServiceData.insert_group(grupo, rels)

        self.assertIn("Ya existe un grupo con el mismo nombre", str(context.exception))
        mock_session.rollback.assert_called_once()

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_all_members_alias(self, mock_session):
        # Simula el resultado del query: [('user1',), ('user2',)]
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [('user1',),
                                                                                                  ('user2',)]

        result = GroupServiceData.get_all_members_alias(1)
        self.assertEqual(result, ['user1', 'user2'])

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_all_members_without_master(self, mock_session):
        # Simula el resultado del query: [(5,), (6,)]
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [(5,), (6,)]

        result = GroupServiceData.get_all_members_without_master(1)
        self.assertEqual(result, [5, 6])

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_groups_editor_or_master(self, mock_session):
        # Simula el resultado del query: [('Grupo A',), ('Grupo B',)]
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [('Grupo A',),
                                                                                                  ('Grupo B',)]

        result = GroupServiceData.get_groups_editor_or_master(8)
        self.assertEqual(result, ['Grupo A', 'Grupo B'])

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_groups_editor_or_master_with_id(self, mock_session):
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [(1, 'Grupo A'),
                                                                                                  (2, 'Grupo B')]
        result = GroupServiceData.get_groups_editor_or_master_with_id(5)
        self.assertEqual(result, [(1, 'Grupo A'), (2, 'Grupo B')])

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test__get_all_groups(self, mock_session):
        mock_session.query.return_value.all.return_value = [('Grupo A', 'Descripción A', 1),
                                                            ('Grupo B', 'Descripción B', 2)]
        result = GroupServiceData._GroupServiceData__get_all_groups()
        self.assertEqual(result, [('Grupo A', 'Descripción A', 1), ('Grupo B', 'Descripción B', 2)])

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_all_user_groups(self, mock_session):
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [
            (1, 'Grupo A', 'Desc A', Rol.editor),
            (2, 'Grupo B', 'Desc B', Rol.master),
        ]
        result = GroupServiceData.get_all_user_groups(10)
        self.assertEqual(result, [
            (1, 'Grupo A', 'Desc A', Rol.editor),
            (2, 'Grupo B', 'Desc B', Rol.master),
        ])

    @patch('src.modelo.service.group_service.group_service_data.session')
    @patch('src.modelo.service.group_service.group_service_data.GroupServiceData.is_user_in_group')
    def test_get_rol_in_group(self, mock_is_in_group, mock_session):
        mock_is_in_group.return_value = True
        mock_session.query.return_value.filter_by.return_value.first.return_value = (Rol.editor,)
        result = GroupServiceData.get_rol_in_group(id_usuario=7, id_grupo=3)
        self.assertEqual(result, Rol.editor)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_master_alias_of_group(self, mock_session):
        mock_session.query.return_value.join.return_value.filter.return_value.first.return_value = ('admin_alias',)
        result = GroupServiceData.get_master_alias_of_group(2)
        self.assertEqual(result, 'admin_alias')


if __name__ == '__main__':
    unittest.main()
