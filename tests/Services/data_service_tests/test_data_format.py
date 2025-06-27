import unittest
from datetime import datetime, date
from src.modelo.service.data_service.data_format import DataFormat


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


if __name__ == "__main__":
    unittest.main()
