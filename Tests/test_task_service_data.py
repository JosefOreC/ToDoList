import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError
from datetime import date

from src.modelo.service.task_service.task_service_data import TaskServiceData
from src.modelo.entities.modelo import Tarea, UsuarioTarea


class TestTaskServiceData(unittest.TestCase):

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_insert_task_user(self, mock_session):
        # Configuración del mock
        mock_session.add_all = MagicMock()
        mock_session.flush = MagicMock()
        mock_session.commit = MagicMock()

        tarea = Tarea(IDTarea=1, Nombre='Tarea de Prueba')
        usuario_tarea = [UsuarioTarea(IDUsuario=1, IDTarea=0, Disponible=True)]

        TaskServiceData.insert_task_user(tarea, usuario_tarea)

        mock_session.add_all.assert_called()  # Verifica que se llamara a add_all
        mock_session.commit.assert_called()  # Verifica que se llamara a commit

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_update_task_user(self, mock_session):
        # Configuración del mock
        mock_session.commit = MagicMock()

        TaskServiceData.update_task_user(1, 1, nombre='Nueva Tarea')

        mock_session.commit.assert_called()  # Verifica que se llamara a commit

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_get_tasks_user_list_date(self, mock_session):
        # Configuración del mock
        mock_session.query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [
            (Tarea(IDTarea=1, Nombre='Tarea 1'), True, False, 1)
        ]

        resultados = TaskServiceData.get_tasks_user_list_date(1, date.today())

        self.assertEqual(len(resultados), 1)  # Verifica que se devolvieron resultados
        self.assertEqual(resultados[0][0].Nombre, 'Tarea 1')  # Verifica el nombre de la tarea

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_get_tasks_user_list_all(self, mock_session):
        # Configuración del mock
        mock_session.query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [
            (Tarea(IDTarea=1, Nombre='Tarea 1'), True, False, 1)
        ]

        resultados = TaskServiceData.get_tasks_user_list_all(1)

        self.assertEqual(len(resultados), 1)  # Verifica que se devolvieron resultados
        self.assertEqual(resultados[0][0].Nombre, 'Tarea 1')  # Verifica el nombre de la tarea

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_get_task(self, mock_session):
        # Configuración del mock
        mock_session.query.return_value.filter_by.return_value.first.return_value = Tarea(IDTarea=1, Nombre='Tarea 1')

        tarea = TaskServiceData.get_task(1)

        self.assertIsNotNone(tarea)  # Verifica que la tarea no sea None
        self.assertEqual(tarea.Nombre, 'Tarea 1')  # Verifica el nombre de la tarea

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_soft_delete_task(self, mock_session):
        # Configuración del mock para UpdateTask
        mock_update_task = patch('src.modelo.service.task_service.task_service_data.UpdateTask', autospec=True).start()
        mock_update = mock_update_task.return_value
        mock_update.update_activo = MagicMock()
        mock_session.commit = MagicMock()

        TaskServiceData.soft_delete_task(1)

        mock_update.update_activo.assert_called_with(False)  # Verifica que se llame a update_activo con False
        mock_session.commit.assert_called()  # Verifica que se llamara a commit

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_delete_task(self, mock_session):
        # Configuración del mock
        mock_session.query.return_value.filter_by.return_value.all.return_value = [UsuarioTarea(IDUsuario=1, IDTarea=1)]
        mock_session.query.return_value.filter_by.return_value.first.return_value = Tarea(IDTarea=1, Nombre='Tarea 1')
        mock_session.delete = MagicMock()
        mock_session.commit = MagicMock()

        TaskServiceData._TaskServiceData__delete_task(1)  # Llamamos al método privado

        mock_session.delete.assert_called()  # Verifica que se llamara a delete
        mock_session.commit.assert_called()  # Verifica que se llamara a commit

    @patch('src.modelo.service.task_service.task_service_data.session')
    def test_get_relations_of_task(self, mock_session):
        # Configuración del mock
        mock_session.query.return_value.filter_by.return_value.all.return_value = [
            UsuarioTarea(IDUsuario=1, IDTarea=1)
        ]

        relaciones = TaskServiceData.get_relations_of_task(1)

        self.assertEqual(len(relaciones), 1)  # Verifica que se devolvieron relaciones
        self.assertEqual(relaciones[0].IDUsuario, 1)  # Verifica el ID del usuario

if __name__ == '__main__':
    unittest.main()