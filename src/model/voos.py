from datetime import date
from model.aeronaves import Aeronave

class Voo:
    def __init__(self, 
                 numeroVoo:int=None, 
                 dataVoo:date=None,
                 codigoCalda:Aeronave=None
                 ):
        self.set_numeroVoo(numeroVoo)
        self.set_dataVoo(dataVoo)
        self.set_codigoCalda(codigoCalda)

    def set_numeroVoo(self, numeroVoo:int):
        self.numeroVoo = numeroVoo

    def set_dataVoo(self, dataVoo:date):
        self.dataVoo = dataVoo

    def set_codigoCalda(self, codigoCalda:Aeronave):
        self.codigoCalda = codigoCalda

    def get_numeroVoo(self) -> int:
        return self.numeroVoo

    def get_dataVoo(self) -> date:
        return self.dataVoo
    
    def get_codigoCalda(self) -> Aeronave:
        return self.codigoCalda

    def to_string(self) -> str:
        return f"Número do voo: {self.get_numeroVoo()} | Descrição: {self.get_dataVoo()} | Código calda: {self.get_codigoCalda()}"