class GameConfig:
    _objeto = None

    def __init__(self):
        self.dificultad = "normal"
        self.numero_maximo_turnos = 10
        GameConfig._objeto = self

    @staticmethod
    def obtener_objeto():
        if GameConfig._objeto is None:
            GameConfig()

        return GameConfig._objeto