"""
    Controlador encargado de recuperar contraseñas
"""

from src.modelo.service.auth_service.recover_password import RecoverPassword
from src.modelo.service.user_service.user_service_data import UserServiceData


class RecoverPasswordController:
    """
        Clase con los metodos necesarios para la comunicación con el objeto de recuperar contraseña
    """

    __recuperacion: RecoverPassword = None

    @staticmethod
    def start_recover_password(alias)->dict['success':bool, 'response':str,
                                       'data':dict['alias', 'respuesta', 'pregunta']]:
        try:
            RecoverPasswordController.__recuperacion = RecoverPassword(alias)
        except Exception as E:
            return {
                'success': False,
                'response': f"No se pudieron recuperar los datos de recuperación:\n{E}",
                'data':{
                    None
                }
            }

        return {
            'success': True,
            'response': f"Se recuperaron los datos.",
            'data': RecoverPasswordController.__recuperacion.data_basic
        }

    @staticmethod
    def is_response_correct(answer: str):
        try:
            is_correct_answer = RecoverPasswordController.__recuperacion.is_answer_correct(answer)
            success = True
            response = "Se validó la recuperación de contraseña."
        except Exception as E:
            is_correct_answer = False
            success = False,
            response = ("No se pudo recuperar los datos. \nProceso de recuperación no completado.\nIntentelo de nuevo."
                        f"\n{E}")

        return {
            'success': success,
            'response': response,
            'data':{
                'success': is_correct_answer,
                'result': "Respuesta correcta." if is_correct_answer else "Respuesta incorrecta."
            }
        }

    @staticmethod
    def change_password(new_password, confirm_password):
        if not new_password or not confirm_password:
            return {
                'success': False,
                'response': "No se pueden dejar campos vacios."
            }



        try:
            UserServiceData.update_user(usuario=RecoverPasswordController.__recuperacion.alias, password=new_password)
            success = True
            response = "Se cambió la contraseña."
        except Exception as E:
            success = False,
            response = f"No se pudo cambiar la contraseña.\n{E}"
        finally:
            RecoverPasswordController.__recuperacion = None

        return {
            'success':success,
            'response':response
        }



