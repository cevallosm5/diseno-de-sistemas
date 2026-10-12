# PSet 2 — Patrones de Diseño en ReservaU

**Proyecto:** ReservaU — reserva de canchas deportivas universitarias  
**Autor:** Martín Cevallos  
**Curso:** Diseño de Sistemas

## 1. Objetivo y alcance

Este PSet extiende ReservaU del PSet 1 para incorporar reservas recurrentes de equipos oficiales, reglas de cancelación diferenciadas, suspensión por no-shows, bloqueos administrativos reutilizables, dos sedes con políticas propias y control de concurrencia. La implementación es una simulación orientada a objetos en Python: no requiere servidor, base de datos, interfaz gráfica ni API.

Se mantiene la regla de prioridad del PSet 1: antes de las 18:00, un capitán de equipo oficial puede desplazar una reserva ordinaria que aún no ha comenzado, sin penalizar al estudiante desplazado; no puede desplazar otra reserva prioritaria. Fuera de ese horario no hay desplazamiento.

## 2. Organización y ejecución

```text
pset-02/
├── README.md
├── <documentos y diagramas en PDF>
└── implementacion/
    ├── simulacion.py
    ├── reserva_u_facade.py
    ├── estudiante.py
    ├── cancha.py
    ├── reserva.py
    ├── regla_prioridad.py
    ├── estrategia_cancelacion.py
    ├── fabrica_reservas.py
    ├── abs_fabrica_campus.py
    ├── campus.py
    ├── reservas_recurrentes.py
    ├── servicio_reservas_recurrentes.py
    ├── plantilla_bloqueo.py
    ├── servicio_bloqueos.py
    ├── configuracion.py
    ├── administrador.py
    └── Dockerfile
```

Desde `pset-02/implementacion/`:

```bash
docker build -t reservau-v2 .
docker run reservau-v2
```

Alternativamente, con Python 3 instalado:

```bash
python3 simulacion.py
```

La simulación termina con `LOS SIETE ESCENARIOS PASARON`. La construcción y ejecución en Docker se verificaron en el entorno de desarrollo.

## 3. Reglas de negocio y restricciones

| Regla | Comportamiento |
|---|---|
| Sedes | Norte: reservas de 06:00 a 22:00 y notificaciones por correo; Sur: 07:00 a 23:00 y notificaciones por SMS. |
| Prioridad | Antes de las 18:00 el capitán oficial puede desplazar una reserva ordinaria futura; la anulación no genera no-show. |
| Recurrentes | Entre 2 y 8 semanas consecutivas, misma cancha y horario; **todo o nada**. Un conflicto impide registrar todas las semanas e identifica la semana conflictiva. |
| Cancelación ordinaria | Con menos de 2 horas de anticipación: `NO_SHOW`; en caso contrario: `CANCELADA`. |
| Cancelación de capitán | Con menos de 24 horas de anticipación: `NO_SHOW`; en caso contrario: `CANCELADA`. |
| Anulación administrativa | Estado `ANULADA`, sin penalización, con notificación al afectado. |
| Suspensión | 3 no-shows en el mismo mes calendario impiden nuevas reservas durante 7 días. |
| Bloqueos | Una plantilla define motivo, franja y equipamiento; se clona para distintas canchas y fechas. Los conflictos existentes se anulan y notifican. |
| Concurrencia | Dos solicitudes simultáneas para la misma cancha y franja no pueden confirmar dos reservas. |

## 4. Tabla de patrones y decisión de concurrencia

| Patrón / decisión | Requerimiento que lo justifica | Problema que resuelve | Clases y métodos |
|---|---|---|---|
| **Factory Method** | RF-22, RF-08 | Evita repartir condicionales de creación y configuración de reservas entre clientes. | `FabricaDeReservas.elegir_creador()`, `CreadorReservaRegular`, `CreadorReservaPrioritaria`, `ReservaRegular`, `ReservaPrioritaria`. |
| **Abstract Factory** | RF-19, RF-20, RNF-04 | Impide mezclar accidentalmente las reglas de Norte con el canal de Sur. | `FabricaNorte`, `FabricaSur` en `abs_fabrica_campus.py`; `Campus.validar_reserva()`, `Campus.notificar()`. |
| **Builder** | RF-11, RF-12 | Evita constructores extensos y solicitudes incompletas. | `SolicitudReservaBuilder.add_capitan()`, `.add_cancha()`, `.add_fecha_inicio()`, `.add_semanas()`, `.add_equipamiento()`, `.add_observaciones()`, `.build()`; `SolicitudReservaRecurrente.obtener_fechas()`. |
| **Prototype** | RF-17, RNF-06 | Evita reconstruir manualmente cada bloqueo y compartir listas mutables. | `PlantillaBloqueo.clonar()` con `copy.deepcopy()`; `ReservaUFacade.bloquear_masivamente()`. |
| **Singleton** | RF-21, RNF-03 | Evita números de negocio dispersos y configuraciones inconsistentes. | `Configuracion.obtener_objeto()`; consultado por `PrioridadAntes18`, estrategias de cancelación y `Estudiante.registrar_no_show()`. |
| **Strategy** | RF-04, RF-06, RF-07, RF-08, RF-14, RF-15 | Evita condicionales por tipo de usuario dentro de `Reserva.cancelar()` y permite variar políticas sin alterar la reserva. | `ReglaPrioridad`, `SinPrioridad`, `PrioridadAntes18`; `CancelacionEstudiante`, `CancelacionCapitan`, `AnulacionAdministrativa`; `Reserva.establecer_estrategia()` y `.cancelar()`. |
| **Facade** | RF-01, RF-05, RF-09, RF-11, RF-18 | Reduce acoplamiento de la simulación a los subsistemas y centraliza la orquestación. | `ReservaUFacade.reservar()`, `.reservar_recurrentemente()`, `.cancelar()`, `.bloquear()`, `.bloquear_masivamente()`, `.ultimo_conflicto_recurrente`. |
| **Concurrencia: locking pesimista** | RNF-02 | Protege como una sola sección crítica la comprobación de disponibilidad y el registro de la reserva. | `Cancha.lock` (`threading.RLock`); `with cancha.lock` en operaciones de reserva y servicios; escenario 7 de `simulacion.py`. |

### 4.1. Prototype: por qué `copy.deepcopy()`

`copy.copy()` crea una copia superficial: los objetos mutables anidados, como la lista `equipamiento`, seguirían compartiéndose entre plantilla y clon. `copy.deepcopy()` duplica también esa lista, de modo que agregar un elemento al equipamiento de un clon no modifica la plantilla ni otros clones. En el escenario 6 se verifica mediante `assert` que la plantilla conserva `['Red', 'Marcador']` mientras el clon modificado contiene además `'Balones'`. Las plantillas se clonan **antes** de asociarlas con una `Cancha`, evitando copiar su `RLock`.

### 4.2. Singleton: beneficio y costo

Centralizar las reglas en `Configuracion` permite cambiar umbrales de prioridad, cancelación y suspensión en un solo lugar, sin buscar constantes en múltiples clases. A cambio, introduce estado global compartido y acoplamiento a la configuración, lo que dificulta aislar pruebas y obliga a controlar cuidadosamente los cambios de valores. El acceso se realiza mediante `Configuracion.obtener_objeto()`.

### 4.3. Concurrencia: por qué locking pesimista

ReservaU tiene **muchas más consultas de disponibilidad que escrituras**, pero las reservas se concentran en picos al inicio del semestre. Se eligió bloqueo pesimista por cancha (`RLock`) porque la sección crítica es corta y garantiza que comprobar disponibilidad y registrar la reserva sucedan de forma indivisible, sin reintentos ni versiones adicionales; la contención se limita a solicitudes de la misma cancha. Su costo es que escrituras simultáneas sobre una misma cancha esperan su turno, aun si buscan franjas diferentes; una alternativa optimista podría mejorar el rendimiento a mayor escala, pero añadiría detección de conflictos y reintentos. La simulación con dos hilos demuestra que **exactamente una** reserva queda confirmada.

## 5. Trazabilidad: requisito → caso de uso → diagrama → patrón → código → simulación

| Requisito | Caso de uso | Diagrama de comportamiento que debe reflejarlo | Patrón / mecanismo | Código responsable | Evidencia en `simulacion.py` |
|---|---|---|---|---|---|
| RF-19, RF-20, RNF-04 — Validación y aviso por sede | Reservar una cancha | Secuencia de reserva, con alternativa fuera de horario | Abstract Factory + Facade | `Campus`, `FabricaNorte`, `FabricaSur`, `ReservaUFacade.reservar()` | Escenarios **1** y **2**: EMAIL Norte, SMS Sur y rechazo a las 23:00 en Norte. |
| RF-22 — Crear reserva según solicitante | Reservar una cancha | Secuencia de reserva | Factory Method | `FabricaDeReservas`, creadores y reservas concretas | Escenarios **1**, **3** y prueba adicional de prioridad. |
| RF-11, RF-12, RF-13, RNF-05 — Reserva recurrente todo o nada | Reservar de forma recurrente | Actividad: iterar semanas, decisión de conflicto y confirmación atómica | Builder + Facade | `SolicitudReservaBuilder`, `ServicioReservasRecurrentes.confirmar()` | Escenario **3**: cuatro semanas confirmadas y rechazo total por conflicto en semana 3. |
| RF-05–RF-08, RF-14, RF-15 — Cancelación diferenciada | Cancelar una reserva | Robustez de cancelación y máquina de estados | Strategy | `Reserva.cancelar()`, estrategias de cancelación | Escenario **4**: `CANCELADA`, `NO_SHOW` y `ANULADA`. |
| RF-16 — Suspensión por 3 no-shows | Cancelar una reserva; Reservar una cancha | Robustez y estados de reserva; secuencia con alternativa «suspendido» | Singleton + Strategy + regla de entidad | `Estudiante.registrar_no_show()`, `.esta_suspendido()`, `Configuracion` | Escenario **5**: tres `NO_SHOW`, suspensión hasta 2026-11-25 15:00 y rechazo de nueva reserva. |
| RF-17, RF-18, RNF-06 — Bloqueo replicado con anulaciones | Bloquear canchas para un evento | Flujo del caso de uso y máquina de estados (`ANULADA`) | Prototype + Facade | `PlantillaBloqueo.clonar()`, `ServicioBloqueos`, `ReservaUFacade.bloquear_masivamente()` | Escenario **6**: dos bloqueos, copia profunda, anulación y notificación a Sofía. |
| RF-04 — Prioridad del capitán | Reservar una cancha | Secuencia: disponibilidad y desplazamiento | Strategy + Factory Method | `PrioridadAntes18`, `Estudiante.solicitar_reserva()` | Prueba adicional: reserva ordinaria `ANULADA`, reserva oficial `CONFIRMADA`, cero penalizaciones y aviso. |
| RNF-02 — Sin doble reserva concurrente | Reservar una cancha | Secuencia de reserva con exclusión mutua | `RLock` pesimista | `Cancha.lock`, `ReservaUFacade.reservar()` | Escenario **7**: dos hilos, una sola confirmación. |

### 5.1. Recorrido completo de la regla de tres no-shows

1. **Requisito RF-16:** después de **3 no-shows en un mismo mes calendario**, el solicitante queda suspendido **7 días**.
2. **Casos de uso:** «Cancelar una reserva» registra el no-show; «Reservar una cancha» rechaza al estudiante suspendido.
3. **Diagramas:** robustez de cancelación; secuencia de reserva con fragmento `alt [solicitante suspendido]`; máquina de estados de `Reserva` con transición a `NO_SHOW`.
4. **Entidad y responsabilidad:** `Estudiante` mantiene `no_shows`; `registrar_no_show()` contabiliza y aplica la suspensión, mientras `esta_suspendido()` determina si puede reservar. El estado de la reserva cambia a `NO_SHOW` mediante `Reserva.cancelar()` y su Strategy.
5. **Configuración:** `Configuracion` aporta el límite de **3** y la duración de **7 días**, evitando codificarlos en varios lugares.
6. **Simulación:** escenario 5: `Total NO_SHOW: 3`, `Suspendida hasta: 2026-11-25 15:00:00` y `Nueva reserva rechazada durante suspensión.`

La suspensión corresponde al **solicitante**, no a un estado de la reserva; por eso la cuenta pertenece a `Estudiante`.

## 6. Escenarios de validación

| N.º | Escenario | Resultado observado |
|---|---|---|
| 1 | Reserva en Norte y Sur | Ambas `CONFIRMADA`, correo en Norte y SMS en Sur. |
| 2 | Fuera del horario de Norte | Rechazo de solicitud a las 23:00. |
| 3 | Recurrente exitosa y conflictiva | 4 reservas confirmadas; segunda solicitud rechazada completamente por conflicto en semana 3. |
| 4 | Tres políticas de cancelación | `CANCELADA`, `NO_SHOW`, `ANULADA` sin penalización. |
| 5 | Tres no-shows en un mes | Suspensión de 7 días y nueva solicitud rechazada. |
| 6 | Bloqueo clonado en dos canchas | Clones independientes; reserva existente `ANULADA` y estudiante notificada. |
| 7 | Dos hilos, misma cancha y franja | Exactamente una reserva `CONFIRMADA`. |

Además, la simulación contiene una **prueba de desplazamiento por prioridad** antes del escenario 4. Se comprobó por separado que un bloqueo administrativo impide desplazar una reserva existente y preserva su estado.

## 7. Documentación entregada

El PSet #2 incluye los siguientes documentos:

1. `01_Requerimientos_ReservaU.pdf`: requerimientos
   funcionales RF-01 a RF-22 y no funcionales RNF-01 a RNF-06.

2. `02_Modelo_de_Dominio_ReservaU.pdf`: modelo conceptual
   de las entidades y sus relaciones.

3. `03_Diagrama_de_Casos_de_Uso_ReservaU.pdf`: actores
   y funcionalidades principales del sistema.

4. `04_Diagramas_de_Flujo_Casos_de_Uso_ReservaU.pdf`:
   flujos principales y alternativos de los casos de uso.

5. `05_Diagrama_de_Robustez_Cancelar_Reserva.pdf`:
   representación ICONIX del proceso de cancelación.

6. `06_Diagrama_de_Secuencia_Reservar_Cancha.pdf`:
   interacciones necesarias para realizar una reserva.

7. `07_Diagrama_de_Actividad_Reserva_Recurrente.pdf`:
   proceso de validación y confirmación de reservas recurrentes.

8. `08_Diagrama_de_Estados_Reserva.pdf`:
   estados y transiciones del ciclo de vida de una reserva.

Los diagramas representan el diseño del sistema.
La implementación en Python y la simulación documentan su comportamiento ejecutable.