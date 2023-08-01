from ..enums.test import Enumeracao


class Entidade:
    def __init__(self, index, name):
        self.id = index
        self.name = name
    @staticmethod
    def print():
        print(Enumeracao.RED.value + Enumeracao.GREEN.value)