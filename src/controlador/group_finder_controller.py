"""

    Encargado de conectar la vista de buscador de grupos con el servicio de recuperación de datos de grupos

"""
from src.modelo.service.data_service.data_format import DataFormat
from src.modelo.service.group_service.group_finder import GroupFinder
from src.modelo.service.session_service.session_manager import SessionManager


class GroupFinderController:
    @staticmethod
    def recover_group(nombre):
        if not nombre:
            nombre = ''
        try:
            resultados = GroupFinder.search_for_group_by_name(id_usuario=SessionManager.get_id_user(), nombre=nombre)
            success = True
            response = "Se recuperaron los datos del grupo."
        except Exception as E:
            success = False
            response = f"No se pudieron recuperar los datos.\n{E}"
            resultados = None

        return {
            'success' : success,
            'response' : response,
            'data':{
                'grupos': DataFormat.convert_to_dict_groups_data_with_out_rol(resultados) if resultados else None
            }
        }


