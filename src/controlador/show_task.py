from src.modelo.service.task_service.task_service_data import TaskServiceData

class TaskController:
    @staticmethod
    def recover_tasks_today():
        try:
            resultados = TaskServiceData.get_tasks_session_user_list_today()
        except Exception as E:
            return False, f"No se pudo recuperar las tareas. \n{E}"

        if resultados:
            return True, resultados
        return True, None