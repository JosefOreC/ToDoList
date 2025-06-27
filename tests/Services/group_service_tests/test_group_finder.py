import unittest
from unittest.mock import patch, MagicMock
from src.modelo.service.group_service.group_finder import GroupFinder


class TestGroupFinder(unittest.TestCase):

    @patch('src.modelo.service.group_service.group_finder.session')
    def test_search_for_group_by_name_with_results(self, mock_session):
        """
        Comprueba que se devuelve la lista de grupos cuando la consulta
        encuentra coincidencias.
        """
        # Arrange ──────────────────────────────────────────────────────────────
        fake_group_list = ['grupo1', 'grupo2']

        # Creamos la cadena de mocks: session.query().join().filter().all()
        mock_query = MagicMock()
        mock_join = MagicMock()
        mock_filter = MagicMock()

        mock_session.query.return_value = mock_query
        mock_query.join.return_value = mock_join
        mock_join.filter.return_value = mock_filter
        mock_filter.all.return_value = fake_group_list

        # Act ─────────────────────────────────────────────────────────────────
        result = GroupFinder.search_for_group_by_name(10, "Alpha")

        # Assert ──────────────────────────────────────────────────────────────
        self.assertEqual(result, fake_group_list)
        mock_session.query.assert_called_once()          # se hizo query
        mock_query.join.assert_called_once()             # se hizo join
        mock_join.filter.assert_called_once()            # se aplicó filtro
        mock_filter.all.assert_called_once()             # se llamó all()

    @patch('src.modelo.service.group_service.group_finder.session')
    def test_search_for_group_by_name_no_results(self, mock_session):
        """
        Comprueba que se devuelve una lista vacía cuando la consulta
        no encuentra coincidencias.
        """
        # Arrange
        mock_query = MagicMock()
        mock_join = MagicMock()
        mock_filter = MagicMock()

        mock_session.query.return_value = mock_query
        mock_query.join.return_value = mock_join
        mock_join.filter.return_value = mock_filter
        mock_filter.all.return_value = []  # sin resultados

        # Act
        result = GroupFinder.search_for_group_by_name(5, "Inexistente")

        # Assert
        self.assertEqual(result, [])
        mock_filter.all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
