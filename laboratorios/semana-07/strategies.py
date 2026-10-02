class EstrategiaAtaque:
    def calcular_danio(self, personaje):
        raise NotImplementedError

class AtaqueNormal(EstrategiaAtaque):
    def calcular_danio(self, personaje):
        return personaje.ataque

class AtaqueFuerte(EstrategiaAtaque):
    def calcular_danio(self, personaje):
        return personaje.ataque * 2
