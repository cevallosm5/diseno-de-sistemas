class GestorDeConfiguracion:
    _objeto = None

    def __init__(self):
        self.modo_mantenimiento = False
        GestorDeConfiguracion._objeto = self


    # Necesito tener en mi clase un metodo que haga referencia a mi objeto
    @staticmethod
    def obtener_objeto(): 
        if GestorDeConfiguracion._objeto is None:
            GestorDeConfiguracion()
        
        return GestorDeConfiguracion._objeto
    
def reserva_permitida(gestor):
    return not gestor.modo_mantenimiento

