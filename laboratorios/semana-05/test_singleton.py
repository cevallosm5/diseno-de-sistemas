from singleton import GestorDeConfiguracion, reserva_permitida

def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True

    assert reserva_permitida(config) is False

def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto()
    
    # Pensamiento inicial: No hace falta cambiar el modo de mantenimiento, ya que por defecto es False
    # Solucion: Cambiar el modo de mantenimiento a False antes de hacer la prueba
    config.modo_mantenimiento = False

    assert reserva_permitida(config) is True

    # Razon por la que falla: Al haber cambiado el modo de mantemiento en test_rechaza_reserva, el modo de mantenimiento ahora es True, por lo que la reserva no es aceptada. Esto se debe a que GestorDeConfiguracion es un singleton, y por lo tanto, la instancia obtenida en test_reserva_aceptada es la misma que la obtenida en test_rechaza_reserva, ya que es Global.