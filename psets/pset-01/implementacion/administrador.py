class Administrador:

    def __init__(self, id_administrador, nombre):
        self.id_administrador = id_administrador
        self.nombre = nombre

    def bloquear_cancha(self, cancha, fecha_hora):
        cancha.bloquear_horario(fecha_hora)

    def habilitar_cancha(self, cancha, fecha_hora):
        cancha.habilitar_horario(fecha_hora)

    def resolver_conflicto(self, reservas, resolucion):
        return {
            "reservas": reservas,
            "resolucion": resolucion
        }