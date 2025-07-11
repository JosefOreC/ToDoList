"""
Módulo para la gestión de grupos y sus relaciones con usuarios.
"""


from src.modelo.entities.modelo import Grupo, UsuarioGrupo, Rol, Usuario, UsuarioTarea, Tarea
from datetime import date
from src.modelo.database_management.base.declarative_base import session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from src.modelo.service.session_service.session_manager import SessionManager


class GroupServiceData:
    @staticmethod
    def insert_group(grupo: Grupo,relation_list: list[UsuarioGrupo]):
        """Inserta un nuevo grupo junto con sus relaciones de usuario.

        Args:
            grupo (Grupo): Instancia del grupo a insertar.
            relation_list (list[UsuarioGrupo]): Lista de relaciones UsuarioGrupo a asociar.

        Raises:
            Exception: Si ya existe un grupo con el mismo nombre.
        """
        try:
            session.add_all([grupo])
            session.flush()
            for miembro in relation_list:
                miembro.IDGrupo = grupo.IDGrupo
            session.add_all(relation_list)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise Exception('Ya existe un grupo con el mismo nombre.')

    @staticmethod
    def get_group_for_id(id_grupo):
        return session.query(Grupo).filter_by(IDGrupo=id_grupo).first()

    @staticmethod
    def get_data_task_group_name(id_grupo):
        """Obtiene el nombre de un grupo dado su ID.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            str or None: Nombre del grupo o None si no existe id_grupo.
        """
        if id_grupo:
            return session.query(Grupo.Nombre).filter(Grupo.IDGrupo==id_grupo).first()[0]
        else:
            return None

    @staticmethod
    def get_all_members(id_grupo) -> list[int]:
        """Obtiene los IDs de todos los miembros de un grupo.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            list[int]: Lista con IDs de usuarios miembros.
        """
        response = session.query(UsuarioGrupo.IDUsuario).filter(UsuarioGrupo.IDGrupo==id_grupo).all()
        return [member[0] for member in response]

    @staticmethod
    def get_all_members_alias(id_grupo) -> list[str]:
        """Obtiene los IDs de todos los miembros de un grupo.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            list[int]: Lista con IDs de usuarios miembros.
        """
        response = (session.query(Usuario.Alias).join(UsuarioGrupo, UsuarioGrupo.IDUsuario==Usuario.IDUsuario)
                    .filter(UsuarioGrupo.IDGrupo == id_grupo).all())
        return [member[0] for member in response]


    @staticmethod
    def get_all_members_with_rol(id_grupo):
        """Obtiene alias y rol de todos los miembros activos de un grupo.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            list[list]: Lista de [alias, rol] para cada miembro activo.
        """
        response = (session.query(Usuario.Alias, UsuarioGrupo.rol)
                    .join(UsuarioGrupo, UsuarioGrupo.IDUsuario == Usuario.IDUsuario)
                    .filter(UsuarioGrupo.IDGrupo == id_grupo, Usuario.Estado==True).all())
        return [[member[0], member[1]] for member in response]

    @staticmethod
    def get_all_members_without_master(id_grupo) -> list[int]:
        """Obtiene los IDs de todos los miembros activos de un grupo excepto el master.

        Args:
            id_grupo (int): ID del grupo.

        Returns:
            list[int]: Lista de IDs de usuarios excepto el master.
        """
        response = session.query(UsuarioGrupo.IDUsuario).join(Usuario, Usuario.IDUsuario==UsuarioGrupo.IDUsuario).filter(
            UsuarioGrupo.IDGrupo==id_grupo, UsuarioGrupo.rol != Rol.master, Usuario.Estado==True).all()
        return [member[0] for member in response]

    @staticmethod
    def get_groups_editor_or_master(id_usuario):
        """Obtiene los nombres de los grupos donde un usuario es editor o master.

        Args:
            id_usuario (int): ID del usuario.

        Returns:
            list[str]: Lista de nombres de grupos.
        """
        response = (session.query(Grupo.Nombre).join(UsuarioGrupo, UsuarioGrupo.
                                          IDGrupo==Grupo.IDGrupo).
                                          filter(UsuarioGrupo.IDUsuario==id_usuario,
                                                 or_(UsuarioGrupo.rol == Rol.editor,
                                                     UsuarioGrupo.rol == Rol.master)).all())
        return [grupo[0] for grupo in response]

    @staticmethod
    def get_groups_editor_or_master_with_id(id_usuario):
        return  (session.query(Grupo.IDGrupo, Grupo.Nombre).join(UsuarioGrupo, UsuarioGrupo.
                                                                 IDGrupo == Grupo.IDGrupo).
                                    filter(UsuarioGrupo.IDUsuario == id_usuario, or_(
                                    UsuarioGrupo.rol == Rol.editor, UsuarioGrupo.rol == Rol.master)).all())

    @staticmethod
    def __get_all_groups():
        return session.query(Grupo.Nombre, Grupo.Descripcion, Grupo.IDMaster).all()

    @staticmethod
    def get_all_user_groups(id_usuario):
        return (session.query(Grupo.IDGrupo, Grupo.Nombre, Grupo.Descripcion, UsuarioGrupo.rol)
                .join(UsuarioGrupo, UsuarioGrupo.IDGrupo==Grupo.IDGrupo)
                .filter(UsuarioGrupo.IDUsuario==id_usuario).all())

    @staticmethod
    def get_rol_in_group(id_usuario, id_grupo) -> Rol:
        if not GroupServiceData.is_user_in_group(id_grupo=id_grupo, id_usuario=id_usuario):
            raise Exception("No existe el usuario en el grupo")
        return session.query(UsuarioGrupo.rol).filter_by(IDUsuario=id_usuario, IDGrupo=id_grupo).first()[0]


    @staticmethod
    def get_master_alias_of_group(id_grupo):
        return session.query(Usuario.Alias).join(UsuarioGrupo, UsuarioGrupo.IDUsuario == Usuario.IDUsuario).filter(
            UsuarioGrupo.IDGrupo == id_grupo, UsuarioGrupo.rol == Rol.master
        ).first()[0]

    @staticmethod
    def is_user_in_group(id_grupo, id_usuario):
        return True if session.query(1).filter(UsuarioGrupo.IDGrupo == id_grupo,
                                               UsuarioGrupo.IDUsuario==id_usuario).first() else False

    @staticmethod
    def add_members_in_group(id_grupo, nuevos_miembros: tuple[int] or int):
        try:
            relaciones = [UsuarioGrupo(IDGrupo=id_grupo, IDUsuario=id_miembro, rol=Rol.miembro)
                          for id_miembro in nuevos_miembros]
            session.add_all(relaciones)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise Exception("No se pudo guardar los datos.")

    @staticmethod
    def change_rol_of_member(id_grupo, id_miembro, new_rol: Rol):
        usuario_grupo = session.query(UsuarioGrupo).filter_by(IDGrupo=id_grupo, IDUsuario=id_miembro).first()
        usuario_grupo.rol = new_rol
        session.commit()

    @staticmethod
    def update_group(id_grupo, nombre: str=None, descripcion=None):
        grupo = session.query(Grupo).filter_by(IDGrupo=id_grupo).first()
        if nombre:
            grupo.Nombre = nombre
        if descripcion:
            grupo.Descripcion = descripcion
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise Exception('No se actualizaron los datos porque ya existe un grupo con el mismo nombre.')

    @staticmethod
    def delete_group_in_all_task_with_id_group(id_grupo):
        relaciones = session.query(UsuarioTarea).filter_by(IDGrupo=id_grupo).all()

        for relacion in relaciones:
            relacion.IDGrupo = None

        session.commit()

    @staticmethod
    def __delete_tareas_relacion(relaciones_tareas: list):
        for relacion in relaciones_tareas:
            session.delete(relacion)

    @staticmethod
    def __conserver_task(relaciones_tareas: list[UsuarioTarea]):
        for relacion in relaciones_tareas:
            relacion.Disponible = False

    @staticmethod
    def __delete_member_group(id_grupo, id_usuario, delete_all_task):
        relacion_grupo = session.query(UsuarioGrupo).filter_by(IDGrupo=id_grupo, IDUsuario=id_usuario).first()

        tareas_pasadas_actuales = (session.query(UsuarioTarea).join(Tarea, Tarea.IDTarea == UsuarioTarea.IDTarea)
                                 .filter(UsuarioTarea.IDGrupo == id_grupo, UsuarioTarea.IDUsuario == id_usuario,
                                Tarea.Fecha_programada <= date.today()).all())
        tareas_futuras = (session.query(UsuarioTarea).join(Tarea, Tarea.IDTarea == UsuarioTarea.IDTarea)
                                 .filter(UsuarioTarea.IDGrupo == id_grupo, UsuarioTarea.IDUsuario == id_usuario,
                                Tarea.Fecha_programada > date.today()).all())

        if tareas_futuras:
            GroupServiceData.__delete_tareas_relacion(tareas_futuras)

        if tareas_pasadas_actuales:
            if delete_all_task:
                GroupServiceData.__delete_tareas_relacion(tareas_pasadas_actuales)
            else:
                GroupServiceData.__conserver_task(tareas_pasadas_actuales)

        session.delete(relacion_grupo)
        session.commit()

    @staticmethod
    def get_cant_members_group(id_grupo):
        return len(session.query(1).filter(UsuarioGrupo.IDGrupo==id_grupo).all())

    @staticmethod
    def out_member_group_session_manager(id_grupo, new_master: int = None, delete_all_task=False):
        id_usuario = SessionManager.get_id_user()
        if GroupServiceData.get_rol_in_group(id_usuario=id_usuario, id_grupo=id_grupo) == Rol.master:
            if not new_master and GroupServiceData.get_cant_members_group(id_grupo) > 1:
                raise Exception(ExceptionGroup,
                                "Como master:\nNo se puede salir del grupo sin antes elegir un nuevo master.")
            if new_master:
                usuario_master = session.query(UsuarioGrupo).filter_by(IDGrupo=id_grupo, IDUsuario=new_master).first()
                usuario_master.rol = Rol.master
                session.commit()
        GroupServiceData.__delete_member_group(id_grupo=id_grupo, id_usuario=id_usuario,
                                               delete_all_task=delete_all_task)

    @staticmethod
    def expel_member_group(id_grupo, id_usuario, delete_registers:bool=False):
        if GroupServiceData.get_rol_in_group(id_usuario=SessionManager.get_id_user(), id_grupo=id_grupo) != Rol.master:
            raise Exception("No se tienen permisos para eliminar miembros de este grupo.")

        if not GroupServiceData.is_user_in_group(id_grupo=id_grupo, id_usuario=id_usuario):
            raise Exception("El usuario a eliminar no está en el grupo.")

        GroupServiceData.__delete_member_group(id_grupo=id_grupo,id_usuario=id_usuario, delete_all_task=delete_registers)

    @staticmethod
    def __delete_group(id_grupo):
        relaciones = session.query(UsuarioGrupo).filter_by(IDGrupo=id_grupo).all()
        grupo = session.query(Grupo).filter_by(IDGrupo=id_grupo).first()

        for relacion in relaciones:
            session.delete(relacion)

        GroupServiceData.delete_group_in_all_task_with_id_group(id_grupo)

        session.delete(grupo)
        session.commit()



if __name__ == '__main__':
    pass
