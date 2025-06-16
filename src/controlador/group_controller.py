"""


"""
from http.client import responses

from sqlalchemy.exc import IntegrityError
from src.modelo.service.group_service.register_group import RegisterGroup, GroupServiceData
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.user_service.user_service_data import UserServiceData
from src.modelo.service.data_service.data_format import DataFormat


class GroupController:
    """Controlador encargado de manejar las operaciones relacionadas a los grupos."""

    @staticmethod
    def register_group(nombre: str, descripcion: str = None,
                       miembros_alias: list[str]=None) -> bool and str:
        """Registra un nuevo grupo con su respectiva descripción y miembros.

        Args:
            nombre (str): Nombre del grupo.
            descripcion (str, optional): Descripción del grupo. Por defecto None.
            miembros_alias (list[str], optional): Lista de alias de los
                                            miembros a agregar. Por defecto None.

        Returns:
        tuple: (bool, str) indicando si se registró correctamente y un mensaje descriptivo.
                """

        grupo = RegisterGroup.create_primitive_group(nombre,
                                                     id_master=SessionManager.get_instance().usuario.IDUsuario,
                                                     descripcion=descripcion)

        miembros_id = [GroupController.recover_id_user(miembro_alias)
                       for miembro_alias in miembros_alias]

        try:
            RegisterGroup(grupo, miembros_id).register_group()
            return True, "Se agregó el grupo con éxito"
        except IntegrityError:
            return False, f"No se pudo guardar el grupo. \n Ya existe un grupo con el mismo nombre."
        except Exception as E:
            return False, f"No se pudo guardar el grupo. \n {E}"

    @staticmethod
    def recover_id_user(alias_usuario):
        """Recupera el ID de un usuario a partir de su alias.

        Args:
            alias_usuario (str): Alias del usuario.

        Returns:
            int: ID del usuario correspondiente al alias.
        """
        return UserServiceData.recover_id_user_for_alias(alias_usuario)

    @staticmethod
    def get_all_members(id_grupo):
        """Obtiene todos los miembros de un grupo, incluyendo sus roles.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            list: Lista de miembros con sus roles.
        """
        return GroupServiceData.get_all_members_with_rol(id_grupo)

    @staticmethod
    def get_all_members_with_rol(id_grupo):
        """Alias adicional para obtener todos los miembros de un grupo con sus roles.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            list: Lista de miembros con roles.
        """
        return GroupServiceData.get_all_members_with_rol(id_grupo)

    @staticmethod
    def is_user_exits(alias_usuario) -> bool and str:
        """Verifica si un usuario con determinado alias existe y no es el creador del grupo.

        Args:
            alias_usuario (str): Alias del usuario a verificar.

        Returns:
            tuple: (bool, str) indicando si existe y un mensaje descriptivo.
        """

        if alias_usuario == SessionManager.get_instance().usuario.Alias:
            return False, (f"No se puede agregar el usuario {alias_usuario} "
                           f"porque es el que está creando el grupo.\n"
                           f"Ya está incluido.")
        try:
            if is_user:=UserServiceData.is_user_with_alias_exits(alias_usuario):
                return is_user, "Usuario existente."

            return is_user, "Usuario no existente."

        except Exception as E:
            return False, f"No se pudo recuperar de la base de datos. \n{E}"

    @staticmethod
    def is_member_in_group(id_grupo, alias_usuario):
        """Verifica si un usuario ya pertenece a un grupo.

        Args:
            id_grupo (int): ID del grupo.
            alias_usuario (str): Alias del usuario.

        Returns:
            bool: True si el usuario ya está en el grupo, False en caso contrario.
        """
        id_usuario = UserServiceData.recover_id_user_for_alias(alias_usuario)
        return GroupServiceData.is_user_in_group(id_grupo, id_usuario)

    @staticmethod
    def get_groups_editable() -> list[list[int,str]]:
        """Obtiene los grupos donde el usuario actual tiene rol de editor o master.

        Returns:
            list: Lista de grupos con IDs y nombres.
        """
        return GroupServiceData.get_groups_editor_or_master_with_id(SessionManager.get_id_user())

    @staticmethod
    def get_rol_in_group(id_grupo):
        """Obtiene el rol del usuario actual en un grupo específico.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            str: Rol del usuario dentro del grupo.
        """
        return GroupServiceData.get_rol_in_group(SessionManager.get_id_user(), id_grupo).name

    @staticmethod
    def get_group_master_alias(id_grupo):
        """Obtiene el alias del usuario que es master (creador) del grupo.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            str: Alias del usuario master del grupo.
        """
        return GroupServiceData.get_master_alias_of_group(id_grupo)

    @staticmethod
    def add_members_to_group(id_grupo, miembros: tuple[str] or str):
        """Agrega uno o más miembros a un grupo específico.

        Args:
            id_grupo (int): ID del grupo.
            miembros (str or tuple[str]): Alias o lista de alias de usuarios a agregar.

        Returns:
            tuple: (bool, str) indicando si se agregó correctamente o no, y un mensaje.
        """
        try:
            if isinstance(miembros, list):
                miembros_id = [GroupController.recover_id_user(miembro)for miembro in miembros
                               if not GroupController.is_member_in_group(id_grupo=id_grupo, alias_usuario=miembro)]
            else:
                miembros_id = GroupController.recover_id_user(miembros)
        except Exception as E:
            return False, f"No se pudo agregar los miembro(s). \n {E}"


        try:
            GroupServiceData.add_members_in_group(id_grupo, miembros_id)
            return True, "Se guardaron los nuevos miembros correctamente."
        except Exception as E:
            return False, f"No se pudo agregar los miembro(s). \n {E}"

    @staticmethod
    def get_all_groups_of_session_manager():
        try:
            resultados = GroupServiceData.get_all_user_groups(SessionManager.get_id_user())
            success=True
            response = "Se recuperaron los datos."
        except Exception as E:
            success=False
            response = f"No se pudieron recuperar los datos. \n{E}"
            resultados=None

        return {
            'success': success,
            'response': response,
            'data':{
                'grupos': DataFormat.convert_to_dict_group_data(resultados) if resultados else None
            }
        }