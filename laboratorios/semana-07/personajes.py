class Personajes():
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    def recibir_ataque(self, danio):
        self.vida = max(0, self.vida - danio)

    def esta_vivo(self):
        return self.vida > 0

class Guerrero(Personajes):
    def __init__(self):
        super().__init__("Guerrero", 100, 20)

class Dragon(Personajes):
    def __init__(self):
        super().__init__("Dragon", 140, 20)

class Soldado(Personajes):
    def __init__(self):
        super().__init__("Soldado", 100, 20)

class Alien(Personajes):
    def __init__(self):
        super().__init__("Alien", 130, 20)