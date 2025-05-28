"""


"""

from src.modelo.entities.tarea import Tarea
from src.modelo.service.task_service.register_task import RegisterTask
from datetime import datetime

class RegisterTaskController:
    @staticmethod
    def event_register_task_user(nombre: str, fecha: str, prioridad: int):
        try:
            fecha = RegisterTaskController.convertir_fecha(fecha)
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

    @staticmethod
    def convertir_fecha(fecha: str):
        return datetime.strptime(fecha, "%d-%m-%Y")
