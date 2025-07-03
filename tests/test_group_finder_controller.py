import unittest
from unittest.mock import patch, MagicMock
from src.controlador.group_finder_controller import GroupFinderController


class TestGroupFinderController(unittest.TestCase):

    @patch('src.controlador.group_finder_controller.DataFormat.convert_to_dict_groups_data_with_out_rol')
    @patch('src.controlador.group_finder_controller.GroupFinder.search_for_group_by_name')
    @patch('src.controlador.group_finder_controller.SessionManager.get_id_user')
    def test_recover_group_success(self, mock_get_id_user, mock_search_group, mock_format_data):
        # Simulaciones
        mock_get_id_user.return_value = 1
        mock_search_group.return_value = ['grupo1', 'grupo2']
        mock_format_data.return_value = [{'nombre': 'grupo1'}, {'nombre': 'grupo2'}]

        result = GroupFinderController.recover_group("grupo")

        self.assertTrue(result['success'])
        self.assertEqual(result['response'], "Se recuperaron los datos del grupo.")
        self.assertIn('grupos', result['data'])
        self.assertEqual(len(result['data']['grupos']), 2)

    @patch('src.controlador.group_finder_controller.GroupFinder.search_for_group_by_name', side_effect=Exception("Fallo en DB"))
    @patch('src.controlador.group_finder_controller.SessionManager.get_id_user')
    def test_recover_group_failure(self, mock_get_id_user, mock_search_group):
        mock_get_id_user.return_value = 1

        result = GroupFinderController.recover_group("grupo")

        self.assertFalse(result['success'])
        self.assertIn("No se pudieron recuperar los datos", result['response'])
        self.assertIsNone(result['data']['grupos'])

    def test_recover_group_empty_name(self):
        with patch('src.controlador.group_finder_controller.SessionManager.get_id_user') as mock_get_id_user, \
             patch('src.controlador.group_finder_controller.GroupFinder.search_for_group_by_name') as mock_search_group, \
             patch('src.controlador.group_finder_controller.DataFormat.convert_to_dict_groups_data_with_out_rol') as mock_format_data:

            mock_get_id_user.return_value = 1
            mock_search_group.return_value = ['grupo_sugerido']
            mock_format_data.return_value = [{'nombre': 'grupo_sugerido'}]

            result = GroupFinderController.recover_group("")

            self.assertTrue(result['success'])
            self.assertEqual(result['response'], "Se recuperaron los datos del grupo.")
            self.assertEqual(result['data']['grupos'][0]['nombre'], 'grupo_sugerido')

    @patch('src.controlador.group_finder_controller.DataFormat.convert_to_dict_groups_data')
    @patch('src.controlador.group_finder_controller.GroupFinder.search_for_group_by')
    @patch('src.controlador.group_finder_controller.SessionManager.get_id_user')
    def test_recover_group_by_filters_success(self, mock_get_user, mock_search, mock_convert):
        # Simular ID de usuario de sesión
        mock_get_user.return_value = 99

        # Simular retorno de búsqueda de grupos
        mock_search.return_value = ['grupo1', 'grupo2']

        # Simular conversión de grupos a diccionario
        mock_convert.return_value = [{'id': 1}, {'id': 2}]

        resultado = GroupFinderController.recover_group_by_filters("grupo", "admin")

        self.assertTrue(resultado['success'])
        self.assertIn("Se recuperaron los grupos", resultado['response'])
        self.assertEqual(resultado['data']['grupos'], [{'id': 1}, {'id': 2}])

        mock_get_user.assert_called_once()
        mock_search.assert_called_once_with(id_usuario=99, nombre="grupo", rol="admin")
        mock_convert.assert_called_once_with(['grupo1', 'grupo2'])

    @patch('src.controlador.group_finder_controller.DataFormat.convert_to_dict_groups_data')
    @patch('src.controlador.group_finder_controller.GroupFinder.search_for_group_by', side_effect=Exception("Error DB"))
    @patch('src.controlador.group_finder_controller.SessionManager.get_id_user')
    def test_recover_group_by_filters_error(self, mock_get_user, mock_search, mock_convert):
        # Simular ID de usuario
        mock_get_user.return_value = 50

        resultado = GroupFinderController.recover_group_by_filters("grupo", "viewer")

        self.assertFalse(resultado['success'])
        self.assertIn("No se recuperaron los grupos", resultado['response'])
        self.assertIsNone(resultado['data']['grupos'])

        mock_get_user.assert_called_once()
        mock_convert.assert_not_called()

if __name__ == '__main__':
    unittest.main()
