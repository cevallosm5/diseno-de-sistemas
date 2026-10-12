import copy


class PlantillaBloqueo:

    def __init__(self, motivo, hora_inicio, hora_fin, equipamiento=None):
        self.motivo = motivo
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.equipamiento = (
            list(equipamiento) if equipamiento is not None else []
        )

        self.cancha = None
        self.fecha = None

    def clonar(self):
        return copy.deepcopy(self)
