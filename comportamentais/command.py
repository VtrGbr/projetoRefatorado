from abc import ABC, abstractmethod

#Classe abstrata para o comando

class Commando(ABC):
    @abstractmethod
    def executar(self):
        pass

# --- Gerenciar evento
class CriarEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    
    def executar(self):
        self.sistema.criar_evento()

class CancelarEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    
    def executar(self):
        self.sistema.cancelar_evento()

class ListarEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.listar_eventos()

class CriarSurveyEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.criar_survey_evento()

class ColetarFeedbackEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.coletar_feedback_evento()

class ListarFeedbacksEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.listar_feedbacks_evento()

class AdicionarSpeakerEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.adicionar_speaker_evento()

class ListarSpeakersEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.listar_speakers_evento()

class RemoverSpeakerEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaEventos'):
        self.sistema = sistema
    def executar(self):
        self.sistema.remover_speaker_evento()

class ReservarLocalEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.reservar_local_evento()

# ----- Gerenciar participante

class AdicionarParticipanteEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.adicionar_participante_evento()

class ListarParticipanteEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.listar_participantes_evento()

class ExcluirParticipanteEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.excluir_participante_evento()

# --- Gerenciar Fornecedor

class AdicionarFornecedorEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.adicionar_fornecedor_evento()

class ListarFornecedorEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.listar_fornecedores_evento()

class AtualizarStatusFornecedorEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.atualizar_status_fornecedor_evento()

# --- Gerenciar Finanças

class DefinirOrcamentoEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.definir_orcamento_evento()

class RegistrarDespesaEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.registrar_despesa_evento()

class VerfinancasEventoCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.ver_financas_evento()

class RemoverDespesaEventoCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.remover_despesa_evento()
# --- Gerenciar Local

class AdicionarLocalCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.adicionar_local()

class ListarLocaisDisponiveisCommand(Commando):
    def __init__(self, sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.listar_locais_disponiveis()

class RemoverLocalCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.remover_local()

class GerarRelatorioGeralCommand(Commando):
    def __init__(self,sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.gerar_relatorio_completo_evento()
        
class ImportarLocaisCsvCommand(Commando):
    def __init__(self,sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.importar_locais_de_csv()

class ImportarParticipanteCsvCommand(Commando):
    def __init__(self,sistema : 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.importar_participantes_csv()

class ImportarFornecedorCsvCommand(Commando):
    def __init__(self, sistema: 'SistemaFacade'):
        self.sistema = sistema
    def executar(self):
        self.sistema.importar_fornecedor_csv()