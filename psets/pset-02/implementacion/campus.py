class Campus:

    def __init__(self, nombre, fabrica):
        self.nombre = nombre
        self.validador = fabrica.crear_validador()
        self.notificador = fabrica.crear_notificador()

    def validar_reserva(self, fecha_hora):
        return self.validador.validar_horario(fecha_hora)

    def notificar(self, destinatario, mensaje):
        self.notificador.enviar(destinatario, mensaje)
