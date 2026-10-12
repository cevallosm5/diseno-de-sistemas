# Singleton: configuracion compartida de ReservaU.

class Configuracion:
    _objeto = None

    def __init__(self):
        self.hora_limite_prioridad = 18
        self.horas_cancelacion_estudiante = 2
        self.horas_cancelacion_capitan = 24
        self.limite_no_shows = 3
        self.dias_suspension = 7
        Configuracion._objeto = self

    @staticmethod
    def obtener_objeto():
        if Configuracion._objeto is None:
            Configuracion()
        return Configuracion._objeto