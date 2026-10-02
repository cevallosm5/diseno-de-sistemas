from factories import FantasyFactory, SciFiFactory
from strategies import AtaqueNormal, AtaqueFuerte
from config import GameConfig


class GameFacade:
    def __init__(self):
        self.config = GameConfig.obtener_objeto()
        self.jugador = None
        self.enemigo = None
        self.estrategia = None
        self.turno = 0

    def seleccionar_mundo(self, mundo):
        if mundo == "fantasia":
            factory = FantasyFactory()
        elif mundo == "scifi":
            factory = SciFiFactory()
        else:
            raise ValueError("Mundo no válido")

        self.jugador = factory.crear_jugador()
        self.enemigo = factory.crear_enemigo()

    def seleccionar_estrategia(self, estrategia):
        if estrategia == "normal":
            self.estrategia = AtaqueNormal()
        elif estrategia == "fuerte":
            self.estrategia = AtaqueFuerte()
        else:
            raise ValueError("Estrategia no válida")

    def atacar(self):
        if self.estrategia is None:
            raise ValueError("Debe seleccionar una estrategia antes de atacar")

        danio = self.estrategia.calcular_danio(self.jugador)
        self.enemigo.recibir_ataque(danio)

        return danio

    def ataque_enemigo(self):
        danio = self.enemigo.ataque
        self.jugador.recibir_ataque(danio)

        return danio

    def ejecutar_turno(self):
        self.turno += 1

        danio_jugador = self.atacar()

        if not self.enemigo.esta_vivo():
            return {
                "danio_jugador": danio_jugador,
                "danio_enemigo": 0
            }

        danio_enemigo = self.ataque_enemigo()

        return {
            "danio_jugador": danio_jugador,
            "danio_enemigo": danio_enemigo
        }

    def partida_terminada(self):
        if not self.jugador.esta_vivo():
            return True

        if not self.enemigo.esta_vivo():
            return True

        if self.turno >= self.config.numero_maximo_turnos:
            return True

        return False

    def determinar_ganador(self):
        if self.jugador.vida <= 0:
            return self.enemigo

        if self.enemigo.vida <= 0:
            return self.jugador

        if self.turno >= self.config.numero_maximo_turnos:
            if self.jugador.vida > self.enemigo.vida:
                return self.jugador
            elif self.enemigo.vida > self.jugador.vida:
                return self.enemigo
            else:
                return None

        return None

    def iniciar(self):
        print("=== VIDEOJUEGO POR TURNOS ===")

        print("\nSelecciona un mundo:")
        print("1. Fantasía")
        print("2. Ciencia ficción")

        opcion_mundo = input("> ")

        if opcion_mundo == "1":
            self.seleccionar_mundo("fantasia")
        elif opcion_mundo == "2":
            self.seleccionar_mundo("scifi")
        else:
            print("Opción no válida")
            return

        print(f"\nJugador: {self.jugador.nombre}")
        print(f"Enemigo: {self.enemigo.nombre}")

        while not self.partida_terminada():
            print(f"\n--- TURNO {self.turno + 1} ---")
            print(f"{self.jugador.nombre}: {self.jugador.vida} HP")
            print(f"{self.enemigo.nombre}: {self.enemigo.vida} HP")

            print("\nSelecciona una estrategia:")
            print("1. Ataque normal")
            print("2. Ataque fuerte")

            opcion_estrategia = input("> ")

            if opcion_estrategia == "1":
                self.seleccionar_estrategia("normal")
            elif opcion_estrategia == "2":
                self.seleccionar_estrategia("fuerte")
            else:
                print("Opción no válida")
                continue

            resultado = self.ejecutar_turno()

            print(
                f"\n{self.jugador.nombre} causó "
                f"{resultado['danio_jugador']} de daño."
            )

            if resultado["danio_enemigo"] > 0:
                print(
                    f"{self.enemigo.nombre} causó "
                    f"{resultado['danio_enemigo']} de daño."
                )

        ganador = self.determinar_ganador()

        print("\n=== FIN DE LA PARTIDA ===")

        if ganador:
            print(f"Ganador: {ganador.nombre}")
        else:
            print("Empate")