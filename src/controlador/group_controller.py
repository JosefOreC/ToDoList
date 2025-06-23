"""


"""


from sqlalchemy.exc import IntegrityError

from src.controlador.task_controller import TaskController
from src.modelo.service.group_service.register_group import RegisterGroup, GroupServiceData
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.user_service.user_service_data import UserServiceData
from src.modelo.service.data_service.data_format import DataFormat, date
from src.modelo.entities.rol import Rol


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
        if GroupController.get_rol_in_group(id_grupo) != 'master':
            return False, "No se tienen los permisos para realizar estos cambios."

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
                'grupos': DataFormat.convert_to_dict_groups_data(resultados) if resultados else None
            }
        }

    @staticmethod
    def get_data_to_view(id_grupo):
        def return_data(success, response, grupo=None, tareas=None,usuario=None,miembros=None):
            return {
                'success': success,
                'response': response,
                'data':{
                    'grupo': grupo,
                    'tareas': tareas,
                    'usuario': {
                        'rol': usuario
                    },
                    'miembros': miembros
                }
            }

        try:
            data_grupo = GroupServiceData.get_group_for_id(id_grupo)
        except Exception as E:
            return return_data(False, f"No se pudieron recuperar los datos del grupo. \n{E}")

        data_grupo = DataFormat.convert_to_dict_group_data(data_grupo)


        data_tasks = TaskController.get_tasks_of_group_date(fecha=date.today(), id_grupo=id_grupo)

        if not data_tasks.get('success'):
            return return_data(False, response=f"No se pudieron recuperar los datos de tareas del grupo. "
                                               f"\n{ data_tasks.get('response')}", grupo=data_grupo)

        data_tasks = data_tasks.get('data').get('tareas')

        try:
            data_user = GroupController.get_rol_in_group(id_grupo)
        except Exception as E:
            return return_data(False, response=f'No se pudieron recuperar los datos del usuario \n{E}',
                               grupo=data_grupo, tareas=data_tasks)

        try:
            data_members = GroupController.get_all_members_with_rol(id_grupo)
        except Exception as E:
            return return_data(False, response=f'No se pudieron recuperrar los miembros. \n{E}',
                               grupo=data_grupo, tareas=data_tasks, usuario=data_user)

        data_members = DataFormat.convert_to_dict_member_data_group(data_members)

        return return_data(True, "Se recuperaron los datos", grupo=data_grupo, tareas= data_tasks,
                           usuario=data_user, miembros= data_members)


    @staticmethod
    def set_rol_member(alias_member: str, id_grupo: int, rol: Rol):

        if GroupController.get_rol_in_group(id_grupo) != 'master':
            return False, "No se tienen los permisos para realizar estos cambios."

        try:
            id_member = UserServiceData.recover_id_user_for_alias(alias_member)
        except Exception as E:
            return {
                'success': False,
                'response': f'No se pudo recuperar los datos del usuario. \n{E}'
            }

        try:
            GroupServiceData.change_rol_of_member(id_grupo, id_member, rol)
            success = True
            response = "Se guardaron los cambios."
        except Exception as E:
            success = False
            response = f"No se pudo actualizar el rol del usuario {alias_member}. \n{E}"

        return {
            'success': success,
            'response': response
        }

    @staticmethod
    def set_rol_members(id_grupo: int, lista_cambios: list[list[str, Rol]]):
        if GroupController.get_rol_in_group(id_grupo) != 'master':
            return False, "No se tienen los permisos para realizar estos cambios."
        bad_responses = []
        for alias, rol in lista_cambios:
            request = GroupController.set_rol_member(alias_member=alias, id_grupo=id_grupo, rol=rol)
            if not request.get('success'):
                bad_responses.append(request.get('response'))

        return {
            'success': True if not bad_responses else False,
            'response': 'Se guardaron los cambios' if not bad_responses else bad_responses
        }

    @staticmethod
    def update_data_group(id_grupo, nombre: str = None, descripcion: str = None):

        if GroupServiceData.get_rol_in_group(id_usuario=SessionManager.get_id_user(), id_grupo=id_grupo) != Rol.master:
            return {
                'success': False,
                'response': "No se tienen permisos para realizar esta acción."
            }

        if not (nombre or descripcion):
            return {
                'success': False,
                'response': "No se hicieron cambios."
            }

        try:
            GroupServiceData.update_group(id_grupo=id_grupo, nombre=nombre, descripcion=descripcion)
            success = True
            response = "Se guardaron los cambios."
        except Exception as E:
            success = False
            response = f"No se pudieron guardar los cambios. \n{E}"

        return {
            'success': success,
            'response': response
        }

    @staticmethod
    def out_of_group(id_grupo, delete_all_tasks, alias_new_master:str=None):

        id_new_master=UserServiceData.recover_id_user_for_alias(alias_new_master) if alias_new_master else None
        try:
            GroupServiceData.out_member_group_session_manager(id_grupo=id_grupo, new_master=id_new_master,
                                                              delete_all_task=delete_all_tasks)
            return {
                'success': True,
                'response': 'Saliste del grupo correctamente'
            }
        except Exception as E:
            return {
                'success': False,
                'response': f'No se pudo salir del grupo. \n{E}'
            }

    @staticmethod
    def expel_member(id_grupo, alias_usuario):
        id_usuario = UserServiceData.recover_id_user_for_alias(alias_usuario)
        try:
            GroupServiceData.expel_member_group(id_grupo=id_grupo, id_usuario=id_usuario, delete_registers=False)
            success = True
            response = f"Se expulsó al usuario {alias_usuario} exitosamente."
        except Exception as E:
            success = False
            response = f"No se pudo expulsar al usuario {alias_usuario}.\n{E}"

        return {
            'success': success,
            'response': response
        }