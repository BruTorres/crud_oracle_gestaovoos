class Aeronave:
    def __init__(self, 
                 codigoCalda:str=None, 
                 nomeAeronave:str=None
                ):
        self.set_codigoCalda(codigoCalda)
        self.set_nomeAeronave(nomeAeronave)

    def set_codigoCalda(self, codigoCalda:str):
        self.codigoCalda = codigoCalda

    def set_nomeAeronave(self, nomeAeronave:str):
        self.nomeAeronave = nomeAeronave

    def get_codigoCalda(self) -> str:
        return self.codigoCalda

    def get_nomeAeronave(self) -> str:
        return self.nomeAeronave

    def to_string(self) -> str:
        return f"Código Calda: {self.get_codigoCalda()} | Nome: {self.get_nomeAeronave()}"