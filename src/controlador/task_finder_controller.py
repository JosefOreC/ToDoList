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
    __funtion_to_recover = {'n': TaskFinder.search_for_tasks_by_name,
                            'd': TaskFinder.search_for_task_by_date,
                            'c': TaskFinder.search_for_task_by_check,
                            'g': TaskFinder.search_for_tasks_by_group,
                            'nd': TaskFinder.search_for_task_by_date_and_name,
                            'nc': TaskFinder.search_for_task_by_check_name,
                            'ng': TaskFinder.search_for_tasks_by_name_group,
                            'dc': TaskFinder.search_for_task_by_check_date,
                            'dg': TaskFinder.search_for_task_by_date_group,
                            'cg': TaskFinder.search_for_task_by_check_group,
                            'ndc': TaskFinder.search_for_task_by_check_date_name,
                            'dcg': TaskFinder.search_for_task_by_check_date_group,
                            'ndcg': TaskFinder.search_for_task_by_check_date_name_group
    }

    @staticmethod
    def recover_task(id_grupo=None, nombre=None, realizado=None, fecha_ini=None, fecha_fin=None, archivado=False):
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

        if funcion == '':
            return {
                'success': True,
                'response': "No hay argumentos de busqueda",
                'data':{
                    'tareas':None
                }
            }

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
