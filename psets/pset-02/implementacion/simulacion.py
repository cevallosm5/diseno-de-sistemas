from datetime import datetime, date, timedelta
from threading import Thread, Barrier

from estudiante import Estudiante, Capitan
from equipo import EquipoOficial
from cancha import Cancha
from campus import Campus
from abs_fabrica_campus import FabricaNorte, FabricaSur
from reserva_u_facade import ReservaUFacade
from reservas_recurrentes import SolicitudReservaBuilder
from plantilla_bloqueo import PlantillaBloqueo


AHORA = datetime(2026, 11, 1, 12)

norte = ReservaUFacade(Campus("Campus Norte", FabricaNorte()))
sur = ReservaUFacade(Campus("Campus Sur", FabricaSur()))


def titulo(numero, nombre):
    print(f"\n{'=' * 55}")
    print(f"ESCENARIO {numero}: {nombre}")
    print("=" * 55)


def crear_capitan(numero, nombre):
    equipo = EquipoOficial(numero, f"Equipo {nombre}")
    return Capitan(numero, nombre, equipo)


# ============================================================
# ESCENARIO 1: RESERVAS EN AMBOS CAMPUS
# ============================================================

titulo(1, "Reservas en Campus Norte y Campus Sur")

juan = Estudiante(1, "Juan")
pedro = Estudiante(2, "Pedro")

cancha_norte = Cancha(1, "Cancha Norte")
cancha_sur = Cancha(2, "Cancha Sur")

fecha_norte = datetime(2026, 11, 10, 10)
fecha_sur = datetime(2026, 11, 10, 11)

print("1. Juan solicita una reserva en Campus Norte.")
reserva_norte = norte.reservar(
    juan, cancha_norte, fecha_norte, AHORA
)

assert reserva_norte is not None
print("2. Horario validado por Campus Norte.")

print("3. Estado:", reserva_norte.estado)

print("\n4. Pedro solicita una reserva en Campus Sur.")
reserva_sur = sur.reservar(
    pedro, cancha_sur, fecha_sur, AHORA
)

assert reserva_sur is not None
print("5. Horario validado por Campus Sur.")

print("6. Estado:", reserva_sur.estado)


# ============================================================
# ESCENARIO 2: HORARIO FUERA DE CAMPUS
# ============================================================

titulo(2, "Reserva fuera del horario permitido")

print("1. Juan solicita una reserva a las 23:00 en Campus Norte.")

rechazada = norte.reservar(
    juan,
    cancha_norte,
    datetime(2026, 11, 11, 23),
    AHORA
)

if rechazada is None:
    print("2. El sistema rechazó la reserva por horario no permitido.")
    print("3. VALIDACIÓN EXITOSA.")
else:
    raise AssertionError("ERROR: Se aceptó una reserva fuera del horario.")


# ============================================================
# ESCENARIO 3: RESERVAS RECURRENTES
# ============================================================

titulo(3, "Reserva recurrente exitosa y conflicto")

capitan = crear_capitan(3, "Carlos")
cancha_recurrente = Cancha(3, "Cancha Recurrente")

inicio = datetime(2026, 11, 10, 16)

print("1. Capitán construye una solicitud de cuatro semanas.")

solicitud = (
    SolicitudReservaBuilder()
    .add_capitan(capitan)
    .add_cancha(cancha_recurrente)
    .add_fecha_inicio(inicio)
    .add_semanas(4)
    .add_equipamiento(["Balones", "Chalecos"])
    .add_observaciones("Entrenamiento oficial")
    .build()
)

print("2. Sistema verifica cada semana.")
for numero, fecha in enumerate(solicitud.obtener_fechas(), 1):
    print(f"   Semana {numero}: {fecha}")

reservas = norte.reservar_recurrentemente(solicitud, AHORA)

assert len(reservas) == 4
print("3. Todas las semanas disponibles.")
print("4. Reservas confirmadas:", len(reservas))

print("\n5. Se construye una segunda solicitud.")

otra_cancha = Cancha(4, "Cancha con conflicto")
otro_capitan = crear_capitan(4, "Daniel")

inicio_conflicto = datetime(2026, 11, 11, 16)

# Otro capitán ya tiene reservada la tercera semana.
fecha_conflicto = inicio_conflicto + timedelta(weeks=2)

capitan_existente = crear_capitan(40, "Roberto")

reserva_existente = norte.reservar(
    capitan_existente,
    otra_cancha,
    fecha_conflicto,
    AHORA
)

assert reserva_existente is not None

solicitud_conflicto = (
    SolicitudReservaBuilder()
    .add_capitan(otro_capitan)
    .add_cancha(otra_cancha)
    .add_fecha_inicio(inicio_conflicto)
    .add_semanas(4)
    .build()
)

print("6. Sistema verifica las semanas.")
for numero, fecha in enumerate(solicitud_conflicto.obtener_fechas(), 1):
    print(f"   Semana {numero}: {fecha}")

resultado_conflicto = norte.reservar_recurrentemente(
    solicitud_conflicto, AHORA
)

assert resultado_conflicto == []

conflicto = norte.ultimo_conflicto_recurrente

assert conflicto is not None
assert conflicto["semana"] == 3
assert conflicto["fecha"] == fecha_conflicto

print(
    f"7. Conflicto detectado en semana {conflicto['semana']}: "
    f"{conflicto['fecha']}"
)
print("   Motivo:", conflicto["motivo"])
print("8. Ninguna reserva recurrente fue confirmada.")



# ============================================================
# PRUEBA ADICIONAL: Prioridad de capitán
# ============================================================

print("\n--- PRUEBA ADICIONAL: Prioridad de capitán ---")

cancha_prioridad = Cancha(90, "Cancha Prioridad")
estudiante_regular = Estudiante(90, "Estudiante Regular")
capitan_prioritario = Capitan(91, "Capitán Prioritario", "Equipo A")

fecha_prioridad = datetime(2026, 11, 26, 16, 0)

reserva_regular = norte.reservar(
    estudiante_regular,
    cancha_prioridad,
    fecha_prioridad,
    AHORA
)

assert reserva_regular is not None
assert reserva_regular.estado == "CONFIRMADA"

reserva_capitan = norte.reservar(
    capitan_prioritario,
    cancha_prioridad,
    fecha_prioridad,
    AHORA
)

assert reserva_capitan is not None
assert reserva_capitan.estado == "CONFIRMADA"
assert reserva_regular.estado == "ANULADA"
assert len(estudiante_regular.no_shows) == 0

print("Reserva original:", reserva_regular.estado)
print("Reserva del capitán:", reserva_capitan.estado)
print("Penalizaciones:", len(estudiante_regular.no_shows))
print("Desplazamiento por prioridad verificado.")

# ============================================================
# ESCENARIO 4: TRES POLÍTICAS DE CANCELACIÓN
# ============================================================

titulo(4, "Cancelaciones mediante Strategy")

print("1. Estudiante cancela con más de dos horas.")

estudiante_cancelacion = Estudiante(5, "Ana")
cancha_cancelacion = Cancha(5, "Cancha Cancelaciones")

fecha_estudiante = datetime(2026, 11, 12, 16)

reserva_estudiante = norte.reservar(
    estudiante_cancelacion,
    cancha_cancelacion,
    fecha_estudiante,
    AHORA
)

estado = norte.cancelar(
    estudiante_cancelacion,
    reserva_estudiante,
    datetime(2026, 11, 12, 12)
)

assert estado == "CANCELADA"
print("2. Resultado:", estado)

print("\n3. Capitán cancela con menos de 24 horas.")

capitan_cancelacion = crear_capitan(6, "Luis")
fecha_capitan = datetime(2026, 11, 13, 16)

reserva_capitan = norte.reservar(
    capitan_cancelacion,
    cancha_cancelacion,
    fecha_capitan,
    AHORA
)

estado = norte.cancelar(
    capitan_cancelacion,
    reserva_capitan,
    datetime(2026, 11, 13, 10)
)

assert estado == "NO_SHOW"
print("4. Resultado:", estado)

print("\n5. Administrador anula una reserva por mantenimiento.")

fecha_admin = datetime(2026, 11, 14, 10)

reserva_admin = norte.reservar(
    estudiante_cancelacion,
    cancha_cancelacion,
    fecha_admin,
    AHORA
)

plantilla_admin = PlantillaBloqueo(
    "Mantenimiento", 10, 12
)

bloqueo_admin = plantilla_admin.clonar()
bloqueo_admin.cancha = cancha_cancelacion
bloqueo_admin.fecha = date(2026, 11, 14)

anuladas = norte.bloquear(bloqueo_admin)

assert len(anuladas) == 1
assert reserva_admin.estado == "ANULADA"

print("6. Resultado:", reserva_admin.estado)
print("7. NO_SHOW de Ana:", len(estudiante_cancelacion.no_shows))


# ============================================================
# ESCENARIO 5: SUSPENSIÓN POR TRES NO-SHOWS
# ============================================================

titulo(5, "Tres no-shows y suspensión")

estudiante_suspension = Estudiante(7, "María")
cancha_suspension = Cancha(6, "Cancha Suspensión")

print("1. María realiza tres reservas.")

for numero, dia in enumerate([16, 17, 18], 1):

    fecha = datetime(2026, 11, dia, 16)

    reserva = norte.reservar(
        estudiante_suspension,
        cancha_suspension,
        fecha,
        AHORA
    )

    assert reserva is not None

    cancelacion = fecha - timedelta(hours=1)

    estado = norte.cancelar(
        estudiante_suspension,
        reserva,
        cancelacion
    )

    assert estado == "NO_SHOW"
    print(f"2.{numero} Cancelación {numero}: {estado}")

print("3. Total NO_SHOW:", len(estudiante_suspension.no_shows))
print("4. Suspendida hasta:", estudiante_suspension.suspendido_hasta)

assert estudiante_suspension.suspendido_hasta is not None

intento = norte.reservar(
    estudiante_suspension,
    cancha_suspension,
    datetime(2026, 11, 20, 16),
    datetime(2026, 11, 18, 16)
)

assert intento is None
print("5. Nueva reserva rechazada durante suspensión.")


# ============================================================
# ESCENARIO 6: PROTOTYPE Y BLOQUEOS MASIVOS
# ============================================================

titulo(6, "Bloqueo clonado en dos canchas")

cancha_a = Cancha(7, "Cancha A")
cancha_b = Cancha(8, "Cancha B")
afectado = Estudiante(8, "Sofía")

fecha_bloqueo = datetime(2026, 11, 21, 10)

print("1. Sofía reserva la Cancha A.")

reserva_afectada = norte.reservar(
    afectado, cancha_a, fecha_bloqueo, AHORA
)

assert reserva_afectada is not None

print("2. Administrador define una plantilla con equipamiento.")

plantilla = PlantillaBloqueo(
    "Torneo universitario",
    10,
    12,
    ["Red", "Marcador"]
)

print("3. Se comprueba la independencia de los clones.")

clon = plantilla.clonar()
clon.equipamiento.append("Balones")

assert plantilla.equipamiento == ["Red", "Marcador"]
assert clon.equipamiento == ["Red", "Marcador", "Balones"]

print("   Equipamiento original:", plantilla.equipamiento)
print("   Equipamiento del clon:", clon.equipamiento)
print("   Prototype: copia profunda verificada.")

print("4. Sistema clona el bloqueo para dos canchas.")

resultados = norte.bloquear_masivamente(
    plantilla,
    [
        (cancha_a, date(2026, 11, 21)),
        (cancha_b, date(2026, 11, 21))
    ]
)

assert reserva_afectada.estado == "ANULADA"
assert len(resultados) == 2
assert len(afectado.no_shows) == 0

print("4. Reserva de Sofía:", reserva_afectada.estado)
print("5. Bloqueos aplicados:", len(resultados))
print("6. Penalizaciones (NO-SHOW):", len(afectado.no_shows))


# ============================================================
# ESCENARIO 7: CONCURRENCIA
# ============================================================

titulo(7, "Dos hilos reservan simultáneamente")

cancha_concurrente = Cancha(9, "Cancha Concurrente")
estudiante_a = Estudiante(9, "Andrés")
estudiante_b = Estudiante(10, "Valentina")

fecha_concurrente = datetime(2026, 11, 22, 19)

barrera = Barrier(2)
resultados_hilos = []


def intentar_reservar(estudiante):
    barrera.wait()

    reserva = norte.reservar(
        estudiante,
        cancha_concurrente,
        fecha_concurrente,
        AHORA
    )

    resultados_hilos.append(
        (estudiante.nombre, reserva is not None)
    )


print("1. Se crean dos hilos.")

hilo1 = Thread(target=intentar_reservar, args=(estudiante_a,))
hilo2 = Thread(target=intentar_reservar, args=(estudiante_b,))

print("2. Ambos intentan reservar simultáneamente.")

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

for nombre, confirmado in resultados_hilos:
    print(f"3. {nombre}: {'CONFIRMADA' if confirmado else 'RECHAZADA'}")

confirmadas = [
    reserva for reserva in cancha_concurrente.reservas
    if reserva.estado == "CONFIRMADA"
]

assert len(confirmadas) == 1
assert sum(confirmado for _, confirmado in resultados_hilos) == 1

print("4. Total de reservas confirmadas:", len(confirmadas))
print("5. Concurrencia controlada correctamente.")

print("\n" + "=" * 55)
print("SIMULACIÓN PSET #2 COMPLETADA")
print("LOS SIETE ESCENARIOS PASARON")
print("=" * 55)
