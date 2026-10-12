from abc import ABC, abstractmethod
from datetime import timedelta

from configuracion import Configuracion


# Estrategia abstracta
class EstrategiaCancelacion(ABC):

    @abstractmethod
    def evaluar(self, reserva, fecha_hora_actual):
        pass


# Estrategia concreta: estudiante
class CancelacionEstudiante(EstrategiaCancelacion):

    def evaluar(self, reserva, fecha_hora_actual):
        config = Configuracion.obtener_objeto()

        tiempo_restante = reserva.fecha_hora_inicio - fecha_hora_actual

        if tiempo_restante < timedelta(hours=config.horas_cancelacion_estudiante):
            return "NO_SHOW"

        return "CANCELADA"


# Estrategia concreta: capitan
class CancelacionCapitan(EstrategiaCancelacion):

    def evaluar(self, reserva, fecha_hora_actual):
        config = Configuracion.obtener_objeto()

        tiempo_restante = reserva.fecha_hora_inicio - fecha_hora_actual

        if tiempo_restante < timedelta(hours=config.horas_cancelacion_capitan):
            return "NO_SHOW"

        return "CANCELADA"


# Estrategia concreta: administrador
class AnulacionAdministrativa(EstrategiaCancelacion):

    def evaluar(self, reserva, fecha_hora_actual):
        return "ANULADA"
