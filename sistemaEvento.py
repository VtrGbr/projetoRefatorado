from criacionais.factory import ParticipanteFactory #Factory method
from criacionais.firebaseServico import firebase_service_instance # singleton
from criacionais.builder import EventoBuilder #Builder

from comportamentais.command import *
from comportamentais.observer import NotificacaoObservador
from comportamentais.state import MenuPrincipalState

from estruturais.decorator import *
from estruturais.adapter import LocaisCsvAdapter

class SistemaEventos:
    def __init__(self):
        self._observadores = [] # observer
        #Agora usaremos a instância única do Singleton para aceder às referências
        self.db_service = firebase_service_instance
        self.eventos_ref = self.db_service.eventos_ref
        self.locais_ref = self.db_service.locais_ref
        self.notificacoes_ref = self.db_service.notificacoes_ref

        #state
        self._state = MenuPrincipalState(self)

    def set_state(self, novoEstado):
        
        self._state = novoEstado
        print(f"---- Mudança de Estado {novoEstado} ----")
    
    def ExecutarEstado(self):
        while self._state is not None:
            self._state.run()


    def anexar(self,observador):
        self._observadores.append(observador)

    def notificar(self,nomeEvento,listaEmail):
        for observador in self._observadores:
            observador.atualizar(nomeEvento,listaEmail)

    def selecionar_evento(self):
        eventos = self.eventos_ref.get()
        if not eventos:
            print("Nenhum evento cadastrado no Firebase.")
            return None

        eventos_lista = list(eventos.items()) # Transforma o dicionário em uma lista de tuplas (nome, dados)

        print("\nEventos disponíveis:")
        for i, (nome_evento, dados_evento) in enumerate(eventos_lista):
            print(f"{i}. {nome_evento} (Data: {dados_evento['data']})")

        try:
            idx = int(input("Selecione o evento pelo número: "))
            # Retorna o nome do evento selecionado (que é a chave no Firebase)
            return eventos_lista[idx][0]
        except (ValueError, IndexError):
            print("Seleção inválida.")
            return None


    def reservar_local_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        
        #Carregando os locais disponiveis
        print("-- Carregando os locais disponiveis")
        locaisDisponiveis = self.locais_ref.get()

        if not locaisDisponiveis:
            print("Nenhum local disponível para reserva. Adicione um local primeiro no menu 'Gerir locais")
            return
        
        #Transformar o dicionario em uma lista
        locais_lista = list(locaisDisponiveis.values())

        print("\n--- Escolha um local para fazer a reserva ---")
        for i, local in enumerate(locais_lista):
            print(f"{i}. {local['nome']} ({local['endereco']}) - Capacidade: {local['capacidade']}")

        try:
            index = int(input("Selecione o local pelo número: "))
            local_escolhido = locais_lista[index]

            #preparar os dados do local para guardar no evento
            local_data ={
                'nome': local_escolhido['nome'],
                'endereco': local_escolhido['endereco'],
                'capacidade': local_escolhido['capacidade']
            }    

            self.eventos_ref.child(sel).child('local_reservado').set(local_data)
            print(f"Local '{local_escolhido['nome']}' reservado com sucesso para o evento '{sel}'.")
        except (ValueError, IndexError):
            print("Seleção inválida.")
        except Exception as e:
            print(f"Ocorreu um erro ao reservar o local: {e}")

 

   
    def criar_evento(self):
        print("\n--- Criando novo evento ---")
        nome = input("Nome: ")
        data = input("Data (dd/mm/aaaa): ")
        try:
            # Usa o Builder para construir o objeto do evento
            builder = EventoBuilder(nome, data)
            
            orcamento_str = input("Definir orçamento inicial (opcional, ex: 5000): ")
            if orcamento_str:
                builder.com_orcamento(orcamento_str)
            
            # Constrói o dicionário final
            novo_evento_data = builder.build()
            
            # Salva no Firebase
            self.eventos_ref.child(nome).set(novo_evento_data)
            print(f"Evento '{nome}' criado com sucesso usando o padrão Builder.")
        except Exception as e:
            print(f"Erro ao criar evento: {e}")

    
    
    def cancelar_evento(self):
        nome_evento = self.selecionar_evento()
        if not nome_evento:
            return

        # 1. Obter os dados do evento diretamente do Firebase
        evento_ref = self.eventos_ref.child(nome_evento)
        dados_evento = evento_ref.get()

        if not dados_evento:
            print("Evento não encontrado no Firebase.")
            return

        # 2. Obter a lista de e-mails dos participantes a partir dos dados do Firebase
        lista_emails = []
        if 'participantes' in dados_evento and dados_evento['participantes']:
            lista_emails = [p['email'] for p in dados_evento['participantes'].values()]

        # 3. Enviar os e-mails
        if lista_emails:
            self.notificar(nome_evento,lista_emails)
            
            print("Notificações criadas com sucesso.")
        else:
            print("Nenhum participante para notificar.")

        # 4. Remover o evento do Firebase
        try:
            evento_ref.delete()
            print(f"Evento '{nome_evento}' cancelado e removido do Firebase.")
        except Exception as e:
            print(f"Erro ao remover evento do Firebase: {e}")
    
    def listar_eventos(self):
        # Pega todos os dados do nó 'eventos'
        eventos = self.eventos_ref.get()
        if not eventos:
            print("Nenhum evento cadastrado.")
            return

        print("\nEventos cadastrados:")
        for nome_evento, dados_evento in eventos.items():
            print(f"- {dados_evento['nome']} ({dados_evento['data']})")

    def criar_survey_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        perguntas = []
        titulo = input("Título da pesquisa: ")
        print("Digite perguntas (deixe em branco e pressione Enter para encerrar):")
        while True:
            p = input("> ")
            if not p: break
            perguntas.append(p)

        # Prepara os dados da pesquisa para salvar no Firebase
        nova_survey_data = {
            'titulo': titulo,
            'perguntas': perguntas
        }

        # Salva a nova pesquisa no Firebase sob o evento selecionado
        try:
            # .push() cria um ID único para a pesquisa
            self.eventos_ref.child(sel).child('Enquete').push(nova_survey_data)
            print(f"Pesquisa '{titulo}' criada com sucesso no Firebase para o evento '{sel}'.")
        except Exception as e:
            print(f"Erro ao salvar a pesquisa no Firebase: {e}")

    def coletar_feedback_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Primeiro, verifica se o ingresso do participante existe no evento
        ingresso = input("Confirme seu Ingresso: ")
        participantes_ref = self.eventos_ref.child(sel).child('participantes')
        participantes = participantes_ref.get()

        if not participantes or ingresso not in participantes:
            print("Ingresso não encontrado para este evento.")
            return

        # Busca a pesquisa mais recente do evento no Firebase
        surveys_ref = self.eventos_ref.child(sel).child('Enquete')
        todas_surveys = surveys_ref.order_by_key().limit_to_last(1).get()

        if not todas_surveys:
            print("Nenhuma pesquisa disponível para este evento.")
            return

        # Pega o ID e os dados da última pesquisa adicionada
        id_survey, dados_survey = list(todas_surveys.items())[0]

        respostas = {}
        print(f"\n--- Respondendo à Pesquisa: {dados_survey['titulo']} ---")
        for pergunta in dados_survey['perguntas']:
            respostas[pergunta] = input(f"{pergunta}: ")

        # Prepara os dados do feedback para salvar
        novo_feedback_data = {
            'ingresso_participante': ingresso,
            'respostas': respostas,
            'id_pesquisa': id_survey # Guarda a referência de qual pesquisa foi respondida
        }

        # Salva o feedback no Firebase
        try:
            self.eventos_ref.child(sel).child('feedbacks').push(novo_feedback_data)
            print("Feedback registrado com sucesso. Obrigado por participar!")
        except Exception as e:
            print(f"Erro ao salvar o feedback no Firebase: {e}")

    def listar_feedbacks_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Pega todos os feedbacks do evento no Firebase
        feedbacks = self.eventos_ref.child(sel).child('feedbacks').get()

        if not feedbacks:
            print("Nenhum feedback registrado para este evento.")
            return

        print(f"\n--- Feedbacks do Evento: {sel} ---")
        # Itera sobre cada feedback (cada um com seu ID único)
        for fb_id, fb_data in feedbacks.items():
            print(f"\nFeedback (Participante com Ingresso: {fb_data['ingresso_participante']})")
            for pergunta, resposta in fb_data['respostas'].items():
                print(f"- {pergunta}: {resposta}")
            print("-" * 20)


    def adicionar_speaker_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Coleta as informações do palestrante
        nome = input("Nome do palestrante: ")
        bio = input("Bio: ")
        email = input("Email: ")
        topico = input("Tópico da palestra: ")
        horario = input("Horário (ex: 14:30): ")

        # Estrutura os dados para salvar no Firebase
        novo_speaker_data = {
            'nome': nome,
            'bio': bio,
            'email': email,
            'topico': topico,
            'horario': horario
        }

        # Salva o novo palestrante no Firebase
        try:
            self.eventos_ref.child(sel).child('Palestrante').push(novo_speaker_data)
            print(f"Palestrante '{nome}' adicionado com sucesso ao evento '{sel}'.")
        except Exception as e:
            print(f"Erro ao salvar o palestrante no Firebase: {e}")

    def listar_speakers_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Pega todos os palestrantes do evento no Firebase
        speakers = self.eventos_ref.child(sel).child('Palestrante').get()

        if not speakers:
            print("Nenhum palestrante cadastrado para este evento.")
            return

        print(f"\n--- Palestrantes do Evento: {sel} ---")
        # Itera sobre cada palestrante (cada um com seu ID único)
        for speaker_id, speaker_data in speakers.items():
            print(f"\nNome: {speaker_data['nome']}")
            print(f"  Tópico: '{speaker_data['topico']}' às {speaker_data['horario']}")
            print(f"  Email: {speaker_data['email']}")
            print(f"  ID para remoção: {speaker_id}") # Mostra o ID
        print("-" * 20)
        return speakers # Retorna os dados para serem usados pela função de remoção

    def remover_speaker_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Primeiro, lista os palestrantes para o usuário ver os IDs
        speakers = self.listar_speakers_evento()
        if not speakers:
            return # Se não houver palestrantes, encerra a função

        # Pede ao usuário o ID do palestrante a ser removido
        speaker_id_para_remover = input("\nDigite o ID do palestrante que deseja remover: ")

        # Verifica se o ID fornecido existe antes de tentar remover
        if speaker_id_para_remover in speakers:
            try:
                # Remove o palestrante do Firebase usando seu ID único
                speaker_nome = speakers[speaker_id_para_remover]['nome']
                self.eventos_ref.child(sel).child('Palestrante').child(speaker_id_para_remover).delete()
                print(f"Palestrante '{speaker_nome}' removido com sucesso.")
            except Exception as e:
                print(f"Erro ao remover o palestrante do Firebase: {e}")
        else:
            print("ID inválido ou não encontrado.")
   
    #factory method
    def adicionar_participante_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        nome = input("Nome: ") 
        email = input("Email: ")
        tipo = input("Tipo de participante (Regular/Vip/Estudante): ")
        
        try:
            # Usa a Factory para criar o objeto do tipo correto
            participante = ParticipanteFactory.criar_participante(tipo, nome, email)
            
            # Converte o objeto para dicionário e guarda no Firebase
            self.eventos_ref.child(sel).child('participantes').child(participante.ingresso).set(participante.to_dict())
            print(f"Participante '{nome}' ({participante.tipo}) adicionado com sucesso!")
            print(f"Ingresso: {participante.ingresso}")
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    def listar_participantes_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Obtém os dados dos participantes do Firebase
        participantes = self.eventos_ref.child(sel).child('participantes').get()

        if not participantes:
            print("Nenhum participante registado para este evento.")
            return

        print(f"\n--- Participantes do Evento: {sel} ---")
        for ingresso, dados in participantes.items():
            print(f"- {dados['nome']} ({dados['email']}) | Ingresso: {ingresso}")

    def excluir_participante_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        ingresso_para_remover = input("Digite o Ingresso do participante a ser removido: ")

        # Ponto de referência para o participante específico
        participante_ref = self.eventos_ref.child(sel).child('participantes').child(ingresso_para_remover)

        # Verifica se o participante existe antes de tentar remover
        if not participante_ref.get():
            print("Ingresso não encontrado.")
            return

        try:
            # Remove o participante do Firebase
            participante_ref.delete()
            print(f"Participante com ingresso '{ingresso_para_remover}' removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover participante: {e}")


    def adicionar_fornecedor_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        nome = input("Nome do fornecedor: ")
        servico = input("Serviço prestado: ")
        contato = input("Contato (opcional): ")

        fornecedor_data = {
            'nome': nome,
            'servico': servico,
            'contato': contato,
            'status': 'Pendente'
        }

        try:
            # Adiciona o fornecedor com um ID único
            self.eventos_ref.child(sel).child('fornecedores').push(fornecedor_data)
            print(f"Fornecedor '{nome}' adicionado com sucesso.")
        except Exception as e:
            print(f"Erro ao adicionar fornecedor: {e}")

    def listar_fornecedores_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        fornecedores = self.eventos_ref.child(sel).child('fornecedores').get()

        if not fornecedores:
            print("Nenhum fornecedor registado para este evento.")
            return None # Retorna None se não houver fornecedores

        print(f"\n--- Fornecedores do Evento: {sel} ---")
        for fid, dados in fornecedores.items():
            print(f"Nome: {dados['nome']} | Serviço: {dados['servico']} | Status: {dados['status']}")
            print(f"  ID para atualização: {fid}")
        return fornecedores

    def atualizar_status_fornecedor_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Lista os fornecedores para o utilizador ver os IDs
        fornecedores = self.listar_fornecedores_evento()
        if not fornecedores:
            return

        fid_para_atualizar = input("\nDigite o ID do fornecedor para atualizar o status: ")
        if fid_para_atualizar not in fornecedores:
            print("ID inválido.")
            return

        novo_status = input("Digite o novo status (ex: Confirmado, Pago): ")

        try:
            # Atualiza apenas o campo 'status' do fornecedor
            fornecedor_ref = self.eventos_ref.child(sel).child('fornecedores').child(fid_para_atualizar)
            fornecedor_ref.update({'status': novo_status})
            print("Status do fornecedor atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")

    def definir_orcamento_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        try:
            valor = float(input("Digite o valor do orçamento: R$"))
            # Guarda o orçamento diretamente no nó do evento
            self.eventos_ref.child(sel).update({'orcamento': valor})
            print(f"Orçamento de R${valor:.2f} definido para o evento '{sel}'.")
        except ValueError:
            print("Erro: Por favor, digite um número válido.")
        except Exception as e:
            print(f"Erro ao definir o orçamento: {e}")

    def registrar_despesa_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        descricao = input("Descrição da despesa: ")
        try:
            valor = float(input("Valor da despesa: R$"))
        except ValueError:
            print("Erro: Por favor, digite um número válido.")
            return
        data = input("Data da despesa (dd/mm/aaaa): ")

        despesa_data = {
            'descricao': descricao,
            'valor': valor,
            'data': data
        }

        try:
            # Adiciona a despesa à lista de despesas do evento
            self.eventos_ref.child(sel).child('despesas').push(despesa_data)
            print("Despesa registada com sucesso.")
        except Exception as e:
            print(f"Erro ao registar a despesa: {e}")

    def ver_financas_evento(self):
        sel = self.selecionar_evento()
        if not sel: return

        # Obtém todos os dados do evento
        dados_evento = self.eventos_ref.child(sel).get()
        if not dados_evento:
            print("Evento não encontrado.")
            return

        orcamento = dados_evento.get('orcamento', 0.0)
        despesas = dados_evento.get('despesas', {})

        total_gasto = sum(item['valor'] for item in despesas.values())
        saldo = orcamento - total_gasto

        print(f"\n--- Finanças do Evento: {sel} ---")
        print(f"Orçamento Total: R${orcamento:.2f}")
        print("\nDespesas Registadas:")
        if not despesas:
            print("Nenhuma despesa registada.")
        else:
            for item in despesas.values():
                print(f"- {item['descricao']} (R${item['valor']:.2f}) em {item['data']}")
        print("-" * 20)
        print(f"Total Gasto: R${total_gasto:.2f}")
        print(f"Saldo Disponível: R${saldo:.2f}")

    
    def adicionar_local(self):
        print("\n---Adicionar um novo local---")
        nome = input("Nome do local: ")
        endereco = input("Endereço: ")
        try:
            capacidade = int(input("Capacidade: "))
        except ValueError:
            print("Erro: A capacidade deve ser um número")
            return
        
        #Guardar no fire base
        local_data={
            'nome': nome,
            'endereco': endereco,
            'capacidade': capacidade
        }

        try:
            self.locais_ref.child(nome).set(local_data)
            print(f"Local '{nome}' adicionado com sucesso! ")
        except Exception as e:
            print("Erro ao guardar o local no Firebase: {e}")
    
    def listar_locais_disponiveis(self):
        print("\n--- Locais Disponíveis ---")
        locais = self.locais_ref.get()

        if not locais:
            print("Nenhum local registrado")
            return
        for nome, dados in locais.items():
            print(f"- {dados['nome']} ({dados['endereco']} - Capacidade {dados['capacidade']})")
        return locais
    
    def remover_local(self):

        locaisExistentes = self.listar_locais_disponiveis()
        if not locaisExistentes:
            return
        localidade = input("Digite o local que deseja remover: ")
        
        
        if localidade not in locaisExistentes:
            print("Esta localidade não se encontra no banco de dados.")
            return
        localRemover_ref = self.locais_ref.child(localidade)
           

        try:
            # Remove o participante do Firebase
            localRemover_ref.delete()
            print(f"O local '{localidade}' removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover localiade: {e}")
    


    def importar_locais_de_csv(self):
        print("\n--- Importar Locais de um Ficheiro CSV ---")
        caminho = input("Digite o caminho para o ficheiro CSV: ")
        
        # O sistema não sabe como ler um CSV. Ele apenas sabe que o adaptador
        # tem um método .obter_locais() que lhe devolverá os dados no formato correto.
        adaptador = LocaisCsvAdapter(caminho)
        novos_locais = adaptador.obterLocais() #Retorna um dicionario para colocar no banco de dados
        
        if novos_locais:
            # O método .update() do Firebase adiciona ou atualiza os locais
            self.locais_ref.update(novos_locais)
            print(f"\n{len(novos_locais)} locais foram importados com sucesso!")
