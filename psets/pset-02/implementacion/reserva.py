class Reserva:

    def __init__(self, estudiante, cancha, fecha_hora_inicio):
        self.estudiante = estudiante
        self.cancha = cancha
        self.fecha_hora_inicio = fecha_hora_inicio
        self.estado = "CONFIRMADA"
        self.estrategia_cancelacion = None

    def establecer_estrategia(self, estrategia):
        self.estrategia_cancelacion = estrategia

    def cancelar(self, fecha_hora_actual):
        if self.estado != "CONFIRMADA":
            raise ValueError("Solo se pueden cancelar reservas confirmadas")

        if self.estrategia_cancelacion is None:
            raise ValueError("No se ha establecido una estrategia de cancelacion")

        self.estado = self.estrategia_cancelacion.evaluar(
            self, fecha_hora_actual
        )

        # Registrar penalización cuando corresponda
        if self.estado == "NO_SHOW":
            self.estudiante.registrar_no_show(fecha_hora_actual)

        return self.estado