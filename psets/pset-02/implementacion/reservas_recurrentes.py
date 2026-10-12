from datetime import timedelta

# Producto
class SolicitudReservaRecurrente:

    def __init__(self):
        self.capitan = None
        self.cancha = None
        self.fecha_inicio = None
        self.semanas = None
        self.equipamiento = []
        self.observaciones = ""

    def obtener_fechas(self):
        return [
            self.fecha_inicio + timedelta(weeks=i)
            for i in range(self.semanas)
        ]

# Builder
class SolicitudReservaBuilder:

    def __init__(self):
        self.solicitud = SolicitudReservaRecurrente()

    def add_capitan(self, capitan):
        self.solicitud.capitan = capitan
        return self

    def add_cancha(self, cancha):
        self.solicitud.cancha = cancha
        return self

    def add_fecha_inicio(self, fecha):
        self.solicitud.fecha_inicio = fecha
        return self

    def add_semanas(self, semanas):
        self.solicitud.semanas = semanas
        return self

    def add_equipamiento(self, equipamiento):
        self.solicitud.equipamiento = list(equipamiento)
        return self

    def add_observaciones(self, observaciones):
        self.solicitud.observaciones = observaciones
        return self

    def build(self):
        if self.solicitud.capitan is None:
            raise ValueError("Debe especificar un capitán")

        if self.solicitud.cancha is None:
            raise ValueError("Debe especificar una cancha")

        if self.solicitud.fecha_inicio is None:
            raise ValueError("Debe especificar una fecha de inicio")

        if self.solicitud.semanas is None or not 2 <= self.solicitud.semanas <= 8:
            raise ValueError("La solicitud debe tener entre 2 y 8 semanas")

        resultado = self.solicitud
        self.solicitud = SolicitudReservaRecurrente()

        return resultado
