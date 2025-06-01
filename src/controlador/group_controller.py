"""


"""
from sqlalchemy.exc import IntegrityError
from src.modelo.service.group_service.register_group import RegisterGroup, GroupServiceData
from src.modelo.service.session_service.session_manager import SessionManager

class GroupController:
    @staticmethod
    def register_group(nombre: str, descripcion: str = None, miembros_id: list[int]=None) -> bool and str:
        grupo = RegisterGroup.create_primitive_group(nombre, id_master=SessionManager.get_instance().usuario.IDUsuario,
                                                     descripcion=descripcion)
        try:
            RegisterGroup(grupo, miembros_id).register_group()
            return True, "Se agregó el grupo con éxito"
        except IntegrityError:
            return False, f"No se pudo guardar el grupo. \n Ya existe un grupo con el mismo nombre."
        except Exception as E:
            return False, f"No se pudo guardar el grupo. \n {E}"

