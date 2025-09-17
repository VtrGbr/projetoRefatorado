import random

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

class SistemaEventos:
    def __init__(self):
        self.eventos = {}

    def selecionar_evento(self):
        if not self.eventos:
            print("Nenhum evento cadastrado.")
            return None
        print("\nEventos disponíveis:")
        for i, (n, e) in enumerate(self.eventos.items()):
            print(f"{i}. {n} (Data: {e.data})")
        try:
            idx = int(input("Selecione o evento: "))
            return list(self.eventos.keys())[idx]
        except (ValueError, IndexError):
            print("Seleção inválida.")
            return None

    def gerenciar_evento(self):
        while True:
            print("\n--- GERENCIAR EVENTO ---")
            print("1. Criar evento")
            print("2. Cancelar evento")
            print("3. Listar eventos")
            print("4. Criar pesquisa de satisfação")
            print("5. Coletar feedback")
            print("6. Listar feedbacks")
            print("7. Adicionar palestrante")
            print("8. Listar palestrantes")
            print("9. Remover palestrante")
            print("0. Voltar")
            op = input("Opção: ")
            if   op == '1': self.criar_evento()
            elif op == '2': self.cancelar_evento()
            elif op == '3': self.listar_eventos()
            elif op == '4': self.criar_survey_evento()
            elif op == '5': self.coletar_feedback_evento()
            elif op == '6': self.listar_feedbacks_evento()
            elif op == '7': self.adicionar_speaker_evento()
            elif op == '8': self.listar_speakers_evento()
            elif op == '9': self.remover_speaker_evento()
            elif op == '0': break
            else: print("Inválido.")


    def gerenciar_participante(self):
        while True:
            print("\n--- GERENCIAR PARTICIPANTE ---")
            print("1. Adicionar participante")
            print("2. Listar participantes")
            print("3. Excluir participante")
            print("0. Voltar")
            op = input("Opção: ")
            if   op == '1': self.adicionar_participante_evento()
            elif op == '2': self.listar_participantes_evento()
            elif op == '3': self.excluir_participante_evento()
            elif op == '0': break
            else: print("Inválido.")


    def gerenciar_fornecedores(self):
        while True:
            print("\n--- GERENCIAR FORNECEDORES ---")
            print("1. Adicionar fornecedor")
            print("2. Listar fornecedores")
            print("3. Atualizar status de fornecedor")
            print("0. Voltar")
            op = input("Opção: ")
            if   op == '1': self.adicionar_fornecedor_evento()
            elif op == '2': self.listar_fornecedores_evento()
            elif op == '3': self.atualizar_status_fornecedor_evento()
            elif op == '0': break
            else: print("Inválido.")


    def gerenciar_financas(self):
        while True:
            print("\n--- GERENCIAR FINANÇAS ---")
            print("1. Definir orçamento")
            print("2. Registrar despesa")
            print("3. Ver finanças")
            print("0. Voltar")
            op = input("Opção: ")
            if   op == '1': self.definir_orcamento_evento()
            elif op == '2': self.registrar_despesa_evento()
            elif op == '3': self.ver_financas_evento()
            elif op == '0': break
            else: print("Inválido.")


    def criar_evento(self):
        nome = input("Nome: ")
        if nome in self.eventos:
            print("Já existe.")
            return
        data = input("Data (dd/mm/aaaa): ")
        self.eventos[nome] = Evento(nome, data)
        print(f"'{nome}' criado.")

    def cancelar_evento(self):
        select = self.selecionar_evento()
        if select:
            del self.eventos[select]
            print(f"'{select}' cancelado.")

    def listar_eventos(self):
        if not self.eventos:
            print("Nenhum cadastrado.")
            return
        for e in self.eventos.values():
            print(f"- {e.nome} ({e.data})")

    def criar_survey_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        perguntas = []
        titulo = input("Título da pesquisa: ")
        print("Digite perguntas (vazio para encerrar):")
        while True:
            p = input("> ")
            if not p: break
            perguntas.append(p)
        self.eventos[sel].criar_survey(titulo, perguntas)

    def coletar_feedback_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        ingresso = input("Ingresso: ")
        self.eventos[sel].coletar_feedback(ingresso)

    def listar_feedbacks_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        self.eventos[sel].listar_feedbacks()

    def adicionar_speaker_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        n = input("Nome: "); bio = input("Bio: ")
        email = input("Email: "); top = input("Tópico: ")
        hr = input("Horário: ")
        sp = Speaker(n, bio, email, top, hr)
        self.eventos[sel].adicionar_speaker(sp)

    def listar_speakers_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        self.eventos[sel].listar_speakers()

    def remover_speaker_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        idx = int(input("Índice do palestrante: "))
        self.eventos[sel].remover_speaker(idx)

    def adicionar_participante_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        n = input("Nome: "); e = input("Email: ")
        p = Participante(n, e)
        self.eventos[sel].adicionar_participante(p)
        print(f"Ingresso: {p.ingresso}")

    def listar_participantes_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        self.eventos[sel].listar_participantes()

    def excluir_participante_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        i = input("Ingresso: ")
        self.eventos[sel].excluir_participante(i)

    def adicionar_fornecedor_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        n = input("Nome: "); s = input("Serviço: ")
        c = input("Contato (opcional): ") or None
        f = Fornecedor(n, s, c)
        self.eventos[sel].adicionar_fornecedor(f)

    def listar_fornecedores_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        self.eventos[sel].listar_fornecedores()

    def atualizar_status_fornecedor_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        idx = int(input("Índice do fornecedor: "))
        st = input("Novo status: ")
        self.eventos[sel].atualizar_fornecedor(idx, st)

    def definir_orcamento_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        val = input("Valor orçamento: R$")
        self.eventos[sel].definir_orcamento(val)

    def registrar_despesa_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        d = input("Descrição: ")
        v = float(input("Valor: R$"))
        dt = input("Data: ")
        self.eventos[sel].registrar_despesa(d, v, dt)

    def ver_financas_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        self.eventos[sel].ver_financas()

    def menu(self):
        while True:
            print("\n====== MENU PRINCIPAL ======")
            print("1. Gerenciar Evento")
            print("2. Gerenciar Participante")
            print("3. Gerenciar Fornecedores")
            print("4. Gerenciar Finanças")
            print("0. Sair")
            opc = input("Opção: ")
            if   opc == '1': self.gerenciar_evento()
            elif opc == '2': self.gerenciar_participante()
            elif opc == '3': self.gerenciar_fornecedores()
            elif opc == '4': self.gerenciar_financas()
            elif opc == '0':
                print("Encerrando...")
                break
            else:
                print("Inválido.")


if __name__ == "__main__":
    SistemaEventos().menu()