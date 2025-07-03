"""
task_controller.py

Este módulo contiene el controlador encargado de manejar la lógica relacionada
con la gestión de tareas, como la recuperación, creación, modificación o eliminación
de tareas de usuario.
"""


from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.entities.tarea import Tarea
from src.modelo.entities.rol import Rol
from src.modelo.service.task_service.register_task import RegisterTask, TaskServiceData
from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.service.user_service.user_service_data import UserServiceData
from src.modelo.service.data_service.data_format import DataFormat, datetime, date

class TaskController:
    """Controlador para la gestión de tareas del usuario y de grupos."""

    @staticmethod
    def recover_tasks_today() -> dict['success': bool, 'response':str, 'data':dict['tareas':list]]:
        """Recupera las tareas programadas para el día actual del usuario en sesión.

        Returns:
            tuple: (bool, list|str) Resultado de la operación y datos o mensaje de error.
        """
        try:
            resultados = TaskServiceData.get_tasks_session_user_list_today()
            success = True
            response = f"Tareas recuperadas."
        except Exception as E:
            success = False
            response = f"No se pudo recuperar las tareas. \n{E}"
            resultados = None

        return {
            'success': success,
            'response': response,
            'data': {
                'tareas': resultados if resultados else None
            }
        }

    @staticmethod
    def recover_task_archivate():
        try:
            resultados = TaskServiceData.get_task_user_archivade(SessionManager.get_id_user())
            response = "Se recuperaron los datos."
            success = True
        except Exception as E:
            response = f"No se recuperaron los datos. \n{E}"
            success = False
            resultados = None

        return {
            'success': success,
            'response': response,
            'data': {
                'tareas': resultados
            }
        }

    @staticmethod
    def recover_all_data_task_to_view_details(id_tarea: int):
        try:
            task_data = TaskServiceData.get_task_data_for_edit(id_usuario=SessionManager.get_id_user(),
                                                               id_tarea=id_tarea)
            success = True
            response = "Se recuperaron los datos de la tarea"
        except Exception as E:
            task_data = None
            success = False
            response = f"No se pudieron recuperar los datos de la tarea. \n{E}"

        return {
            'success': success,
            'response': response,
            'data': DataFormat.convert_to_dict_tarea_to_edit(task_data) if task_data else task_data
        }

    @staticmethod
    def recover_task_date(fecha: datetime) -> dict['success': bool, 'response':str, 'data':dict['tareas':list]]:
        try:
            resultados = TaskServiceData.get_tasks_user_list_date(SessionManager.get_id_user(), fecha_inicio=fecha)
            success = True
            response = f"Tareas recuperadas."
        except Exception as E:
            success = False
            response = f"No se pudo recuperar las tareas. \n{E}"
            resultados = None

        return {
            'success': success,
            'response': response,
            'data': {
                'tareas': resultados if resultados else None
            }
        }



    @staticmethod
    def event_register_task_user(nombre: str, fecha: str, prioridad: int, detalle: str):
        """Registra una nueva tarea para el usuario en sesión.

        Args:
            nombre (str): Nombre de la tarea.
            fecha (str): Fecha programada.
            prioridad (int): Prioridad entre 1 y 5.
            detalle (str): Detalles de la tarea.

        Returns:
            tuple: (bool, str) Resultado y mensaje.
        """
        is_tarea_create, response = TaskController.__create_tarea(nombre, fecha, prioridad, detalle)
        if not is_tarea_create:
            return is_tarea_create, response
        return RegisterTask(response).register_task()

    @staticmethod
    def __create_tarea(nombre: str, fecha: str, prioridad: int, detalle: str, tipo_check: bool = False) -> bool or Tarea:
        """Crea una instancia de tarea validando fecha y prioridad.

        Args:
            nombre (str): Nombre de la tarea.
            fecha (str): Fecha en formato string.
            prioridad (int): Prioridad entre 1 y 5.
            detalle (str): Detalles.

        Returns:
            tuple: (bool, Tarea|str) Resultado y tarea o mensaje de error.
        """
        try:
            fecha = DataFormat.convertir_data_to_date(fecha)
        except Exception as E:
            return False, f"Fecha no valida. Error {E}"

        try:
            prioridad = int(prioridad)
            if prioridad <= 0 or prioridad > 5:
                return False, "Prioridad no válida, tiene que estar el 1 al 5."
        except ValueError as E:
            return False, E
        except TypeError as E:
            return False, E

        return True, Tarea(Nombre=nombre, Fecha_programada=fecha, Prioridad=prioridad, Detalle = detalle,
                           type_check=tipo_check)

    @staticmethod
    def validar_datos(fecha: str=None, prioridad: int=None):
        """Valida los datos ingresados para fecha y prioridad.

        Args:
            fecha (str, optional): Fecha.
            prioridad (int, optional): Prioridad.

        Returns:
            tuple: (bool, str) Resultado de validación y mensaje.
        """
        try:
            DataFormat.convertir_data_to_date(fecha)
        except Exception as E:
            return False, f"Fecha no valida. Error {E}"


        try:
            prioridad = int(prioridad)
            if prioridad <= 0 or prioridad > 5:
                return False, "Prioridad no válida, tiene que estar el 1 al 5."
        except ValueError as E:
            return False, E
        except TypeError as E:
            return False, E
        return True, "Datos validos"

    @staticmethod
    def event_update_task_user(id_usuario, id_tarea, nombre = None,
                         fecha = None, prioridad= None, disponible=None,
                         realizado = None, detalle = None):
        """Actualiza los campos modificables de una tarea.

        Args:
            id_usuario (int): ID del usuario.
            id_tarea (int): ID de la tarea.
            nombre (str, optional): Nombre nuevo.
            fecha (str, optional): Nueva fecha.
            prioridad (int, optional): Nueva prioridad.
            disponible (bool, optional): Disponibilidad.
            realizado (bool, optional): Estado de realización.
            detalle (str, optional): Nuevos detalles.

        Returns:
            tuple: (bool, str) Resultado y mensaje.
        """
        if not (nombre or fecha or prioridad or detalle) and disponible is None and realizado is None:
            return False, 'No hubo cambios.'

        if fecha:
            try:
                fecha = DataFormat.convertir_data_to_date(fecha)
            except ValueError as E:
                return False, E

        try:
            TaskServiceData.update_task_user(id_usuario=id_usuario, id_tarea=id_tarea, nombre=nombre,
                                             fecha=fecha, prioridad=prioridad,
                                             disponible=disponible, realizado=realizado, detalle=detalle)
            return True, 'Se guardaron los cambiós con exito'
        except Exception as E:
            return False, f'No se guardaron los cambios. \n{E}'

    @staticmethod
    def event_update_task_session_manager(id_tarea, nombre=None,
                               fecha=None, prioridad=None, disponible=None,
                               realizado=None, detalle = None):
        """Actualiza la tarea de un usuario en sesión.

        Args:
            id_tarea (int): ID de la tarea.
            (otros argumentos opcionales): Nuevos valores para actualizar.

        Returns:
            tuple: (bool, str)
        """
        return TaskController.event_update_task_user(id_usuario=SessionManager.get_instance().usuario.IDUsuario,
                                                     id_tarea=id_tarea, nombre=nombre,
                                                     fecha=fecha, prioridad=prioridad, disponible=disponible,
                                                     realizado=realizado, detalle=detalle)

    @staticmethod
    def event_check_in_task(id_tarea, realizado):
        if not TaskServiceData.is_editable_task_for_user(id_tarea, SessionManager.get_id_user()):
            return False, "El usuario no tiene permisos para checkear esta tarea."

        return TaskController.event_update_task_session_manager(id_tarea, realizado=realizado)


    @staticmethod
    def event_edit_task_session_manager(id_tarea, nombre, fecha, prioridad, detalle):
        """Edita los campos obligatorios de una tarea desde el usuario en sesión.

        Args:
            id_tarea (int): ID de la tarea.
            nombre (str): Nuevo nombre.
            fecha (str): Nueva fecha.
            prioridad (int): Nueva prioridad.
            detalle (str): Nuevos detalles.

        Returns:
            tuple: (bool, str)
       """

        if not nombre or not fecha or not prioridad:
            return False, "No se puede dejar vació ningún campo."

        if (id_grupo := TaskServiceData.get_id_group_of_task(id_tarea)) is not None:
            rol = GroupServiceData.get_rol_in_group(SessionManager.get_id_user(), id_grupo)
            if rol == Rol.miembro:
                return False, "No se tienen los permisos para editar la tarea"

        try:
            prioridad = int(prioridad)
            if prioridad <=0 or prioridad > 5:
                return False, "Prioridad no válida, tiene que estar el 1 al 5."
        except ValueError as E:
            return False, E
        except TypeError as E:
            return False, E

        return TaskController.event_update_task_session_manager(id_tarea, nombre=nombre, fecha=fecha,
                                                                prioridad=prioridad,
                                                                detalle=detalle)

    @staticmethod
    def event_register_task_group(id_grupo, nombre: str, fecha: str, prioridad: int, detalle: str, tipo_check = False,
                                  miembros_disponible: list[[str, bool]] or str = 'all'): #lista (alias, disponible)
        """Registra una nueva tarea para un grupo.

        Args:
            id_grupo (int): ID del grupo.
            nombre (str): Nombre de la tarea.
            fecha (str): Fecha de la tarea.
            prioridad (int): Prioridad entre 1 y 5.
            detalle (str): Detalles de la tarea.
            tipo_check: Tarea check 0:individual, 1:grupalmente
            miembros_disponible (list or str): Lista de tuplas (alias, disponible) o 'all'.

        Returns:
            tuple: (bool, str)
        """
        if (GroupServiceData.get_rol_in_group(id_usuario=SessionManager.get_id_user(), id_grupo=id_grupo).name
                not in ['master', 'editor']):
            return False, "No se tienen los permisos para realizar estos cambios."

        is_tarea_create, response = TaskController.__create_tarea(nombre,fecha,prioridad,detalle, tipo_check)
        if miembros_disponible != 'all':
            miembros_id_disponible = [[UserServiceData.recover_id_user_for_alias(miembro), disponible]
                                      for miembro, disponible in miembros_disponible]
        else:
            miembros_id_disponible = miembros_disponible

        if not is_tarea_create:
            return is_tarea_create, response

        return RegisterTask(tarea=response, id_grupo=id_grupo,miembro_disponible=miembros_id_disponible).register_task()

    @staticmethod
    def event_add_group_task_exits(id_tarea, id_grupo, miembros_disponible: list[[str, bool]] or str = 'all'):

        try:
            TaskServiceData.add_group_to_task_exits(id_tarea=id_tarea, id_grupo=id_grupo,
                                                    miembro_disponible=miembros_disponible)
            return True, "Se agregó el grupo a la tarea."
        except Exception as E:
            return False, f"No se pudo agregar el grupo a la tarea.\n{E}"


    @staticmethod
    def event_archive_task(id_tarea)->dict:
        """Marca una tarea como archivada.

        Args:
            id_tarea (int): ID de la tarea.

        Returns:
            tuple: (bool, str)
        """
        try:
            TaskServiceData.update_task_user(id_usuario=SessionManager.get_instance().usuario.IDUsuario,
                                             id_tarea=id_tarea, archivado=True)
            success = True
            response = "Tarea Archivada"
        except Exception as E:
            success = False
            response = "No se pudo archivar la tarea. \n{E}"

        return {
            'success': success,
            'response': response,
        }

    @staticmethod
    def event_delete_task(id_tarea):
        """Elimina lógicamente una tarea (soft delete).

        Args:
            id_tarea (int): ID de la tarea.

        Returns:
            tuple: (bool, str)
        """

        if (id_grupo:=TaskServiceData.get_id_group_of_task(id_tarea)) is not None:
            try:
                rol = GroupServiceData.get_rol_in_group(SessionManager.get_id_user(), id_grupo)
                if rol in [Rol.miembro, Rol.editor]:
                    return False, "No se tienen los permisos para eliminar la tarea"
            except:
                try:
                    TaskServiceData.delete_relation_task(id_usuario=SessionManager.get_id_user(), id_tarea=id_tarea)
                except Exception as E:
                    return False, f'No se pudo eliminar la tarea.\n{E}'
                return True, "Tarea Eliminada"
        try:
            TaskServiceData.soft_delete_task(id_tarea=id_tarea)
            return True, "Tarea eliminada"
        except Exception as E:
            return False, f"No se pudo eliminar la tarea.\n{E}"


    @staticmethod
    def get_tasks_of_group_date(fecha: date or datetime or str, id_grupo:int):
        try:
            resultados = TaskServiceData.get_all_task_of_group_date(grupo_id=id_grupo,
                                                                    usuario_id=SessionManager.get_id_user(),
                                                                    fecha_inicio=fecha)
            success = True
            response = "Se obtuvieron los datos."
        except Exception as E:
            success = False
            response = f"No se pudieron recuperar los datos. \n{E}"
            resultados = None

        return {
            'success': success,
            'response': response,
            'data': {
                'tareas': DataFormat.convert_to_dict_task_data_groups(resultados) if resultados else None
            }
        }

    @staticmethod
    def event_unarchive_task(id_tarea)->dict:
        try:
            TaskServiceData.update_task_user(id_usuario=SessionManager.get_id_user(), id_tarea=id_tarea,
                                             archivado=False)
            success = True
            response = 'Se archivó la tarea'
        except:
            success = False
            response = 'No se pudo desarchivar la tarea'

        return {
            'success': success,
            'response': response
        }

    @staticmethod
    def add_member_group_to_task(alias_users_permitions: list[str, bool], id_tarea:int):

        try:
            validos, invalidos = TaskServiceData.add_members_to_task_group(id_tarea=id_tarea,
                                                                alias_users_permitions=alias_users_permitions)
            success = True
            response = "Se agregaron a los usuarios."
        except Exception as E:
            success = False
            response = f"No se agregaron a los usuarios.\n{E}"
            validos, invalidos = None, None

        if validos:
            if len(validos) == len(alias_users_permitions):
                validos = "all"
            else:
                validos = [{'alias': miembro} for miembro in validos]
        else:
            validos = None

        invalidos= [{'alias': alias, 'fail': error} for alias, error in invalidos] if invalidos else None


        return {
            'success': success,
            'response': response,
            'data': {
                'usuarios_agregados': validos,
                'usuarios_invalidos': invalidos
            }
        }

    @staticmethod
    def edit_disponible_to_task_in_group(id_tarea, alias_usuario, disponible):
        try:
            id_usuario = UserServiceData.recover_id_user_for_alias(alias_usuario)
            TaskServiceData.edit_disponible_from_user(id_usuario=id_usuario, id_tarea=id_tarea, disponible=disponible)
            success = True
            response = "Se editó el apartado disponible de un usuario de la tarea."
        except Exception as E:
            success = False
            response = f"No se puedo editar el apartado disponible de un usuario. \n{E}"

        return {
            'success': success,
            'response': response
        }

    @staticmethod
    def edit_type_check_to_task(id_tarea, alias_usuario, type_check):
        try:
            id_usuario = UserServiceData.recover_id_user_for_alias(alias_usuario)
            TaskServiceData.edit_type_check_from_group(id_usuario, id_tarea, type_check)
            success = True
            response = "Se actualizó el tipo de check."
        except Exception as E:
            success = False
            response = f"No se puedo actualizar el tipo de check.\n{E}"

        return {
            'success': success,
            'response': response
        }

    @staticmethod
    def delete_user_of_task_group(alias_usuario, id_tarea):
        try:
            id_usuario = UserServiceData.recover_id_user_for_alias(alias_usuario)
            TaskServiceData.delete_relation_task_member_group(id_usuario, id_tarea)
            success = True
            response = f"Se quitó al usuario {alias_usuario} de la tarea."
        except Exception as E:
            success = False
            response = f"No se pudo quitar al usuario {alias_usuario} de la tarea. \n{E}"

        return {
            'success': success,
            'response': response
        }



