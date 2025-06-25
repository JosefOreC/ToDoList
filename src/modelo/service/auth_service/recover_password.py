"""
    Encargado de recuperar los datos basicos para la recuperación de contraseña, validar los datos del usuario,
    cambiar contraseña
"""

import bcrypt
from src.modelo.service.user_service.user_service_data import UserServiceData
from src.modelo.service.data_service.data_format import DataFormat

class RecoverPassword:

    def __init__(self, alias):
        self.alias = alias
        self.data_basic = self.recover_basic_data_user()

    def recover_basic_data_user(self):
        basic_data_out_format = UserServiceData.recover_basic_data_user(self.alias)
        return DataFormat.convert_to_dict_basic_data_user(basic_data_out_format)

    def is_answer_correct(self, answer):
        return bcrypt.checkpw(answer.encode('utf-8'), self.data_basic.get('respuesta').encode('utf-8'))

    def change_password(self, password):
        UserServiceData.update_user(self.alias, password=password)
