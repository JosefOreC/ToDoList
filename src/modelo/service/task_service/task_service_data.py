"""
Clase que controla la entidad tarea y relacionados
desde la base de datos CRUD.
"""
from typing import Any

from sqlalchemy.exc import IntegrityError


from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.modelo import UsuarioTarea, Tarea, Rol
from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.data_service.data_format import DataFormat
from datetime import date
from src.modelo.service.task_service.update_task import UpdateTask
from src.modelo.service.user_service.user_service_data import UserServiceData


class TaskServiceData:
    @staticmethod
    def insert_task_user(tarea: Tarea, usuario_tarea: list[UsuarioTarea]):
        """
        Inserta una tarea y sus relaciones con usuarios en la base de datos.

        Args:
            tarea (Tarea): Instancia de la tarea a guardar.
            usuario_tarea (list[UsuarioTarea]): Lista de relaciones usuario-tarea.
        """
        session.add_all([tarea])
        session.flush()
        for relacion in usuario_tarea:
            relacion.IDTarea = tarea.IDTarea
        session.add_all(usuario_tarea)
        session.commit()

    @staticmethod
    def update_task_user(id_usuario, id_tarea, nombre = None,
                         fecha = None, prioridad = None, disponible = None,
                         realizado = None, detalle = None, archivado = None, type_check=None):

        """
        Actualiza los datos de una tarea relacionada a un usuario específico.

        Args:
            id_usuario (int): ID del usuario.
            id_tarea (int): ID de la tarea.
            nombre (str): Nuevo nombre de la tarea.
            fecha (date): Nueva fecha programada.
            prioridad (int, optional): Nueva prioridad.
            disponible (bool, optional): Estado de disponibilidad.
            realizado (bool, optional): Estado de realización.
            detalle (str, optional): Nuevo detalle de la tarea.
            archivado (bool, optional): Estado de archivado.
        """

        if (id_grupo:=TaskServiceData.get_id_group_of_task(id_tarea)) is not None:
            rol_sm = GroupServiceData.get_rol_in_group(id_usuario=SessionManager.get_id_user(), id_grupo=id_grupo)
            is_sm_master = rol_sm == Rol.master
            if not is_sm_master:
                is_sm_editor = rol_sm == Rol.editor

                if not is_sm_editor:
                    raise Exception("No se tienen Permisos para editar esta tarea.")

                rol_user_edit = GroupServiceData.get_rol_in_group(id_usuario=id_usuario, id_grupo=id_grupo)
                is_user_edit_master = rol_user_edit == Rol.master
                if is_user_edit_master:
                    raise Exception("No se puede editar la tarea a un master.")

                is_editable = session.query(UsuarioTarea.Disponible).filter(UsuarioTarea.IDUsuario==id_usuario,
                                                                    UsuarioTarea.IDTarea==id_tarea,
                                                                    UsuarioTarea.IDGrupo==id_grupo).first()[0]

                if not is_editable:
                    raise Exception("No tienes los permisos para editar esta tarea.")

        updatedata = UpdateTask(id_tarea, id_usuario)

        if nombre:
            updatedata.update_name(nombre)
        if archivado is not None:
            updatedata.update_archivado(archivado)
        if fecha:
            updatedata.update_fecha(fecha)
        if prioridad:
            updatedata.update_prioridad(prioridad)
        if disponible is not None:
            updatedata.update_disponible(disponible)
        if realizado is not None:
            updatedata.update_realizado(realizado)
        if detalle:
            updatedata.update_detalle(detalle)
        if type_check:
            updatedata.update_type_check(type_check)

        session.commit()

    @staticmethod
    def edit_disponible_from_user(id_usuario, id_tarea, disponible):
        TaskServiceData.update_task_user(id_usuario=id_usuario, id_tarea=id_tarea, disponible=disponible)

    @staticmethod
    def edit_type_check_from_group(id_usuario, id_tarea, type_check):
        TaskServiceData.update_task_user(id_usuario=id_usuario, id_tarea=id_tarea, type_check=type_check)

    @staticmethod
    def delete_relation_task(id_usuario, id_tarea):
        """
        Se usa cuando se está eliminando una tarea de un grupo de la que ya no se es miembro (Desaparece solo
        para el usuario que lo elimina)
        :param id_usuario:
        :param id_tarea:
        :return:
        """

        usuario_tarea = session.query(UsuarioTarea).filter_by(IDUsuario=id_usuario, IDTarea=id_tarea).first()
        session.delete(usuario_tarea)
        session.commit()

    @staticmethod
    def delete_relation_task_member_group(id_usuario, id_tarea):
        """
        Se usa cuando se está eliminando una tarea de un grupo de la que ya no se es miembro (Desaparece solo
        para el usuario que lo elimina)
        :param id_usuario:
        :param id_tarea:
        :return:
        """

        if (id_grupo:=TaskServiceData.get_id_group_of_task(id_tarea)) is not None:

            rel = session.query(UsuarioTarea.Disponible).filter(UsuarioTarea.IDUsuario==SessionManager.get_id_user(),
                                                               UsuarioTarea.IDGrupo==id_grupo,
                                                               UsuarioTarea.IDTarea==id_tarea).first()[0]

            is_rol_permition = (GroupServiceData.get_rol_in_group(id_grupo=id_grupo,
                                                                  id_usuario=SessionManager.get_id_user())
                                                                in [Rol.master, Rol.editor])

            is_editable_task_for_user = rel

            if not is_rol_permition or not is_editable_task_for_user:
                raise Exception("No se tienen permisos para eliminar usuarios.")

            if GroupServiceData.get_rol_in_group(id_grupo=id_grupo, id_usuario=id_usuario) == Rol.master:
                raise Exception("No se puede quitar de una tarea de grupo al master.")


        usuario_tarea = session.query(UsuarioTarea).filter_by(IDUsuario=id_usuario, IDTarea=id_tarea).first()
        session.delete(usuario_tarea)
        session.commit()

    @staticmethod
    def get_tasks_user_list_date(usuario_id: int, fecha_inicio: str or date, fecha_fin: str or date = None,
                                 activo = True,
                                 archivado = False):
        fecha_inicio = DataFormat.convertir_data_to_date(fecha_inicio)
        if not fecha_fin:
            fecha_fin = fecha_inicio
        else:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)

        if fecha_fin < fecha_inicio:
            raise Exception(f'La fecha de inicio {fecha_inicio} es mayor a la fecha de fin {fecha_fin}. '
                            f'\nNo se recuperó datos.')
        resultados = session.query(Tarea,
                                   UsuarioTarea.Disponible,
                                   UsuarioTarea.Realizado, UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                   UsuarioTarea.IDUsuario==usuario_id).filter(UsuarioTarea.IDTarea==Tarea.IDTarea,
                                   Tarea.Fecha_programada >= fecha_inicio,
                                   Tarea.Fecha_programada <= fecha_fin,
                                   Tarea.Activo == activo,
                                   UsuarioTarea.Archivado == archivado).order_by(Tarea.Prioridad.asc()).all()
        return resultados

    @staticmethod
    def __get_all_task():
        return session.query(Tarea.Nombre, Tarea.Fecha_programada, Tarea.Detalle, Tarea.Prioridad, Tarea.Activo)

    @staticmethod
    def get_tasks_user_list_all(usuario_id: int, activo=True, archivado=False):

        resultados = session.query(Tarea,
                                    UsuarioTarea.Disponible,
                                    UsuarioTarea.Realizado, UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                    UsuarioTarea.IDUsuario == usuario_id).filter(
                                    UsuarioTarea.IDTarea == Tarea.IDTarea,
                                    Tarea.Activo == activo,
                                    UsuarioTarea.Archivado == archivado).order_by(Tarea.Prioridad.asc()).all()
        return resultados

    @staticmethod
    def get_task_user_archivade(usuario_id: int):
        return TaskServiceData.get_tasks_user_list_all(usuario_id, archivado = True)

    @staticmethod
    def get_tasks_session_user_list_date(fecha: str or date):
        usuario_id = SessionManager.get_instance().usuario.IDUsuario
        return TaskServiceData.get_tasks_user_list_date(usuario_id, fecha)

    @staticmethod
    def get_tasks_session_user_list_today():
        return TaskServiceData.get_tasks_session_user_list_date(date.today())
    
    @staticmethod
    def get_task(id_tarea):
        return session.query(Tarea).filter_by(IDTarea=id_tarea).first()
            
    @staticmethod
    def soft_delete_task(id_tarea):
        """

        :param id_tarea:
        :return:
        """
        actualizacion = UpdateTask(id_tarea)
        actualizacion.update_activo(False)
        session.commit()

    @staticmethod
    def get_relations_of_task(id_tarea):
        return session.query(UsuarioTarea).filter_by(IDTarea=id_tarea).all()

    @staticmethod
    def get_id_group_of_task(id_tarea):
        response = session.query(UsuarioTarea.IDGrupo).filter_by(IDTarea=id_tarea).first()[0]
        return response if response else None

    @staticmethod
    def is_editable_task_for_user(id_tarea, id_usuario):
        """
            Parametros: Id de la tarea e Id del usuario
            Retorna si una tarea es editable para un usuario.
        """
        return session.query(UsuarioTarea.Disponible).filter_by(IDTarea=id_tarea, IDUsuario=id_usuario).first()[0]

    @staticmethod
    def __delete_task(id_tarea):

        relaciones = TaskServiceData.get_relations_of_task(id_tarea)
        tarea = TaskServiceData.get_task(id_tarea)
        for relacion in relaciones:
            session.delete(relacion)

        session.delete(tarea)
        session.commit()

    @staticmethod
    def get_all_task_of_group_date(grupo_id, usuario_id: int, fecha_inicio: str or date, activo=True):

        fecha_inicio = DataFormat.convertir_data_to_date(fecha_inicio)

        return (session.query(Tarea, UsuarioTarea.Archivado, UsuarioTarea.Realizado, UsuarioTarea.Disponible)
        .join(UsuarioTarea, UsuarioTarea.IDTarea == Tarea.IDTarea)
        .filter(
                    UsuarioTarea.IDGrupo == grupo_id,
                    Tarea.Fecha_programada == fecha_inicio,
                    Tarea.Activo == activo,
                    UsuarioTarea.IDUsuario == usuario_id
        )).order_by(Tarea.Prioridad.asc()).all()

    @staticmethod
    def get_task_data_for_edit(id_tarea: int, id_usuario: int):
        return (session.query(Tarea, UsuarioTarea).join(UsuarioTarea, UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(Tarea.IDTarea==id_tarea, UsuarioTarea.IDUsuario==id_usuario, Tarea.Activo==True)
                .first())

    @staticmethod
    def __add_member_to_task_group(id_tarea, id_usuario, id_grupo, disponible = True):
        if session.query(1).filter(UsuarioTarea.IDUsuario==id_usuario, UsuarioTarea.IDTarea==id_tarea,
                                   UsuarioTarea.IDGrupo == id_grupo).first():
            raise Exception("Esta relación ya está agregada.", IntegrityError)

        new_rela = UsuarioTarea(IDUsuario=id_usuario, IDGrupo=id_grupo, IDTarea=id_tarea, Disponible=disponible)
        try:
            session.add_all([new_rela])
            session.commit()
        except Exception as E:
            session.rollback()
            raise Exception("No se pudo agregar la relacion.\n {E}")

    @staticmethod
    def add_members_to_task_group(id_tarea, alias_users_permitions: list[str,bool])\
            -> tuple[list[Any], list[list[str | Any]]]:
        usuarios_validos = []
        usuarios_invalidos = []
        if (id_grupo:= TaskServiceData.get_id_group_of_task(id_tarea)) is None:
            raise Exception("La tarea no pertenece a ningún Grupo.")

        if GroupServiceData.get_rol_in_group(id_usuario=SessionManager.get_id_user()
                , id_grupo=id_grupo) not in [Rol.editor, Rol.master]:
            raise Exception("No se tienen permisos para realizar estos cambios.")

        for alias, disponible in alias_users_permitions:
            try:
                temp = UserServiceData.recover_id_user_for_alias(alias)
                if not GroupServiceData.is_user_in_group(id_grupo, temp):
                    usuarios_invalidos.append([alias, "No pertenece al grupo."])
                TaskServiceData.__add_member_to_task_group(id_tarea, temp, id_grupo, disponible)
                usuarios_validos.append(alias)
            except Exception as E:
                usuarios_invalidos.append([alias, f"No se pudo por {E}"])

        return usuarios_validos, usuarios_invalidos

    @staticmethod
    def add_group_to_task_exits(id_tarea, id_grupo, miembro_disponible: list[str, bool]):
        """
        Agrega un grupo a una tarea ya existente
        :param id_tarea:
        :param id_grupo:
        :param miembro_disponible:
        :return:
        """

        rela_pr = session.query(UsuarioTarea).filter_by(IDUsuario = SessionManager.get_id_user(),
                                                        IDTarea=id_tarea).first()

        if rela_pr.IDGrupo:
            raise Exception("La tarea ya tiene un grupo.")

        rol_sm = GroupServiceData.get_rol_in_group(SessionManager.get_id_user(), id_grupo)
        is_master_or_editor = rol_sm in [Rol.master, Rol.editor]

        if not is_master_or_editor:
            raise Exception("No se tienen permisos en el grupo para agregar una tarea.")

        rela_pr.IDGrupo=id_grupo
        session.commit()

        master = GroupServiceData.get_master_alias_of_group(id_grupo)
        rela_master = [master, True]

        if miembro_disponible == 'all':
            miembros = GroupServiceData.get_all_members_alias(id_grupo)
            alias_sm = SessionManager.get_instance().usuario.Alias
            miembro_disponible = [[alias, True] for alias in miembros if alias_sm != alias]
        elif rela_master in miembro_disponible:
            pass
        elif [master, False] in miembro_disponible:
            indice = miembro_disponible.index([master, False])
            miembro_disponible[indice] = rela_master
        else:
            miembro_disponible.append(rela_master)

        TaskServiceData.add_members_to_task_group(id_tarea=id_tarea, alias_users_permitions=miembro_disponible)

