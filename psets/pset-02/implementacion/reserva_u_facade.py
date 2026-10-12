from datetime import datetime

from servicio_reservas_recurrentes import ServicioReservasRecurrentes
from servicio_bloqueos import ServicioBloqueos


class ReservaUFacade:

    def __init__(self, campus):
        self.campus = campus
        self.servicio_recurrentes = ServicioReservasRecurrentes()
        self.servicio_bloqueos = ServicioBloqueos()

    def _notificar_desplazamientos(self, anteriores, cancha):
        for reserva in anteriores:
            if reserva.estado == "ANULADA":
                self.campus.notificar(
                    reserva.estudiante.nombre,
                    f"Tu reserva del {reserva.fecha_hora_inicio} "
                    f"en {cancha.nombre} fue anulada por prioridad "
                    "de un capitán, sin penalización."
                )

    def reservar(self, estudiante, cancha, fecha_hora, fecha_hora_actual=None):
        if fecha_hora_actual is None:
            fecha_hora_actual = datetime.now()

        if not self.campus.validar_reserva(fecha_hora):
            return None

        with cancha.lock:
            anteriores = [
                reserva for reserva in cancha.reservas
                if reserva.fecha_hora_inicio == fecha_hora
                and reserva.estado == "CONFIRMADA"
            ]

            reserva = estudiante.solicitar_reserva(
                cancha, fecha_hora, fecha_hora_actual
            )

            if reserva is not None:
                self.campus.notificar(
                    estudiante.nombre,
                    f"Reserva confirmada para {fecha_hora} "
                    f"en {cancha.nombre}"
                )
                self._notificar_desplazamientos(anteriores, cancha)

        return reserva

    @property
    def ultimo_conflicto_recurrente(self):
        return self.servicio_recurrentes.ultimo_conflicto

    def reservar_recurrentemente(self, solicitud, fecha_hora_actual=None):
        fechas = solicitud.obtener_fechas()

        if not all(self.campus.validar_reserva(fecha) for fecha in fechas):
            return []

        cancha = solicitud.cancha

        with cancha.lock:
            anteriores = [
                reserva for reserva in cancha.reservas
                if reserva.fecha_hora_inicio in fechas
                and reserva.estado == "CONFIRMADA"
            ]

            reservas = self.servicio_recurrentes.confirmar(
                solicitud, fecha_hora_actual
            )

            if reservas:
                self.campus.notificar(
                    solicitud.capitan.nombre,
                    f"Se confirmaron {len(reservas)} reservas "
                    f"recurrentes en {cancha.nombre}."
                )
                self._notificar_desplazamientos(anteriores, cancha)

        return reservas

    def cancelar(self, estudiante, reserva, fecha_hora_actual=None):
        if fecha_hora_actual is None:
            fecha_hora_actual = datetime.now()

        if reserva.estudiante is not estudiante:
            raise ValueError("No puedes cancelar una reserva ajena")

        return estudiante.cancelar_reserva(reserva, fecha_hora_actual)

    def bloquear(self, bloqueo):
        return self.servicio_bloqueos.aplicar_bloqueo(
            bloqueo, campus=self.campus
        )

    def bloquear_masivamente(self, plantilla, asignaciones):
        resultados = []

        for cancha, fecha in asignaciones:
            bloqueo = plantilla.clonar()
            bloqueo.cancha = cancha
            bloqueo.fecha = fecha

            anuladas = self.bloquear(bloqueo)

            resultados.append({
                "cancha": cancha.nombre,
                "fecha": fecha,
                "reservas_anuladas": len(anuladas)
            })

        return resultados
