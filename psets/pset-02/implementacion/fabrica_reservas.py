from reserva import Reserva
from estudiante import Capitan
from estrategia_cancelacion import (
    CancelacionEstudiante,
    CancelacionCapitan
)


# Productos
class ReservaRegular(Reserva):
    tipo = "REGULAR"


class ReservaPrioritaria(Reserva):
    tipo = "PRIORITARIA"


# Creador base
class CreadorDeReserva:

    def crear_reserva(self, estudiante, cancha, fecha_hora_inicio):
        raise NotImplementedError


# Creadores concretos
class CreadorReservaRegular(CreadorDeReserva):

    def crear_reserva(self, estudiante, cancha, fecha_hora_inicio):
        reserva = ReservaRegular(estudiante, cancha, fecha_hora_inicio)

        reserva.establecer_estrategia(CancelacionEstudiante())

        return reserva


class CreadorReservaPrioritaria(CreadorDeReserva):

    def crear_reserva(self, estudiante, cancha, fecha_hora_inicio):
        reserva = ReservaPrioritaria(estudiante, cancha, fecha_hora_inicio)

        reserva.establecer_estrategia(CancelacionCapitan())

        return reserva


# Selector de creadores
class FabricaDeReservas:

    @staticmethod
    def elegir_creador(estudiante):
        if isinstance(estudiante, Capitan):
            return CreadorReservaPrioritaria()

        return CreadorReservaRegular()
