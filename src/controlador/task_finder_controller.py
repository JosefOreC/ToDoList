"""
    Encargado de conectar la vista de buscador de tareas con el servicio de recuperación de datos de tareas
"""
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.task_service.task_finder import TaskFinder
from src.modelo.service.data_service.data_format import DataFormat

class TaskFinderController:
    """
        Clase controlador encargada de recuperar datos de las tareas por buscador
        el diccionario __funtion_to_recover tiene una metodologia para seleccionar la funcion de buscador, siendo que
        buscar por:
        n = nombre
        d = fecha
        c = check
        g = grupo
        siendo las diferentes convinaciones la forma de busqueda
    """

    @staticmethod
    def recover_task(id_grupo=None, nombre=None, realizado=None, fecha_ini=None, fecha_fin=None, archivado=False
                     , prioridad: list[str] | None = None):

        argumentos = {'id_usuario': SessionManager.get_id_user()}
        funcion = ''

        if nombre and nombre != '':
            funcion+='n'
            argumentos['nombre'] = nombre

        if fecha_ini:
            funcion+='d'
            argumentos['fecha_ini']=fecha_ini

        if fecha_fin:
            if 'd' not in funcion:
                funcion+='d'
            argumentos['fecha_fin']=fecha_fin

        if realizado is not None:
            funcion+='c'
            argumentos['realizado']=realizado

        if id_grupo:
            funcion+='g'
            argumentos['id_grupo']=id_grupo

        argumentos['archivado']=archivado

        if prioridad:
            argumentos['prioridad']=prioridad

        """
        try:
            resultados = TaskFinderController.__funtion_to_recover.get(funcion)(**argumentos)
            success = True
            response = "Se recuperaron los datos de las tareas."
        except Exception as E:
            resultados = None
            success = False
            response = f"No se pudieron recuperar los datos.\n{E}"

        return{
            'success' : success,
            'response' : response,
            'data':{
                'tareas': DataFormat.convert_to_dict_task_data(resultados) if resultados else None
            }
        }
        """

        try:
            resultados = TaskFinder.search_for_task_by(**argumentos)
            success = True
            response = "Se recuperaron los datos de las tareas."
        except Exception as E:
            resultados = None
            success = False
            response = f"No se pudieron recuperar los datos.\n{E}"

        return {
            'success': success,
            'response': response,
            'data': {
                'tareas': DataFormat.convert_to_dict_task_data(resultados) if resultados else None
            }
        }


