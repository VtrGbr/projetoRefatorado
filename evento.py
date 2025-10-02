import random
from sistemaEvento import *


class Participante:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self.ingresso = self.gerar_ingresso()

    def gerar_ingresso(self):
        return f"ING{random.randint(1000, 9999)}"


class Despesa:
    def __init__(self, descricao, valor, data):
        self.descricao = descricao
        self.valor = float(valor)
        self.data = data


class Survey:
    def __init__(self, titulo, perguntas):
        self.titulo = titulo
        self.perguntas = perguntas


class Feedback:
    def __init__(self, ingresso, respostas):
        self.ingresso = ingresso
        self.respostas = respostas


class Fornecedor:
    def __init__(self, nome, servico, contato=None):
        self.nome = nome
        self.servico = servico
        self.contato = contato
        self.status = "Pendente"

    def atualizar_status(self, novo_status):
        self.status = novo_status
        print(f"Status de '{self.nome}' atualizado para {self.status}.")


class Speaker:
    def __init__(self, nome, bio, email, topico, horario):
        self.nome = nome
        self.bio = bio
        self.email = email
        self.topico = topico
        self.horario = horario

class Evento:
    def __init__(self, nome, data):
        self.nome = nome
        self.data = data
        self.participantes = {}
        self.fornecedores = []
        self.budget = 0.0
        self.expenses = []
        self.surveys = []
        self.feedbacks = []
        self.speakers = []
        self.local = None

    def criar_survey(self, titulo, perguntas):
        survey = Survey(titulo, perguntas)
        self.surveys.append(survey)
        print(f"Survey '{titulo}' criada.")

    def coletar_feedback(self, ingresso):
        if ingresso not in self.participantes:
            print("Ingresso não encontrado.")
            return
        if not self.surveys:
            print("Nenhuma pesquisa disponível.")
            return
        survey = self.surveys[-1]
        respostas = {}
        print(f"Survey: {survey.titulo}")
        for p in survey.perguntas:
            respostas[p] = input(f"{p} ")
        fb = Feedback(ingresso, respostas)
        self.feedbacks.append(fb)
        print("Feedback registrado.")

    def listar_feedbacks(self):
        if not self.feedbacks:
            print("Nenhum feedback registrado.")
            return
        print(f"\nFeedbacks de '{self.nome}':")
        for fb in self.feedbacks:
            print(f"Ingresso: {fb.ingresso}")
            for p, r in fb.respostas.items():
                print(f"- {p}: {r}")

    def adicionar_participante(self, participante):
        self.participantes[participante.ingresso] = participante

    def listar_participantes(self):
        if not self.participantes:
            print("Nenhum participante cadastrado.")
            return
        print(f"\nParticipantes de '{self.nome}':")
        for ing, p in self.participantes.items():
            print(f"- {p.nome} ({p.email}) | Ingresso: {ing}")

    def excluir_participante(self, ingresso):
        if ingresso in self.participantes:
            nome = self.participantes[ingresso].nome
            del self.participantes[ingresso]
            print(f"Participante '{nome}' removido.")
        else:
            print("Ingresso não encontrado.")


    def adicionar_fornecedor(self, fornecedor):
        self.fornecedores.append(fornecedor)

    def listar_fornecedores(self):
        if not self.fornecedores:
            print("Nenhum fornecedor cadastrado.")
            return
        print(f"\nFornecedores de '{self.nome}':")
        for f in self.fornecedores:
            print(f"- {f.nome} | Serviço: {f.servico} | Status: {f.status}")

    def atualizar_fornecedor(self, índice, status):
        try:
            self.fornecedores[índice].atualizar_status(status)
        except IndexError:
            print("Índice inválido.")

    def definir_orcamento(self, valor):
        self.budget = float(valor)
        print(f"Orçamento definido: R${self.budget:.2f}")

    def registrar_despesa(self, descricao, valor, data):
        d = Despesa(descricao, valor, data)
        self.expenses.append(d)
        print(f"Despesa '{descricao}' de R${valor:.2f} em {data} registrada.")

    def ver_financas(self):
        total = sum(d.valor for d in self.expenses)
        saldo = self.budget - total
        print(f"Orçamento: R${self.budget:.2f}")
        print(f"Total gasto: R${total:.2f}")
        print(f"Saldo: R${saldo:.2f}")

    def adicionar_speaker(self, sp):
        self.speakers.append(sp)
        print(f"Palestrante '{sp.nome}' adicionado.")

    def listar_speakers(self):
        if not self.speakers:
            print("Nenhum palestrante cadastrado.")
            return
        print(f"\nPalestrantes de '{self.nome}':")
        for sp in self.speakers:
            print(f"- {sp.nome} sobre '{sp.topico}' às {sp.horario} ({sp.email})")

    def remover_speaker(self, índice):
        try:
            rem = self.speakers.pop(índice)
            print(f"Palestrante '{rem.nome}' removido.")
        except IndexError:
            print("Índice inválido.")





if __name__ == "__main__":
    # O Singleton é inicializado aqui, na primeira vez que é chamado
    sistema = SistemaEventos()
    notificacaoServico = NotificacaoObservador(sistema.notificacoes_ref)

    sistema.anexar(notificacaoServico)
    sistema.ExecutarEstado()
    #sistema.menu() 


    print("\nSistema pronto. A instância do Firebase foi carregada.")