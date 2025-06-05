"""


"""
from types import NoneType

from src.modelo.entities.modelo import Grupo, UsuarioGrupo, Rol, Usuario, UsuarioTarea
from src.modelo.database_management.base.declarative_base import session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError



class GroupServiceData:
    @staticmethod
    def insert_group(grupo: Grupo,relation_list: list[UsuarioGrupo]):
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
    def get_data_task_group_name(id_grupo):
        if id_grupo:
            return session.query(Grupo.Nombre).filter(Grupo.IDGrupo==id_grupo).first()[0]
        else:
            return None

    @staticmethod
    def get_all_members(id_grupo) -> list[int]:
        response = session.query(UsuarioGrupo.IDUsuario).filter(UsuarioGrupo.IDGrupo==id_grupo).all()
        return [member[0] for member in response]

    @staticmethod
    def get_all_members_with_rol(id_grupo):
        response = (session.query(Usuario.Alias, UsuarioGrupo.rol)
                    .join(Usuario, Usuario.IDUsuario == UsuarioGrupo.IDUsuario)
                    .filter(UsuarioGrupo.IDGrupo == id_grupo, Usuario.Estado==True).all())
        return [[member[0], member[1]] for member in response]

    @staticmethod
    def get_all_members_without_master(id_grupo) -> list[int]:
        response = session.query(UsuarioGrupo.IDUsuario).join(Usuario, Usuario.IDUsuario==UsuarioGrupo.IDUsuario).filter(
            UsuarioGrupo.IDGrupo==id_grupo, UsuarioGrupo.rol != Rol.master, Usuario.Estado==True).all()
        return [member[0] for member in response]

    @staticmethod
    def get_groups_editor_or_master(id_usuario):
        response = (session.query(Grupo.Nombre).join(UsuarioGrupo, UsuarioGrupo.
                                          IDGrupo==Grupo.IDGrupo).
                                          filter(UsuarioGrupo.IDUsuario==id_usuario,
                                          UsuarioGrupo.rol == Rol.editor or UsuarioGrupo.rol == Rol.master).all())
        return [grupo[0] for grupo in response]

    @staticmethod
    def get_groups_editor_or_master_with_id(id_usuario):
        return  (session.query(Grupo.IDGrupo, Grupo.Nombre).join(UsuarioGrupo, UsuarioGrupo.
                                                                 IDGrupo == Grupo.IDGrupo).
                                    filter(UsuarioGrupo.IDUsuario == id_usuario, or_(
                                    UsuarioGrupo.rol == Rol.editor, UsuarioGrupo.rol == Rol.master)).all())

    @staticmethod
    def get_rol_in_group(id_usuario, id_grupo):
        try:
            return session.query(UsuarioGrupo.rol).filter_by(IDUsuario=id_usuario, IDGrupo=id_grupo).first()[0]
        except NoneType:
            return None

    @staticmethod
    def get_master_alias_of_group(id_grupo):
        return session.query(Usuario.Alias).join(UsuarioGrupo, UsuarioGrupo.IDUsuario == Usuario.IDUsuario).filter(
            UsuarioGrupo.IDGrupo == id_grupo
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
            raise Exception('No se pudo actualizar los datos')

    @staticmethod
    def delete_group_in_all_task_with_id_group(id_grupo):
        relaciones = session.query(UsuarioTarea).filter_by(IDGrupo=id_grupo).all()

        for relacion in relaciones:
            relacion.IDGrupo = None

        session.commit()

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