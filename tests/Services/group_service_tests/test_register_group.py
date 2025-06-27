import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.modelo.service.group_service.register_group import RegisterGroup
from src.modelo.entities.modelo import Grupo, UsuarioGrupo, Rol


class TestRegisterGroup(unittest.TestCase):

    def setUp(self):
        self.fake_grupo = Grupo(Nombre="TestGroup", IDMaster=1, Descripcion="Grupo de prueba", Fecha_creacion=datetime.today())

    def test_create_primitive_group(self):
        grupo = RegisterGroup.create_primitive_group("GrupoX", 10, "desc")
        self.assertEqual(grupo.Nombre, "GrupoX")
        self.assertEqual(grupo.IDMaster, 10)
        self.assertEqual(grupo.Descripcion, "desc")
        self.assertIsInstance(grupo.Fecha_creacion, datetime)

    @patch('src.modelo.service.group_service.register_group.GroupServiceData.insert_group')
    def test_register_group_only_master(self, mock_insert_group):
        rg = RegisterGroup(self.fake_grupo)
        rg.register_group()

        # Validamos que solo se haya agregado 1 relación (el master)
        args, kwargs = mock_insert_group.call_args
        grupo_passed, relations_passed = args

        self.assertEqual(grupo_passed, self.fake_grupo)
        self.assertEqual(len(relations_passed), 1)
        self.assertEqual(relations_passed[0].IDUsuario, self.fake_grupo.IDMaster)
        self.assertEqual(relations_passed[0].rol, Rol.master)

    @patch('src.modelo.service.group_service.register_group.GroupServiceData.insert_group')
    def test_register_group_with_members(self, mock_insert_group):
        miembros = [2, 3]
        rg = RegisterGroup(self.fake_grupo, miembros_id=miembros)
        rg.register_group()

        args, kwargs = mock_insert_group.call_args
        grupo_passed, relations_passed = args

        self.assertEqual(grupo_passed, self.fake_grupo)
        self.assertEqual(len(relations_passed), 1 + len(miembros))

        # Validamos al menos un miembro
        roles = [rel.rol for rel in relations_passed]
        self.assertIn(Rol.miembro, roles)
        self.assertIn(Rol.master, roles)


if __name__ == "__main__":
    unittest.main()
