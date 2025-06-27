import unittest
from unittest.mock import patch, MagicMock
from src.modelo.service.task_service.update_task import UpdateTask

class TestUpdateTask(unittest.TestCase):

    @patch('src.modelo.service.task_service.update_task.session')
    def setUp(self, mock_session):
        self.mock_session = mock_session
        self.mock_tarea = MagicMock()
        self.mock_usuario_tarea = MagicMock()

        # Mock the session query response
        self.mock_session.query.return_value.filter_by.return_value.first.side_effect = [
            self.mock_tarea,
            self.mock_usuario_tarea
        ]

        self.updater = UpdateTask(1, 2)

    def test_update_name(self):
        self.updater.update_name('Nuevo nombre')
        self.assertEqual(self.mock_tarea.Nombre, 'Nuevo nombre')

    def test_update_activo(self):
        self.updater.update_activo(True)
        self.assertTrue(self.mock_tarea.Activo)

    def test_update_archivado(self):
        self.updater.update_archivado(True)
        self.assertTrue(self.mock_usuario_tarea.Archivado)

    def test_update_fecha(self):
        self.updater.update_fecha('2025-06-27')
        self.assertEqual(self.mock_tarea.Fecha_programada, '2025-06-27')

    def test_update_prioridad(self):
        self.updater.update_prioridad(5)
        self.assertEqual(self.mock_tarea.Prioridad, 5)

    def test_update_disponible(self):
        self.updater.update_disponible(False)
        self.assertFalse(self.mock_usuario_tarea.Disponible)

    @patch('src.modelo.service.task_service.update_task.session')
    def test_update_realizado_type_check_false(self, mock_session):
        self.mock_tarea.type_check = False
        updater = UpdateTask(1, 2)
        updater._UpdateTask__tarea = self.mock_tarea
        updater._UpdateTask__usuario_tarea = self.mock_usuario_tarea

        updater.update_realizado(True)
        self.assertTrue(self.mock_usuario_tarea.Realizado)

    @patch('src.modelo.service.task_service.update_task.session')
    def test_update_realizado_type_check_true(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.all.return_value = [
            MagicMock(), MagicMock()
        ]
        self.mock_tarea.type_check = True

        updater = UpdateTask(1, 2)
        updater._UpdateTask__tarea = self.mock_tarea
        updater._UpdateTask__usuario_tarea = MagicMock(IDTarea=1, IDGrupo=2)

        updater.update_realizado(False)
        for usuario_tarea in mock_session.query.return_value.filter_by.return_value.all.return_value:
            self.assertFalse(usuario_tarea.Realizado)

    def test_update_detalle(self):
        self.updater.update_detalle("Detalle actualizado")
        self.assertEqual(self.mock_tarea.Detalle, "Detalle actualizado")

if __name__ == '__main__':
    unittest.main()
