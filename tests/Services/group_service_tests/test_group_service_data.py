import unittest
from unittest.mock import patch, MagicMock
from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.entities.modelo import Rol


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


if __name__ == '__main__':
    unittest.main()
