
from datetime import datetime
class DataFormat:
    @staticmethod
    def convertir_fecha(fecha: str):
        return datetime.strptime(fecha, "%d-%m-%Y")