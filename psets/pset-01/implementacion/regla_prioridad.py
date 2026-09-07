# Regla de prioridad para reservas

class ReglaPrioridad:

    def permite_reservar(self, hora_reserva):
        raise NotImplementedError


class SinPrioridad(ReglaPrioridad):

    def permite_reservar(self, hora_reserva):
        return hora_reserva.hour >= 18


class PrioridadAntes18(ReglaPrioridad):

    def permite_reservar(self, hora_reserva):
        return True