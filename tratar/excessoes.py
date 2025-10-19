'''
    Este arquivo, conterá as classes para os tratamentos de excessões específicas para a maioria dos métodos
'''

class ErroBase(Exception):
    pass

class EventoJaExistenteError(ErroBase):
    pass

class DataInvalidaError(ErroBase):
    pass

class NomeInvalidoError(ErroBase):
    pass

class EmailInvalidoError(ErroBase):
    pass

class TopicoInvalidoError(ErroBase):
    pass

class HorarioInvalidoError(ErroBase):
    pass
class OrcamentoInvalidoError(ErroBase):
    def __init__(self,saldoDisponivel, despesa ):
        self.saldoDisponivel = saldoDisponivel
        self.despesa = despesa
        mensagem = f"O valor R$ {despesa:.2f} excede o valor disponível R$ {saldoDisponivel:.2f}"      
        super().__init__(mensagem)


