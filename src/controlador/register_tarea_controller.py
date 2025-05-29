"""


"""

from src.modelo.entities.tarea import Tarea
from src.modelo.service.task_service.register_task import RegisterTask
from src.modelo.format_data import DataFormat

class RegisterTaskController:
    @staticmethod
    def event_register_task_user(nombre: str, fecha: str, prioridad: int):
        try:
            fecha = DataFormat.convertir_fecha(fecha)
        except Exception as E:
            return False, f"Fecha no valida. Error {E}"

        try:
            prioridad = int(prioridad)
        except ValueError as E:
            return False, E
        except TypeError as E:
            return False, E

        tarea = Tarea(Nombre=nombre, Fecha_programada=fecha, Prioridad=prioridad)
        return RegisterTask(tarea).register_task()


