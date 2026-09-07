class Cancha:

    def __init__(self, id_cancha, nombre):
        self.id_cancha = id_cancha
        self.nombre = nombre
        self.reservas = []
        self.horarios_bloqueados = []

    def esta_disponible(self, fecha_hora):

        if fecha_hora in self.horarios_bloqueados:
            return False

        for reserva in self.reservas:
            if reserva.fecha_hora_inicio == fecha_hora and reserva.estado == "CONFIRMADA":
                return False

        return True

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)

    def bloquear_horario(self, fecha_hora):
        self.horarios_bloqueados.append(fecha_hora)

    def habilitar_horario(self, fecha_hora):
        if fecha_hora in self.horarios_bloqueados:
            self.horarios_bloqueados.remove(fecha_hora)