from personajes import Guerrero, Dragon, Soldado, Alien

class CreadorDePersonajes:
    def crear_personaje(self):
        raise NotImplementedError

class CreadorDeGuerrero(CreadorDePersonajes):
    def crear_personaje(self):
        return Guerrero()

class CreadorDeDragon(CreadorDePersonajes):
    def crear_personaje(self):
        return Dragon()

class CreadorDeSoldado(CreadorDePersonajes):
    def crear_personaje(self):
        return Soldado()

class CreadorDeAlien(CreadorDePersonajes):
    def crear_personaje(self):
        return Alien()

class PersonajeFactory:
    @staticmethod
    def elegir_creador(tipo):
        if tipo == "guerrero":
            return CreadorDeGuerrero()
        elif tipo == "dragon":
            return CreadorDeDragon()
        elif tipo == "soldado":
            return CreadorDeSoldado()
        elif tipo == "alien":
            return CreadorDeAlien()

        raise ValueError("Tipo de personaje no válido")

    @staticmethod
    def crear(tipo):
        creador = PersonajeFactory.elegir_creador(tipo)
        return creador.crear_personaje()

class MundoFactory:
    def crear_jugador(self):
        raise NotImplementedError

    def crear_enemigo(self):
        raise NotImplementedError

class FantasyFactory(MundoFactory):
    def crear_jugador(self):
        return PersonajeFactory.crear("guerrero")

    def crear_enemigo(self):
        return PersonajeFactory.crear("dragon")

class SciFiFactory(MundoFactory):
    def crear_jugador(self):
        return PersonajeFactory.crear("soldado")

    def crear_enemigo(self):
        return PersonajeFactory.crear("alien")