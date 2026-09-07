from datetime import timedelta


class Reserva:

    def __init__(self, estudiante, cancha, fecha_hora_inicio):
        self.estudiante = estudiante
        self.cancha = cancha
        self.fecha_hora_inicio = fecha_hora_inicio
        self.estado = "CONFIRMADA"

    def cancelar(self, fecha_hora_actual):
        tiempo_restante = self.fecha_hora_inicio - fecha_hora_actual

        if tiempo_restante < timedelta(hours=2):
            self.estado = "NO_SHOW"
        else:
            self.estado = "CANCELADA"

        return self.estado