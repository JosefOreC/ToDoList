import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.modelo.entities.modelo import Tarea, UsuarioTarea
from src.modelo.service.task_service import task_service_data
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

    @patch("src.modelo.service.task_service.task_service_data.session")
    @patch("src.modelo.service.task_service.task_service_data.GroupServiceData.get_rol_in_group")
    @patch("src.modelo.service.task_service.task_service_data.SessionManager.get_id_user")
    @patch("src.modelo.service.task_service.task_service_data.TaskServiceData.get_id_group_of_task")
    def test_delete_relation_task_member_group(self, mock_get_id_group, mock_get_id_user, mock_get_rol, mock_session):
        # Preparar mocks
        mock_get_id_group.return_value = 1
        mock_get_id_user.return_value = 99
        mock_get_rol.side_effect = [Rol.editor, Rol.miembro]  # Primero para el SM, luego para el usuario a eliminar

        # Simular que la tarea es editable para el SM (Disponible=True)
        mock_session.query().filter().first.return_value = [True]

        # Simular objeto UsuarioTarea para eliminar
        mock_usuario_tarea = MagicMock()
        mock_session.query().filter_by().first.return_value = mock_usuario_tarea

        # Ejecutar la función
        TaskServiceData.delete_relation_task_member_group(5, 10)

        # Verificar llamadas
        mock_session.delete.assert_called_once_with(mock_usuario_tarea)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.TaskServiceData.add_members_to_task_group")
    @patch("src.modelo.service.task_service.task_service_data.GroupServiceData.get_all_members_alias")
    @patch("src.modelo.service.task_service.task_service_data.GroupServiceData.get_master_alias_of_group")
    @patch("src.modelo.service.task_service.task_service_data.GroupServiceData.get_rol_in_group")
    @patch("src.modelo.service.task_service.task_service_data.SessionManager.get_instance")
    @patch("src.modelo.service.task_service.task_service_data.SessionManager.get_id_user")
    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_add_group_to_task_exits_all(
            self, mock_session, mock_get_id_user, mock_get_instance, mock_get_rol,
            mock_get_master, mock_get_all_alias, mock_add_members
    ):
        # Mock sesión y objeto tarea
        mock_task = MagicMock()
        mock_task.IDGrupo = None
        mock_session.query().filter_by().first.return_value = mock_task

        # Simular usuario logueado
        mock_get_id_user.return_value = 1

        # Simular sesión de usuario
        mock_usuario = MagicMock()
        mock_usuario.Alias = "yo"
        mock_get_instance.return_value.usuario = mock_usuario

        # Simular rol válido
        mock_get_rol.return_value = Rol.editor

        # Simular alias master y alias del grupo
        mock_get_master.return_value = "master"
        mock_get_all_alias.return_value = ["yo", "master", "otro"]

        # Ejecutar función
        TaskServiceData.add_group_to_task_exits(1, 2, "all")

        # Verificar asignación de grupo y commit
        self.assertEqual(mock_task.IDGrupo, 2)
        mock_session.commit.assert_called_once()

        # Verificar miembros agregados (excluyendo "yo")
        expected_members = [["master", True], ["otro", True]]
        mock_add_members.assert_called_once_with(id_tarea=1, alias_users_permitions=expected_members)

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_add_member_to_task_group_success(self, mock_session):
        # No existe la relación
        mock_session.query().filter().first.return_value = None

        TaskServiceData._TaskServiceData__add_member_to_task_group(1, 2, 3, disponible=True)

        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_add_member_to_task_group_already_exists(self, mock_session):
        # Ya existe la relación
        mock_session.query().filter().first.return_value = True

        with self.assertRaises(Exception) as context:
            TaskServiceData._TaskServiceData__add_member_to_task_group(1, 2, 3, disponible=True)

        self.assertIn("Esta relación ya está agregada", str(context.exception))

    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_add_member_to_task_group_commit_error(self, mock_session):
        # No existe la relación
        mock_session.query().filter().first.return_value = None
        # Simular error al hacer commit
        mock_session.commit.side_effect = Exception("Fallo de base de datos")

        with self.assertRaises(Exception) as context:
            TaskServiceData._TaskServiceData__add_member_to_task_group(1, 2, 3, disponible=True)

        self.assertIn("No se pudo agregar la relación", str(context.exception))
        mock_session.rollback.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.DataFormat.convertir_data_to_date")
    @patch("src.modelo.service.task_service.task_service_data.session")
    def test_get_all_task_of_group_date(self, mock_session, mock_convert_date):
        mock_convert_date.return_value = "2025-07-03"

        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_order = MagicMock()
        mock_order.all.return_value = [("tarea1", False, False, True)]

        # Encadenamiento de query
        mock_filter.order_by.return_value = mock_order
        mock_query.join.return_value.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        result = TaskServiceData.get_all_task_of_group_date(
            grupo_id=1,
            usuario_id=10,
            fecha_inicio="2025-07-03",
            activo=True
        )

        mock_convert_date.assert_called_once_with("2025-07-03")
        mock_session.query.assert_called_once()
        self.assertEqual(result, [("tarea1", False, False, True)])

    @patch("src.modelo.service.task_service.task_service_data.session")
    @patch("src.modelo.service.task_service.task_service_data.TaskServiceData.get_task")
    @patch("src.modelo.service.task_service.task_service_data.TaskServiceData.get_relations_of_task")
    def test___delete_task(self, mock_get_relations, mock_get_task, mock_session):
        # Arrange
        relacion1 = MagicMock()
        relacion2 = MagicMock()
        tarea = MagicMock()

        mock_get_relations.return_value = [relacion1, relacion2]
        mock_get_task.return_value = tarea

        # Act
        task_service_data.TaskServiceData._TaskServiceData__delete_task(1)

        # Assert
        mock_session.delete.assert_any_call(relacion1)
        mock_session.delete.assert_any_call(relacion2)
        mock_session.delete.assert_any_call(tarea)
        self.assertEqual(mock_session.delete.call_count, 3)
        mock_session.commit.assert_called_once()

    @patch("src.modelo.service.task_service.task_service_data.TaskServiceData.get_tasks_user_list_all")
    def test_get_task_user_archivade(self, mock_get_all):
        # Preparar valor de retorno simulado
        mock_get_all.return_value = ["tarea1", "tarea2"]

        # Ejecutar método
        result = TaskServiceData.get_task_user_archivade(1)

        # Verificar llamada y retorno
        mock_get_all.assert_called_once_with(1, archivado=True)
        self.assertEqual(result, ["tarea1", "tarea2"])

    @patch("src.modelo.service.task_service.task_service_data.TaskServiceData.get_tasks_user_list_date")
    @patch("src.modelo.service.task_service.task_service_data.SessionManager.get_instance")
    def test_get_tasks_session_user_list_date(self, mock_get_instance, mock_get_date):
        # Simular usuario con ID
        mock_user = MagicMock()
        mock_user.IDUsuario = 99
        mock_get_instance.return_value.usuario = mock_user

        # Valor simulado de retorno
        mock_get_date.return_value = ["tarea_a"]

        # Ejecutar método
        result = TaskServiceData.get_tasks_session_user_list_date("2025-07-03")

        # Verificar
        mock_get_date.assert_called_once_with(99, "2025-07-03")
        self.assertEqual(result, ["tarea_a"])

    @patch("src.modelo.service.task_service.task_service_data.TaskServiceData.get_tasks_session_user_list_date")
    def test_get_tasks_session_user_list_today(self, mock_get_today):
        # Simular retorno
        mock_get_today.return_value = ["tarea_hoy"]

        # Ejecutar función
        result = TaskServiceData.get_tasks_session_user_list_today()

        # Verificar
        mock_get_today.assert_called_once_with(date.today())
        self.assertEqual(result, ["tarea_hoy"])

if __name__ == "__main__":
    unittest.main()
