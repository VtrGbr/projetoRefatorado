import random
from sistemaEvento import SistemaEventos, NotificacaoObservador

if __name__ == "__main__":
    # O Singleton é inicializado aqui, na primeira vez que é chamado
    sistema = SistemaEventos()
    notificacaoServico = NotificacaoObservador(sistema.notificacoes_ref)

    sistema.anexar(notificacaoServico)
    sistema.ExecutarEstado()
    #sistema.menu() 


    print("\nSistema pronto. A instância do Firebase foi carregada.")