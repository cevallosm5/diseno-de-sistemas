class Inventario:
    def verificar(self, producto):
        print(f"Verificando el stock de: {producto}")
        return True # Asumimos que siempre hay stock

class Pago:
    def procesar(self, monto):
        print(f"Procesando pago: ${monto}")
        return True # Asumimos que el pago siempre es exitoso

class Envio:
    def crear_envio(self, producto):
        print(f"Preparando el envío de: {producto}")
        return True # Asumimos que el envío siempre se crea exitosamente

class ServicioNotificacion:
    def notificar_usuario(self, producto):
        print(f"Tu compra fue realizada con exito! Hemos enviado tu producto: {producto}")
        return True # Siempre llega la notificacion

class TiendaFacade:
    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()
        self.notificacion = ServicioNotificacion()

    def comprar(self, producto, precio):

        if not self.inventario.verificar(producto):
            print("No hay stock")
            return
        
        if not self.pago.procesar(precio):
            print("Fallo el pago")
            return

        self.envio.crear_envio(producto)
        self.notificacion.notificar_usuario(producto)


def main():
    
    tienda = TiendaFacade()
    tienda.comprar("Laptop", 1500)

main()