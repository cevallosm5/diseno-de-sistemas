from regla_prioridad import SinPrioridad, PrioridadAntes18
from reserva import Reserva


class Estudiante:

    def __init__(self, id_estudiante, nombre):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.regla_prioridad = SinPrioridad()

    def puede_reservar(self, hora_reserva):
        return self.regla_prioridad.permite_reservar(hora_reserva)

    def solicitar_reserva(self, cancha, fecha_hora_inicio):

        if not cancha.esta_disponible(fecha_hora_inicio):
            return None

        if not self.puede_reservar(fecha_hora_inicio):
            return None

        reserva = Reserva(self, cancha, fecha_hora_inicio)

        cancha.agregar_reserva(reserva)

        return reserva

    def cancelar_reserva(self, reserva, fecha_hora_actual):
        return reserva.cancelar(fecha_hora_actual)


class Capitan(Estudiante):

    def __init__(self, id_estudiante, nombre, equipo):
        super().__init__(id_estudiante, nombre)
        self.equipo = equipo
        self.regla_prioridad = PrioridadAntes18()