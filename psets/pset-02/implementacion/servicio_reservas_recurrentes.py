from datetime import datetime
from estudiante import Capitan
from fabrica_reservas import FabricaDeReservas
from estrategia_cancelacion import AnulacionAdministrativa


class ServicioReservasRecurrentes:

    def confirmar(self, solicitud, fecha_hora_actual=None):

        self.ultimo_conflicto = None

        if fecha_hora_actual is None:
            fecha_hora_actual = datetime.now()

        capitan = solicitud.capitan
        cancha = solicitud.cancha
        fechas = solicitud.obtener_fechas()

        if not isinstance(capitan, Capitan):
            raise ValueError("Solo un capitán puede reservar recurrentemente")

        if not 2 <= len(fechas) <= 8:
            raise ValueError("Se requieren entre 2 y 8 semanas")

        if capitan.esta_suspendido(fecha_hora_actual):
            return []

        with cancha.lock:

            reservas_a_desplazar = []

            # VALIDAR TODAS LAS SEMANAS ANTES DE MODIFICAR NADA
            for semana, fecha in enumerate(fechas, start=1):

                if fecha <= fecha_hora_actual:
                    self.ultimo_conflicto = {
                        "semana": semana,
                        "fecha": fecha,
                        "motivo": "La fecha ya pasó"
                    }
                    return []

                if fecha in cancha.horarios_bloqueados:
                    self.ultimo_conflicto = {
                        "semana": semana,
                        "fecha": fecha,
                        "motivo": "Horario bloqueado"
                    }
                    return []

                for inicio, fin in cancha.intervalos_bloqueados:
                    if inicio <= fecha < fin:
                        self.ultimo_conflicto = {
                            "semana": semana,
                            "fecha": fecha,
                            "motivo": "Bloqueo administrativo"
                        }
                        return []

                for reserva in cancha.reservas:

                    if (
                        reserva.fecha_hora_inicio == fecha
                        and reserva.estado == "CONFIRMADA"
                    ):

                        if not capitan.tiene_prioridad(fecha):
                            self.ultimo_conflicto = {
                                "semana": semana,
                                "fecha": fecha,
                                "motivo": "Fuera del horario de prioridad"
                            }
                            return []

                        if reserva.estudiante.tiene_prioridad(fecha):
                            self.ultimo_conflicto = {
                                "semana": semana,
                                "fecha": fecha,
                                "motivo": "Horario ocupado por otro capitán"
                            }
                            return []

                        reservas_a_desplazar.append(reserva)

            # CREAR TODAS LAS RESERVAS
            creador = FabricaDeReservas.elegir_creador(capitan)

            nuevas_reservas = [
                creador.crear_reserva(capitan, cancha, fecha)
                for fecha in fechas
            ]

            # CONFIRMAR EL CAMBIO
            reservas_agregadas = []
            estados_originales = []

            try:
                for reserva in nuevas_reservas:
                    cancha.agregar_reserva(reserva)
                    reservas_agregadas.append(reserva)

                for reserva in reservas_a_desplazar:
                    estados_originales.append(
                        (reserva, reserva.estado, reserva.estrategia_cancelacion)
                    )
                    reserva.establecer_estrategia(AnulacionAdministrativa())
                    try:
                        reserva.cancelar(fecha_hora_actual)
                    finally:
                        reserva.establecer_estrategia(
                            estados_originales[-1][2]
                        )

            except Exception:
                for reserva in reservas_agregadas:
                    if reserva in cancha.reservas:
                        cancha.reservas.remove(reserva)

                for reserva, estado, estrategia in estados_originales:
                    reserva.estado = estado
                    reserva.establecer_estrategia(estrategia)

                raise

            return nuevas_reservas
