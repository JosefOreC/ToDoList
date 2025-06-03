"""

"""

from src.modelo.service.session_service.session_manager import SessionManager
from src.controlador.task_controller import TaskController
from src.modelo.service.data_service.data_format import DataFormat

class MainViewController:
    @staticmethod
    def log_out():
        SessionManager.log_out()
        return True, 'Se cerró sesión con exito'

    @staticmethod
    def recover_task_today_with_format():
        is_task_recover, response =TaskController.recover_tasks_today()

        if not is_task_recover or not response:
            return is_task_recover, response

        tareas = DataFormat.convert_to_dict_task_data(response)

        return is_task_recover, tareas



