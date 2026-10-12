from datetime import timedelta

from regla_prioridad import SinPrioridad, PrioridadAntes18
from configuracion import Configuracion


class Estudiante:

    def __init__(self, id_estudiante, nombre):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.regla_prioridad = SinPrioridad()

        # Registro de penalizaciones
        self.no_shows = []
        self.suspendido_hasta = None

    def tiene_prioridad(self, fecha_hora):
        return self.regla_prioridad.tiene_prioridad(fecha_hora)

    def solicitar_reserva(self, cancha, fecha_hora_inicio, fecha_hora_actual=None):
        from datetime import datetime
        from fabrica_reservas import FabricaDeReservas
        from estrategia_cancelacion import AnulacionAdministrativa

        if fecha_hora_actual is None:
            fecha_hora_actual = datetime.now()

        # No permitir reservas durante una suspensión
        if self.esta_suspendido(fecha_hora_actual):
            return None

        # No permitir reservas en el pasado
        if fecha_hora_inicio <= fecha_hora_actual:
            return None

        with cancha.lock:

            # Verificar bloqueos administrativos antes de modificar reservas
            if fecha_hora_inicio in cancha.horarios_bloqueados:
                return None

            for inicio, fin in cancha.intervalos_bloqueados:
                if inicio <= fecha_hora_inicio < fin:
                    return None

            # Identificar una reserva confirmada en el horario solicitado
            reserva_existente = None

            for reserva in cancha.reservas:
                if (
                    reserva.fecha_hora_inicio == fecha_hora_inicio
                    and reserva.estado == "CONFIRMADA"
                ):
                    reserva_existente = reserva
                    break

            # Si existe una reserva, evaluar si puede ser desplazada
            if reserva_existente is not None:

                if not self.tiene_prioridad(fecha_hora_inicio):
                    return None

                if reserva_existente.estudiante.tiene_prioridad(fecha_hora_inicio):
                    return None

            # Crear primero la reserva mediante Factory Method
            creador = FabricaDeReservas.elegir_creador(self)

            nueva_reserva = creador.crear_reserva(
                self,
                cancha,
                fecha_hora_inicio
            )

            # Si no hay desplazamiento, verificar disponibilidad
            if reserva_existente is None:
                if not cancha.esta_disponible(fecha_hora_inicio):
                    return None

            # Desplazar la reserva anterior sin penalización
            if reserva_existente is not None:
                estrategia_original = reserva_existente.estrategia_cancelacion

                reserva_existente.establecer_estrategia(
                    AnulacionAdministrativa()
                )

                try:
                    reserva_existente.cancelar(fecha_hora_actual)
                finally:
                    reserva_existente.establecer_estrategia(
                        estrategia_original
                    )

            cancha.agregar_reserva(nueva_reserva)

            return nueva_reserva

    def cancelar_reserva(self, reserva, fecha_hora_actual):
        return reserva.cancelar(fecha_hora_actual)

    def registrar_no_show(self, fecha_hora):
        config = Configuracion.obtener_objeto()

        # Registrar la penalización
        self.no_shows.append(fecha_hora)

        # Contar NO_SHOW del mismo mes calendario
        no_shows_mes = [
            fecha for fecha in self.no_shows
            if fecha.year == fecha_hora.year
            and fecha.month == fecha_hora.month
        ]

        # Aplicar suspensión al alcanzar el límite
        if len(no_shows_mes) >= config.limite_no_shows:
            nueva_suspension = fecha_hora + timedelta(
                days=config.dias_suspension
            )

            if (
                self.suspendido_hasta is None
                or nueva_suspension > self.suspendido_hasta
            ):
                self.suspendido_hasta = nueva_suspension

    def esta_suspendido(self, fecha_hora):
        if self.suspendido_hasta is None:
            return False

        return fecha_hora < self.suspendido_hasta


class Capitan(Estudiante):

    def __init__(self, id_estudiante, nombre, equipo):
        super().__init__(id_estudiante, nombre)
        self.equipo = equipo
        self.regla_prioridad = PrioridadAntes18()