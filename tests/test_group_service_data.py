import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError

from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.entities.modelo import Grupo, UsuarioGrupo, Rol

class TestGroupServiceData(unittest.TestCase):

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_insert_group_success(self, mock_session):
        mock_session.add_all = MagicMock()
        mock_session.commit = MagicMock()

        grupo = Grupo(Nombre='Grupo de Prueba')
        relation_list = [UsuarioGrupo(IDUsuario=1, IDGrupo=0, rol=Rol.miembro)]

        GroupServiceData.insert_group(grupo, relation_list)

        mock_session.add_all.assert_called()
        mock_session.commit.assert_called()

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_insert_group_integrity_error(self, mock_session):
        # Simulamos el comportamiento del commit para que lance una IntegrityError
        mock_session.add_all = MagicMock()
        mock_session.commit = MagicMock(side_effect=IntegrityError("Ya existe un grupo con el mismo nombre.", 
                                                                   params=None, 
                                                                   orig=None))

        grupo = Grupo(Nombre='Grupo de Prueba')
        relation_list = [UsuarioGrupo(IDUsuario=1, IDGrupo=0, rol=Rol.miembro)]

        with self.assertRaises(Exception) as context:  # Cambiamos a Exception aquí
            GroupServiceData.insert_group(grupo, relation_list)

        # Verifica que el mensaje de la excepción sea el esperado
        self.assertEqual(str(context.exception), 'Ya existe un grupo con el mismo nombre.')

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_data_task_group_name(self, mock_session):
        mock_session.query.return_value.filter.return_value.first.return_value = ('Grupo de Prueba',)

        result = GroupServiceData.get_data_task_group_name(1)
        self.assertEqual(result, 'Grupo de Prueba')

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_all_members(self, mock_session):
        mock_session.query.return_value.filter.return_value.all.return_value = [(1,), (2,)]

        result = GroupServiceData.get_all_members(1)
        self.assertEqual(result, [1, 2])

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_get_all_members_with_rol(self, mock_session):
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [
            ('Usuario1', Rol.miembro.name),
            ('Usuario2', Rol.editor.name)
        ]

        result = GroupServiceData.get_all_members_with_rol(1)
        self.assertEqual(result, [['Usuario1', Rol.miembro.name], ['Usuario2', Rol.editor.name]])

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_change_rol_of_member(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = UsuarioGrupo(IDGrupo=1, IDUsuario=1)
        mock_session.commit = MagicMock()

        GroupServiceData.change_rol_of_member(1, 1, Rol.editor)

        mock_session.commit.assert_called()

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_update_group(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = Grupo(Nombre='Viejo Nombre')
        mock_session.commit = MagicMock()

        GroupServiceData.update_group(1, nombre='Nuevo Nombre')

        mock_session.commit.assert_called()

    @patch('src.modelo.service.group_service.group_service_data.session')
    def test_delete_group_in_all_task_with_id_group(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.all.return_value = [MagicMock(IDGrupo=1)]
        mock_session.commit = MagicMock()

        GroupServiceData.delete_group_in_all_task_with_id_group(1)

        mock_session.commit.assert_called()

if __name__ == '__main__':
    unittest.main()