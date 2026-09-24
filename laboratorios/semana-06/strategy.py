from abc import ABC, abstractmethod

class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, precio_base):
        pass

class SinDescuento(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base

class DescuentoVIP(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.8  # 20% de descuento

class DescuentoEstudiante(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.95 # 5% de descuento

class DescuentoEmpleado(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.75 # 25% de descuento

class Compra:
    def __init__(self, EstrategiaDescuento):
        self.estrategia_descuento = EstrategiaDescuento

    def calcular_total(self, precio_base):
        return self.estrategia_descuento.aplicar(precio_base)

def main():
    cliente_normal = SinDescuento()
    cliente_vip = DescuentoVIP()
    cliente_estudiante = DescuentoEstudiante()
    cliente_empleado = DescuentoEmpleado()

    compra1 = Compra(cliente_normal)
    print(compra1.calcular_total(100))  # Salida: 100

    compra2 = Compra(cliente_vip)
    print(compra2.calcular_total(1000))  # Salida: 800

    compra3 = Compra(cliente_estudiante)
    print(compra3.calcular_total(10))  # Salida: 9.5

    compra4 = Compra(cliente_empleado)
    print(compra4.calcular_total(200))  # Salida: 150

main()