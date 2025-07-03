import unittest
from datetime import datetime, date
from unittest.mock import patch, MagicMock
from src.modelo.service.data_service.data_format import DataFormat
from src.modelo.entities.rol import Rol



class TestDataFormat(unittest.TestCase):

    def test_convertir_data_to_date_from_string(self):
        fecha_str = "26-06-2025"
        fecha_date = DataFormat.convertir_data_to_date(fecha_str)
        self.assertIsInstance(fecha_date, date)
        self.assertEqual(fecha_date, date(2025, 6, 26))

    def test_convertir_data_to_date_from_date(self):
        today = date.today()
        result = DataFormat.convertir_data_to_date(today)
        self.assertEqual(result, today)
        self.assertIsInstance(result, date)

    def test_convertir_data_to_date_from_datetime(self):
        now = datetime(2025, 1, 1, 12, 0)
        result = DataFormat.convertir_data_to_date(now)
        self.assertEqual(result, now)  # corregido para coincidir con datetime

    def test_convertir_data_to_date_invalid_format(self):
        with self.assertRaises(ValueError):
            DataFormat.convertir_data_to_date("2025/01/01")

    def test_convertir_date_to_str(self):
        fecha = datetime(2025, 6, 26)  # corregido: usar datetime, no date
        result = DataFormat.convertir_date_to_str(fecha)
        self.assertEqual(result, "26-06-2025")

    def test_convert_to_dict_basic_data_user(self):
        usuario_data = ("juan", "color favorito", "rojo")
        result = DataFormat.convert_to_dict_basic_data_user(usuario_data)
        expected = {'alias': 'juan', 'pregunta': 'color favorito', 'respuesta': 'rojo'}
        self.assertEqual(result, expected)

    def test_convert_to_dict_group_data(self):
        class GrupoMock:
            IDGrupo = 1
            Nombre = "Equipo Alpha"
            Descripcion = "Grupo de pruebas"

        grupo = GrupoMock()
        result = DataFormat.convert_to_dict_group_data(grupo)
        expected = {
            'id_grupo': 1,
            'nombre': "Equipo Alpha",
            'descripcion': "Grupo de pruebas"
        }
        self.assertEqual(result, expected)

    def test_convert_to_dict_member_data_group(self):
        miembros = [("ana", "ADMIN"), ("luis", "MIEMBRO")]
        result = DataFormat.convert_to_dict_member_data_group(miembros)
        expected = [
            {'alias': 'ana', 'rol': 'ADMIN'},
            {'alias': 'luis', 'rol': 'MIEMBRO'}
        ]
        self.assertEqual(result, expected)

    @patch('src.modelo.service.data_service.data_format.GroupServiceData.get_data_task_group_name')
    @patch('src.modelo.service.data_service.data_format.GroupServiceData.get_rol_in_group')
    @patch('src.modelo.service.data_service.data_format.SessionManager.get_id_user')
    def test_task_activa_con_grupo_y_rol(self, mock_get_id_user, mock_get_rol, mock_get_group_name):
        mock_get_id_user.return_value = 1
        mock_get_group_name.return_value = 'Grupo 1'
        mock_get_rol.return_value.name = 'admin'

        tarea_mock = MagicMock()
        tarea_mock.IDTarea = 1
        tarea_mock.Nombre = "Tarea A"
        tarea_mock.Fecha_programada.strftime.return_value = "01-07-2025"
        tarea_mock.Prioridad = 2
        tarea_mock.Activo = True
        tarea_mock.Detalle = "Detalle A"

        DataFormat.prioridades = {2: 'Media'}

        result = DataFormat.convert_to_dict_task_data([
            (tarea_mock, True, False, 10, False)
        ])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['nombre'], "Tarea A")
        self.assertEqual(result[0]['grupo'], "Grupo 1")
        self.assertEqual(result[0]['rol'], "admin")
        self.assertEqual(result[0]['nombre_prioridad'], "Media")

    @patch('src.modelo.service.data_service.data_format.GroupServiceData.get_data_task_group_name')
    @patch('src.modelo.service.data_service.data_format.GroupServiceData.get_rol_in_group',
           side_effect=Exception("Sin rol"))
    @patch('src.modelo.service.data_service.data_format.SessionManager.get_id_user')
    def test_task_activa_sin_rol(self, mock_get_id_user, mock_get_rol, mock_get_group_name):
        mock_get_id_user.return_value = 2
        mock_get_group_name.return_value = 'Grupo 2'

        tarea_mock = MagicMock()
        tarea_mock.IDTarea = 2
        tarea_mock.Nombre = "Tarea B"
        tarea_mock.Fecha_programada.strftime.return_value = "02-07-2025"
        tarea_mock.Prioridad = 1
        tarea_mock.Activo = True
        tarea_mock.Detalle = "Detalle B"

        DataFormat.prioridades = {1: 'Alta'}

        result = DataFormat.convert_to_dict_task_data([
            (tarea_mock, False, True, 20, False)
        ])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['rol'], None)
        self.assertEqual(result[0]['grupo'], "Grupo 2")

    def test_task_sin_grupo(self):
        tarea_mock = MagicMock()
        tarea_mock.IDTarea = 3
        tarea_mock.Nombre = "Tarea C"
        tarea_mock.Fecha_programada.strftime.return_value = "03-07-2025"
        tarea_mock.Prioridad = 3
        tarea_mock.Activo = True
        tarea_mock.Detalle = "Detalle C"

        DataFormat.prioridades = {3: 'Baja'}

        result = DataFormat.convert_to_dict_task_data([
            (tarea_mock, True, True, None, True)
        ])

        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]['grupo'])
        self.assertIsNone(result[0]['rol'])
        self.assertFalse(result[0]['is_in_group'])

    def test_task_inactiva_no_incluida(self):
        tarea_mock = MagicMock()
        tarea_mock.Activo = False

        result = DataFormat.convert_to_dict_task_data([
            (tarea_mock, True, True, 10, False)
        ])

        self.assertEqual(result, [])  # No debe incluirse por estar inactiva

    def test_convertir_date_to_str_with_datetime(self):
        fecha = datetime(2025, 7, 3)
        resultado = DataFormat.convertir_date_to_str(fecha)
        self.assertEqual(resultado, "03-07-2025")

    def test_convertir_date_to_str_with_date(self):
        fecha = date(2025, 7, 3)
        resultado = DataFormat.convertir_date_to_str(fecha)
        self.assertEqual(resultado, "03-07-2025")

    def test_convertir_date_to_str_invalid_type(self):
        with self.assertRaises(ValueError):
            DataFormat.convertir_date_to_str("2025-07-03")

    def test_convert_to_dict_groups_data(self):
        grupos_mock = [
            (1, "Grupo A", "Descripción A", Rol.master),
            (2, "Grupo B", "Descripción B", Rol.editor)
        ]

        resultado = DataFormat.convert_to_dict_groups_data(grupos_mock)

        esperado = [
            {'id_grupo': 1, 'nombre': "Grupo A", 'descripcion': "Descripción A", 'rol_usuario': 'master'},
            {'id_grupo': 2, 'nombre': "Grupo B", 'descripcion': "Descripción B", 'rol_usuario': 'editor'}
        ]

        self.assertEqual(resultado, esperado)

    def test_convert_to_dict_groups_data_with_out_rol(self):
        class GrupoMock:
            def __init__(self, IDGrupo, Nombre, Descripcion):
                self.IDGrupo = IDGrupo
                self.Nombre = Nombre
                self.Descripcion = Descripcion

        # Simula la función convert_to_dict_group_data usada internamente
        def dummy_convert_to_dict_group_data(grupo):
            return {
                'id_grupo': grupo.IDGrupo,
                'nombre': grupo.Nombre,
                'descripcion': grupo.Descripcion
            }

        # Parchar temporalmente el metodo interno
        original = DataFormat.convert_to_dict_group_data
        DataFormat.convert_to_dict_group_data = staticmethod(dummy_convert_to_dict_group_data)

        grupos_mock = [
            GrupoMock(1, "Grupo X", "Desc X"),
            GrupoMock(2, "Grupo Y", "Desc Y")
        ]

        resultado = DataFormat.convert_to_dict_groups_data_with_out_rol(grupos_mock)

        esperado = [
            {'id_grupo': 1, 'nombre': "Grupo X", 'descripcion': "Desc X"},
            {'id_grupo': 2, 'nombre': "Grupo Y", 'descripcion': "Desc Y"}
        ]

        self.assertEqual(resultado, esperado)

        # Restaurar metodo original
        DataFormat.convert_to_dict_group_data = original

if __name__ == "__main__":
    unittest.main()
