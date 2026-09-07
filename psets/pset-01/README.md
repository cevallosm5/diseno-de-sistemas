# PSet 1: Anaisis y Diseño de ReservaU

**Nombre:** Martin Cevallos\
**Código:** 00335290\
**NRC:** 1642\
**Fecha:** 6 de septiembre de 2026

## Descripcion

ReservaU es una plataforma para la reserva de canchas deportivas universitarias. Este PSet desarrolla el sistema desde la definición de requerimientos hasta una implementación orientada a objetos en Python.

El sistema permite a estudiantes reservar y cancelar canchas, aplica prioridad a capitanes de equipos oficiales antes de las 6:00 p. m., clasifica automáticamente las cancelaciones realizadas con menos de dos horas de anticipación como no-show y permite al administrador gestionar la disponibilidad de las canchas e intervenir en conflictos de reservas.

## Estructura del proyecto

``` 
pset-01/
├── README.md
├── 01_Requerimientos_ReservaU.pdf
├── 02_Modelo_de_Dominio_ReservaU.pdf
├── 03_Diagrama_de_Casos_de_Uso_ReservaU.pdf
├── 04_Diagramas_de_Flujo_Casos_de_Uso_ReservaU.pdf
└── implementacion/
    ├── administrador.py
    ├── cancha.py
    ├── equipo.py
    ├── estudiante.py
    ├── regla_prioridad.py
    ├── reserva.py
    ├── simulacion.py
    └── Dockerfile
```

## Documentación

-   **01_Requerimientos_ReservaU.pdf:** requerimientos funcionales y no funcionales.
-   **02_Modelo_de_Dominio_ReservaU.pdf:** clases, atributos, responsabilidades, relaciones y reglas de negocio.
-   **03_Diagrama_de_Casos_de_Uso_ReservaU.pdf:** visión general de los actores y casos de uso del sistema.
-   **04_Diagramas_de_Flujo_Casos_de_Uso_ReservaU.pdf:** flujos principales y alternos de CU-01 a CU-04.

## Implementación

La carpeta `implementacion/` contiene una implementación orientada a objetos del modelo de dominio.

La regla de prioridad se implementa mediante composición: cada estudiante tiene una regla de prioridad. Los estudiantes normales utilizan `SinPrioridad` y los capitanes utilizan `PrioridadAntes18`.

La clasificación entre cancelación normal y no-show es responsabilidad de `Reserva`, según el tiempo restante antes del inicio.

## Docker

Construir la imagen desde `implementacion/`:

``` bash
docker build -t reservau .
```

Ejecutar:

``` bash
docker run reservau
```

El contenedor ejecuta `simulacion.py`, imprime la simulación completa y termina al finalizar el script.