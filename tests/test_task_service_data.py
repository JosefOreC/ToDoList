import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.modelo.entities.modelo import Tarea, UsuarioTarea
from src.modelo.service.task_service.task_service_data import TaskServiceData
from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.entities.rol import Rol

class TestTaskServiceData(unittest.TestCase):

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_insert_task_user(self, mock_session):
        mock_tarea = Tarea(IDTarea=1)
        relaciones = [UsuarioTarea(IDUsuario=1), UsuarioTarea(IDUsuario=2)]

        TaskServiceData.insert_task_user(mock_tarea, relaciones)

        mock_session.add_all.assert_any_call([mock_tarea])
        for relacion in relaciones:
            self.assertEqual(relacion.IDTarea, mock_tarea.IDTarea)
        mock_session.add_all.assert_called_with(relaciones)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.group_service.group_service_data.GroupServiceData.get_rol_in_group")
    @patch("src.modelo.service.group_service.group_service_data.GroupServiceData.is_user_in_group")
    @patch("src.modelo.service.task_service.task_service_data.SessionManager.get_instance")
    @patch("src.modelo.service.task_service.task_service_data.UpdateTask")
    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_update_task_user(self, mock_session, mock_update_task, mock_session_manager, mock_is_user, mock_get_rol):
        # Simular que el usuario actual es master (permiso para editar)
        # y que el usuario editado no es master (para evitar excepción)
        mock_get_rol.side_effect = [Rol.master, Rol.miembro]

        mock_is_user.return_value = True

        updater = MagicMock()
        mock_update_task.return_value = updater

        mock_user = MagicMock()
        mock_user.IDUsuario = 1
        mock_session_manager.return_value.usuario = mock_user

        TaskServiceData.update_task_user(1, 1, nombre="Test", realizado=True)

        updater.update_name.assert_called_with("Test")
        updater.update_realizado.assert_called_with(True)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_delete_relation_task(self, mock_session):
        mock_instance = MagicMock()
        mock_session.query().filter_by().first.return_value = mock_instance

        TaskServiceData.delete_relation_task(1, 1)

        mock_session.delete.assert_called_with(mock_instance)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_tasks_user_list_date_invalid_range(self, mock_session, mock_convert):
        mock_convert.side_effect = lambda x: date(2024, 1, 2) if x == "2024-01-02" else date(2024, 1, 1)
        with self.assertRaises(Exception):
            TaskServiceData.get_tasks_user_list_date(1, "2024-01-02", "2024-01-01")

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_task(self, mock_session):
        TaskServiceData.get_task(1)
        mock_session.query().filter_by.assert_called_with(IDTarea=1)

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_relations_of_task(self, mock_session):
        TaskServiceData.get_relations_of_task(1)
        mock_session.query().filter_by.assert_called_with(IDTarea=1)

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_id_group_of_task(self, mock_session):
        mock_session.query().filter_by().first.return_value = [5]
        grupo_id = TaskServiceData.get_id_group_of_task(1)
        self.assertEqual(grupo_id, 5)

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_is_editable_task_for_user(self, mock_session):
        mock_session.query().filter_by().first.return_value = [True]
        result = TaskServiceData.is_editable_task_for_user(1, 1)
        self.assertTrue(result)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_add_members_in_group_success(self, mock_session):
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        GroupServiceData.add_members_in_group(1, (2, 3))
        self.assertTrue(mock_session.add_all.called)
        self.assertTrue(mock_session.commit.called)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_change_rol_of_member_success(self, mock_session):
        mock_query = MagicMock()
        mock_user_group = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_user_group
        mock_session.query.return_value = mock_query

        GroupServiceData.change_rol_of_member(1, 2, "editor")
        self.assertEqual(mock_user_group.rol, "editor")
        self.assertTrue(mock_session.commit.called)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_update_group_name_and_description(self, mock_session):
        grupo_mock = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = grupo_mock
        mock_session.commit.return_value = None

        GroupServiceData.update_group(1, nombre="Nuevo Grupo", descripcion="Descripción actualizada")
        self.assertEqual(grupo_mock.Nombre, "Nuevo Grupo")
        self.assertEqual(grupo_mock.Descripcion, "Descripción actualizada")
        self.assertTrue(mock_session.commit.called)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_delete_group_in_all_task_with_id_group(self, mock_session):
        tarea1 = MagicMock()
        tarea2 = MagicMock()
        mock_session.query.return_value.filter_by.return_value.all.return_value = [tarea1, tarea2]

        GroupServiceData.delete_group_in_all_task_with_id_group(1)
        self.assertIsNone(tarea1.IDGrupo)
        self.assertIsNone(tarea2.IDGrupo)
        self.assertTrue(mock_session.commit.called)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_cant_members_group(self, mock_session):
        mock_session.query.return_value.filter.return_value.all.return_value = [1, 2, 3]
        count = GroupServiceData.get_cant_members_group(1)
        self.assertEqual(count, 3)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_delete_member_group_deletes_relation(self, mock_session):
        relacion_mock = MagicMock()
        tarea_pasada = MagicMock()
        tarea_futura = MagicMock()
        session_query = mock_session.query.return_value

        session_query.filter_by.return_value.first.return_value = relacion_mock
        session_query.join.return_value.filter.return_value.all.side_effect = [[tarea_pasada], [tarea_futura]]

        with patch.object(GroupServiceData, '_GroupServiceData__delete_tareas_relacion') as mock_delete:
            with patch.object(GroupServiceData, '_GroupServiceData__conserver_task') as mock_conserve:
                GroupServiceData._GroupServiceData__delete_member_group(1, 1, False)
                mock_delete.assert_called_once_with([tarea_futura])
                mock_conserve.assert_called_once_with([tarea_pasada])
                mock_session.delete.assert_called_once_with(relacion_mock)
                self.assertTrue(mock_session.commit.called)

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_delete_group_success(self, mock_session):
        relacion = MagicMock()
        grupo = MagicMock()
        mock_session.query.return_value.filter_by.return_value.all.return_value = [relacion]
        mock_session.query.return_value.filter_by.return_value.first.return_value = grupo

        with patch.object(GroupServiceData, 'delete_group_in_all_task_with_id_group') as mock_delete_task:
            GroupServiceData._GroupServiceData__delete_group(1)
            mock_session.delete.assert_any_call(relacion)
            mock_delete_task.assert_called_once_with(1)
            mock_session.delete.assert_called_with(grupo)
            self.assertTrue(mock_session.commit.called)

    @patch('src.modelo.service.task_service.task_service_data.UpdateTask')
    @patch('src.modelo.service.task_service.task_service_data.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.task_service.task_service_data.TaskServiceData.get_id_group_of_task')
    @patch('src.modelo.service.task_service.task_service_data.session.query')
    @patch('src.modelo.service.task_service.task_service_data.session.commit')
    @patch('src.modelo.service.task_service.task_service_data.SessionManager.get_instance')  # ✅ NUEVO patch
    def test_update_task_user_success(self, mock_get_instance, mock_commit, mock_query, mock_get_group, mock_get_rol,
                                      mock_update_task):
        # Mock usuario logueado
        mock_usuario = MagicMock()
        mock_usuario.IDUsuario = 1
        mock_get_instance.return_value.usuario = mock_usuario

        mock_get_group.return_value = 10
        mock_get_rol.side_effect = [Rol.editor, Rol.miembro]
        mock_query.return_value.filter.return_value.first.return_value = [True]
        mock_update_task_instance = MagicMock()
        mock_update_task.return_value = mock_update_task_instance

        TaskServiceData.update_task_user(
            id_usuario=1,
            id_tarea=1,
            nombre="Test",
            realizado=True
        )

        mock_update_task_instance.update_name.assert_called_once_with("Test")
        mock_update_task_instance.update_realizado.assert_called_once_with(True)
        mock_commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
