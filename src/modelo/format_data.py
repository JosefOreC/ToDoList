
from datetime import datetime, date
class DataFormat:
    @staticmethod
    def convertir_fecha(fecha: str):
        if isinstance(fecha, str):
            return datetime.strptime(fecha, "%d-%m-%Y").date()
        elif isinstance(fecha, datetime):
            return fecha.date()
        elif isinstance(fecha, date):
            return fecha
        else:
            raise ValueError("Formato de fecha no soportado")