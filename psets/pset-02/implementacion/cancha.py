from threading import RLock


class Cancha:

    def __init__(self, id_cancha, nombre):
        self.id_cancha = id_cancha
        self.nombre = nombre
        self.reservas = []
        self.horarios_bloqueados = []
        self.intervalos_bloqueados = []
        self.lock = RLock()

    def esta_disponible(self, fecha_hora):

        # Verificar bloqueos individuales
        if fecha_hora in self.horarios_bloqueados:
            return False

        # Verificar intervalos de bloqueo
        for inicio, fin in self.intervalos_bloqueados:
            if inicio <= fecha_hora < fin:
                return False

        # Verificar reservas confirmadas
        for reserva in self.reservas:
            if (
                reserva.fecha_hora_inicio == fecha_hora
                and reserva.estado == "CONFIRMADA"
            ):
                return False

        return True

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)

    def bloquear_horario(self, fecha_hora):
        if fecha_hora not in self.horarios_bloqueados:
            self.horarios_bloqueados.append(fecha_hora)

    def habilitar_horario(self, fecha_hora):
        if fecha_hora in self.horarios_bloqueados:
            self.horarios_bloqueados.remove(fecha_hora)

    def bloquear_intervalo(self, inicio, fin):
        if inicio >= fin:
            raise ValueError(
                "La hora de inicio debe ser anterior a la hora de fin"
            )

        self.intervalos_bloqueados.append((inicio, fin))