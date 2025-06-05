"""


"""
from sqlalchemy.exc import IntegrityError
from src.modelo.service.group_service.register_group import RegisterGroup, GroupServiceData
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.user_service.user_service_data import UserServiceData


class GroupController:
    @staticmethod
    def register_group(nombre: str, descripcion: str = None, miembros_alias: list[str]=None) -> bool and str:
        grupo = RegisterGroup.create_primitive_group(nombre, id_master=SessionManager.get_instance().usuario.IDUsuario,
                                                     descripcion=descripcion)

        miembros_id = [GroupController.add_member_group(miembro_alias) for miembro_alias in miembros_alias]

        try:
            RegisterGroup(grupo, miembros_id).register_group()
            return True, "Se agregó el grupo con éxito"
        except IntegrityError:
            return False, f"No se pudo guardar el grupo. \n Ya existe un grupo con el mismo nombre."
        except Exception as E:
            return False, f"No se pudo guardar el grupo. \n {E}"

    @staticmethod
    def add_member_group(alias_usuario):
        return UserServiceData.recover_id_user_for_alias(alias_usuario)

    @staticmethod
    def get_all_members(id_grupo):
        return GroupServiceData.get_all_members_with_rol(id_grupo)
    @staticmethod
    def get_all_members_with_rol(id_grupo):
        return GroupServiceData.get_all_members_with_rol(id_grupo)

    @staticmethod
    def is_user_exits(alias_usuario) -> bool and str:

        try:
            if is_user:=UserServiceData.is_user_with_alias_exits(alias_usuario):
                return is_user, "Usuario existente."

            return is_user, "Usuario no existente."

        except Exception as E:
            return False, f"No se pudo recuperar de la base de datos. \n{E}"

    @staticmethod
    def get_groups_editable() -> list[list[int,str]]:
        return GroupServiceData.get_groups_editor_or_master_with_id(SessionManager.get_id_user())



