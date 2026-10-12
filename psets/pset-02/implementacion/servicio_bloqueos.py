from datetime import datetime, time

from estrategia_cancelacion import AnulacionAdministrativa


class ServicioBloqueos:

    def aplicar_bloqueo(self, bloqueo, campus=None):

        cancha = bloqueo.cancha

        # Validar información del bloqueo
        if cancha is None or bloqueo.fecha is None:
            raise ValueError(
                "El bloqueo debe tener una cancha y una fecha"
            )

        # Construir intervalo
        inicio = datetime.combine(
            bloqueo.fecha,
            time(hour=bloqueo.hora_inicio)
        )

        fin = datetime.combine(
            bloqueo.fecha,
            time(hour=bloqueo.hora_fin)
        )

        if inicio >= fin:
            raise ValueError(
                "La hora de inicio debe ser anterior a la hora de fin"
            )

        reservas_anuladas = []

        # Proteger la operación completa
        with cancha.lock:

            # Identificar reservas dentro del intervalo
            for reserva in cancha.reservas:

                if (
                    inicio <= reserva.fecha_hora_inicio < fin
                    and reserva.estado == "CONFIRMADA"
                ):

                    # Aplicar Strategy de anulación administrativa
                    estrategia_original = reserva.estrategia_cancelacion

                    reserva.establecer_estrategia(
                        AnulacionAdministrativa()
                    )

                    try:
                        reserva.cancelar(datetime.now())
                    finally:
                        reserva.establecer_estrategia(
                            estrategia_original
                        )

                    reservas_anuladas.append(reserva)

                    # Notificar mediante Abstract Factory
                    if campus is not None:
                        mensaje = (
                            f"Tu reserva del "
                            f"{reserva.fecha_hora_inicio} "
                            f"en {cancha.nombre} "
                            f"ha sido anulada por motivos administrativos."
                        )

                        campus.notificar(
                            reserva.estudiante.nombre,
                            mensaje
                        )

            # Bloquear el intervalo completo
            cancha.bloquear_intervalo(inicio, fin)

        return reservas_anuladas

    def aplicar_bloqueos_masivos(self, plantilla, asignaciones):

        resultados = []

        for cancha, fecha in asignaciones:

            # Clonar la plantilla mediante Prototype
            bloqueo = plantilla.clonar()

            # Personalizar cada clon
            bloqueo.cancha = cancha
            bloqueo.fecha = fecha

            # Aplicar el bloqueo
            reservas_anuladas = self.aplicar_bloqueo(bloqueo)

            resultados.append({
                "cancha": cancha.nombre,
                "fecha": fecha,
                "reservas_anuladas": len(reservas_anuladas)
            })

        return resultados