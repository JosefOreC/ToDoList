"""


"""


from src.modelo.entities.modelo import Grupo, UsuarioGrupo, Rol
from src.modelo.database_management.base.declarative_base import session
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
        response = session.query(UsuarioGrupo.IDUsuario, UsuarioGrupo.rol).filter(UsuarioGrupo.IDGrupo == id_grupo).all()
        return [[member[0], member[1]] for member in response]
    @staticmethod
    def get_all_members_without_master(id_grupo) -> list[int]:
        response = session.query(UsuarioGrupo.IDUsuario).where(UsuarioGrupo.rol != Rol.master).filter(UsuarioGrupo.IDGrupo==id_grupo).all()
        return [member[0] for member in response]

    @staticmethod
    def get_groups_editor_or_master(id_usuario):
        response = (session.query(Grupo.Nombre).join(UsuarioGrupo, UsuarioGrupo.
                                          IDGrupo==Grupo.IDGrupo).
                                          filter(UsuarioGrupo.IDUsuario==id_usuario,
                                          UsuarioGrupo.rol == Rol.editor or UsuarioGrupo.rol == Rol.master).all())
        return [grupo[0] for grupo in response]


if __name__ == '__main__':
    pass