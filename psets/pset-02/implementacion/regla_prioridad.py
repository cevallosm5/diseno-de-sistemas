from abc import ABC, abstractmethod
from configuracion import Configuracion


class ReglaPrioridad(ABC):

    @abstractmethod
    def tiene_prioridad(self, fecha_hora):
        pass


class SinPrioridad(ReglaPrioridad):

    def tiene_prioridad(self, fecha_hora):
        return False


class PrioridadAntes18(ReglaPrioridad):

    def tiene_prioridad(self, fecha_hora):
        config = Configuracion.obtener_objeto()
        return fecha_hora.hour < config.hora_limite_prioridad
