from abc import ABC, abstractmethod

# Validador
class ValidadorCampus(ABC):

    @abstractmethod
    def validar_horario(self, fecha_hora):
        pass

class ValidadorNorte(ValidadorCampus):

    def validar_horario(self, fecha_hora):
        return 6 <= fecha_hora.hour < 22

class ValidadorSur(ValidadorCampus):

    def validar_horario(self, fecha_hora):
        return 7 <= fecha_hora.hour < 23

# Notificador
class Notificador(ABC):

    @abstractmethod
    def enviar(self, destinatario, mensaje):
        pass

class NotificadorEmail(Notificador):

    def enviar(self, destinatario, mensaje):
        print(f"EMAIL para {destinatario}: {mensaje}")

class NotificadorSMS(Notificador):

    def enviar(self, destinatario, mensaje):
        print(f"SMS para {destinatario}: {mensaje}")


# Fabrica abstracta
class FabricaCampusABC(ABC):

    @abstractmethod
    def crear_validador(self):
        pass

    @abstractmethod
    def crear_notificador(self):
        pass

# Fabrica: Campus Norte
class FabricaNorte(FabricaCampusABC):

    def crear_validador(self):
        return ValidadorNorte()

    def crear_notificador(self):
        return NotificadorEmail()

# Fabrica: Campus Sur
class FabricaSur(FabricaCampusABC):

    def crear_validador(self):
        return ValidadorSur()

    def crear_notificador(self):
        return NotificadorSMS()