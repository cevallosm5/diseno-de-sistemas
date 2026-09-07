from datetime import datetime

from estudiante import Estudiante, Capitan
from equipo import EquipoOficial
from cancha import Cancha
from administrador import Administrador


# ==========================================
# CREACIÓN DE OBJETOS
# ==========================================

# Equipos
equipo_1 = EquipoOficial(1, "Equipo Oficial A")

# Usuarios
estudiante_1 = Estudiante(1, "Martin")
estudiante_2 = Estudiante(2, "Juan")

capitan_1 = Capitan(
    3,
    "Carlos",
    equipo_1
)

administrador = Administrador(
    1,
    "Administrador ReservaU"
)

# Canchas
cancha_1 = Cancha(1, "Cancha Futbol")
cancha_2 = Cancha(2, "Cancha Tennis")
cancha_3 = Cancha(3, "Cancha Volley")
cancha_4 = Cancha(4, "Cancha Baile")
cancha_5 = Cancha(5, "Cancha Basket")
cancha_6 = Cancha(6, "Cancha Ping Pong")
cancha_7 = Cancha(7, "Cancha Playa")
cancha_8 = Cancha(8, "Cancha Esgrima")


# ==========================================
# CU-01: RESERVAR CANCHA
# ==========================================

print("\n=== CU-01: RESERVAR CANCHA ===")

hora_reserva = datetime(2026, 9, 10, 17, 0)

print("1. Estudiante solicita reservar una cancha.")
print("2. Sistema verifica disponibilidad.")

if cancha_1.esta_disponible(hora_reserva):

    print("3. La cancha está disponible.")
    print("4. Sistema verifica si la hora es antes de las 6:00 p.m.")

    reserva_cu01 = capitan_1.solicitar_reserva(
        cancha_1,
        hora_reserva
    )

    if reserva_cu01:

        print("5. El solicitante es capitán.")
        print("6. Se permite continuar con la reserva.")
        print("7. Sistema crea la reserva.")
        print("8. Sistema asocia la reserva con el estudiante y la cancha.")
        print("9. Sistema confirma la reserva.")

        print(
            f"Reserva confirmada para "
            f"{reserva_cu01.estudiante.nombre} "
            f"en {reserva_cu01.cancha.nombre}."
        )

    else:
        print("La reserva no fue permitida.")

else:
    print("3a. La cancha no está disponible.")
    print("3a.1 La reserva no puede realizarse.")


# ==========================================
# CU-01 ALTERNO:
# ESTUDIANTE SIN PRIORIDAD
# ==========================================

print("\n=== CU-01 ALTERNO: ESTUDIANTE SIN PRIORIDAD ===")

hora_temprana = datetime(2026, 9, 12, 17, 0)

print("1. Estudiante solicita reservar una cancha.")
print("2. Sistema verifica disponibilidad.")

if cancha_2.esta_disponible(hora_temprana):

    print("3. La cancha está disponible.")
    print("4. Sistema verifica si la hora es antes de las 6:00 p.m.")
    print("5. Sistema verifica si el solicitante es capitán.")

    reserva_sin_prioridad = estudiante_1.solicitar_reserva(
        cancha_2,
        hora_temprana
    )

    if reserva_sin_prioridad is None:
        print("5a. El solicitante no es capitán.")
        print("5a.1 La reserva no está permitida.")
    else:
        print("ERROR: la reserva debería haber sido rechazada.")

else:
    print("La cancha no está disponible.")


# ==========================================
# CU-01 ALTERNO:
# CANCHA NO DISPONIBLE
# ==========================================

print("\n=== CU-01 ALTERNO: CANCHA NO DISPONIBLE ===")

hora_ocupada = datetime(2026, 9, 13, 19, 0)

reserva_original = estudiante_1.solicitar_reserva(
    cancha_2,
    hora_ocupada
)

print("1. Se intenta reservar una cancha ya ocupada.")
print("2. Sistema verifica disponibilidad.")

reserva_duplicada = capitan_1.solicitar_reserva(
    cancha_2,
    hora_ocupada
)

if reserva_duplicada is None:
    print("3a. La cancha no está disponible.")
    print("3a.1 La reserva no puede realizarse.")
else:
    print("ERROR: se permitió una reserva duplicada.")


# ==========================================
# CU-02: CANCELAR RESERVA - NO SHOW
# ==========================================

print("\n=== CU-02: CANCELAR RESERVA - NO SHOW ===")

hora_cancelacion = datetime(2026, 9, 10, 16, 0)

print("1. Estudiante solicita cancelar su reserva.")
print("2. Sistema identifica la reserva.")
print("3. Sistema calcula cuánto tiempo falta para el inicio.")

estado_cu02 = capitan_1.cancelar_reserva(
    reserva_cu01,
    hora_cancelacion
)

print("4. Sistema determina si faltan menos de 2 horas.")

if estado_cu02 == "NO_SHOW":

    print("4a.1 Sistema registra la reserva como NO_SHOW.")
    print("4a.2 Sistema informa al estudiante que se registró como no-show.")

else:

    print("5. Sistema registra la reserva como CANCELADA.")
    print("6. Sistema confirma la cancelación.")

print(f"Estado final de la reserva: {estado_cu02}")


# ==========================================
# CU-02: CANCELACIÓN NORMAL
# ==========================================

print("\n=== CU-02: CANCELACIÓN NORMAL ===")

hora_reserva_normal = datetime(2026, 9, 14, 20, 0)

reserva_normal = estudiante_1.solicitar_reserva(
    cancha_3,
    hora_reserva_normal
)

hora_cancelacion_normal = datetime(2026, 9, 14, 16, 0)

print("1. Estudiante solicita cancelar su reserva.")
print("2. Sistema identifica la reserva.")
print("3. Sistema calcula cuánto tiempo falta para el inicio.")

estado_normal = estudiante_1.cancelar_reserva(
    reserva_normal,
    hora_cancelacion_normal
)

print("4. Sistema determina si faltan menos de 2 horas.")

if estado_normal == "CANCELADA":

    print("5. Sistema registra la reserva como CANCELADA.")
    print("6. Sistema confirma la cancelación.")

else:

    print("ERROR: debería haberse registrado como CANCELADA.")

print(f"Estado final de la reserva: {estado_normal}")


# ==========================================
# CU-03: GESTIONAR CANCHAS
# ==========================================

print("\n=== CU-03: GESTIONAR CANCHAS ===")

hora_bloqueo = datetime(2026, 9, 11, 15, 0)

print("1. Administrador solicita gestionar una cancha.")
print("2. Sistema identifica la cancha seleccionada.")
print("3. Administrador indica la disponibilidad para una fecha u hora.")

administrador.bloquear_cancha(
    cancha_1,
    hora_bloqueo
)

print("4. Sistema actualiza la disponibilidad de la cancha.")
print("5. Sistema confirma la actualización.")

if cancha_1.esta_disponible(hora_bloqueo):
    print("ERROR: la cancha debería estar bloqueada.")
else:
    print("La cancha quedó bloqueada correctamente.")


# ==========================================
# CU-04: RESOLVER CONFLICTO DE RESERVA
# ==========================================

print("\n=== CU-04: RESOLVER CONFLICTO DE RESERVA ===")

print("1. Administrador selecciona el conflicto de reserva.")
print("2. Sistema identifica las reservas involucradas.")

reservas_en_conflicto = [reserva_cu01]

print("3. Administrador indica la resolución del conflicto.")

resolucion = "Mantener la reserva existente."

resultado = administrador.resolver_conflicto(
    reservas_en_conflicto,
    resolucion
)

print("4. Sistema registra la resolución.")

print(
    f"Resolución registrada: "
    f"{resultado['resolucion']}"
)


# ==========================================
# PRUEBAS ADICIONALES
# ==========================================

print("\n\n=== PRUEBAS ADICIONALES ===")


# ==========================================
# PRUEBA 1:
# ESTUDIANTE A LAS 18:00
# ==========================================

print("\n--- Prueba 1: estudiante a las 18:00 ---")

hora_18 = datetime(2026, 9, 15, 18, 0)

reserva_18 = estudiante_1.solicitar_reserva(
    cancha_4,
    hora_18
)

if reserva_18:
    print("OK: estudiante puede reservar a las 18:00.")
else:
    print("ERROR: estudiante debería poder reservar a las 18:00.")


# ==========================================
# PRUEBA 2:
# CAPITÁN ANTES DE LAS 18:00
# ==========================================

print("\n--- Prueba 2: capitán antes de las 18:00 ---")

hora_capitan = datetime(2026, 9, 15, 17, 0)

reserva_capitan = capitan_1.solicitar_reserva(
    cancha_5,
    hora_capitan
)

if reserva_capitan:
    print("OK: capitán puede reservar antes de las 18:00.")
else:
    print("ERROR: capitán debería poder reservar antes de las 18:00.")


# ==========================================
# PRUEBA 3:
# ESTUDIANTE ANTES DE LAS 18:00
# ==========================================

print("\n--- Prueba 3: estudiante antes de las 18:00 ---")

hora_estudiante_temprana = datetime(2026, 9, 16, 17, 0)

reserva_temprana = estudiante_1.solicitar_reserva(
    cancha_6,
    hora_estudiante_temprana
)

if reserva_temprana is None:
    print("OK: estudiante no puede reservar antes de las 18:00.")
else:
    print("ERROR: estudiante no debería poder reservar antes de las 18:00.")


# ==========================================
# PRUEBA 4:
# CANCHA BLOQUEADA
# ==========================================

print("\n--- Prueba 4: cancha bloqueada ---")

hora_bloqueada = datetime(2026, 9, 16, 19, 0)

administrador.bloquear_cancha(
    cancha_7,
    hora_bloqueada
)

reserva_bloqueada = estudiante_1.solicitar_reserva(
    cancha_7,
    hora_bloqueada
)

if reserva_bloqueada is None:
    print("OK: no se puede reservar una cancha bloqueada.")
else:
    print("ERROR: se permitió reservar una cancha bloqueada.")


# ==========================================
# PRUEBA 5:
# HABILITAR CANCHA NUEVAMENTE
# ==========================================

print("\n--- Prueba 5: habilitar cancha ---")

administrador.habilitar_cancha(
    cancha_7,
    hora_bloqueada
)

reserva_habilitada = estudiante_1.solicitar_reserva(
    cancha_7,
    hora_bloqueada
)

if reserva_habilitada:
    print("OK: la cancha vuelve a estar disponible.")
else:
    print("ERROR: la cancha debería poder reservarse después de habilitarla.")


# ==========================================
# PRUEBA 6:
# CANCELACIÓN EXACTAMENTE 2 HORAS ANTES
# ==========================================

print("\n--- Prueba 6: cancelación exactamente 2 horas antes ---")

hora_inicio_2h = datetime(2026, 9, 17, 20, 0)

reserva_2h = estudiante_1.solicitar_reserva(
    cancha_6,
    hora_inicio_2h
)

hora_cancelacion_2h = datetime(2026, 9, 17, 18, 0)

estado_2h = estudiante_1.cancelar_reserva(
    reserva_2h,
    hora_cancelacion_2h
)

if estado_2h == "CANCELADA":
    print("OK: exactamente 2 horas antes se registra como CANCELADA.")
else:
    print(
        f"ERROR: se esperaba CANCELADA "
        f"y se obtuvo {estado_2h}."
    )


# ==========================================
# PRUEBA 7:
# CANCELACIÓN 1H59 ANTES
# ==========================================

print("\n--- Prueba 7: cancelación 1h59 antes ---")

hora_inicio_159 = datetime(2026, 9, 18, 20, 0)

reserva_159 = estudiante_1.solicitar_reserva(
    cancha_8,
    hora_inicio_159
)

hora_cancelacion_159 = datetime(2026, 9, 18, 18, 1)

estado_159 = estudiante_1.cancelar_reserva(
    reserva_159,
    hora_cancelacion_159
)

if estado_159 == "NO_SHOW":
    print("OK: 1h59 antes se registra como NO_SHOW.")
else:
    print(
        f"ERROR: se esperaba NO_SHOW "
        f"y se obtuvo {estado_159}."
    )


# ==========================================
# PRUEBA 8:
# DOS ESTUDIANTES INTENTAN RESERVAR
# LA MISMA CANCHA Y HORA
# ==========================================

print("\n--- Prueba 8: estudiante intenta reservar cancha ocupada por otro ---")

cancha_prueba_doble = Cancha(9, "Cancha Prueba Doble")

hora_compartida = datetime(2026, 9, 19, 19, 0)

primera_reserva = estudiante_1.solicitar_reserva(
    cancha_prueba_doble,
    hora_compartida
)

segunda_reserva = estudiante_2.solicitar_reserva(
    cancha_prueba_doble,
    hora_compartida
)

if primera_reserva and segunda_reserva is None:
    print(
        f"OK: {estudiante_1.nombre} mantiene la reserva."
    )
    print(
        f"OK: {estudiante_2.nombre} no puede reservar "
        f"la misma cancha y hora."
    )
else:
    print("ERROR: se permitió una doble reserva.")