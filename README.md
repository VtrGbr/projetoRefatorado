## Créditos e Autoria

Este projeto foi desenvolvido em duas fases distintas, com contribuições fundamentais de diferentes autores:

### Projeto Original

* **Autora:** Eliane Lais de Melo Bastos
* **Git:** LaisMelo22
* **Contribuição:** Concepção e implementação inicial das funcionalidades principais do sistema de gestão de eventos, como parte da disciplina de Projeto de Software.

### Refatoração e Arquitetura de Software

* **Autor:** Vítor Gabriel dos Santos Oliveira
* **Git:** VtrGbr
* **Contribuição:** Responsável pela refatoração do projeto, migração para o Firebase Realtime Database e pela implementação de uma arquitetura avançada baseada nos seguintes padrões de projeto:
    * **Criacionais:** Singleton, Factory Method, Builder.
    * **Comportamentais:** State, Command, Observer.
    * **Estruturais:** Facade, Decorator, Adapter.

# Sistema de Gestão de Eventos

Uma implementação em Python de um sistema de gestão de eventos, utilizando Firebase como base de dados e aplicando padrões de projeto de software para uma arquitetura robusta e escalável. 
Este projeto foi originalmente desenvolvido pela aluna ELIANE LAIS DE MELO BASTOS da matéria Projeto de Software e após a troca dos projetos fiquei com este projeto e fiquei com a responsabilidade de implementar os padrões de projeto.

## Funcionalidades Implementadas

* **Gestão de Eventos:** Criação, cancelamento e listagem de eventos.
* **Gestão de Participantes:** Adição de diferentes tipos de participantes (Regular, VIP, Estudante) com benefícios automáticos, listagem e remoção.
* **Gestão de Locais:**  Adição, listagem e remoção de locais, com a capacidade de importar locais a partir de ficheiros CSV.
* **Notificações:** Sistema de notificação (via Firebase) para o cancelamento de eventos.
* **Gestão Financeira:** Definição de orçamento e registo de despesas por evento.
* **Coordenação de Fornecedores:** Gestão completa de fornecedores, incluindo adição, listagem e atualização de status.
* **Gestão de Palestrantes (Speakers):** Adição, listagem e remoção de palestrantes de um evento.
* **Feedback e Pesquisas:** Criação de pesquisas e recolha de feedback dos participantes.

---

## Configuração e Instalação

Para executar este projeto, são necessários alguns passos de configuração, principalmente para a ligação com a base de dados Firebase.

### Pré-requisitos

* Python 3.x
* Conta Google para aceder ao Firebase

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git) cd seu-repositorio 
```

#  Instalar dependências
Este projeto requer a biblioteca firebase-admin. Instale-a usando o pip:

```bash
pip install firebase-admin
```

# Configurar a Base de Dados Firebase

O sistema utiliza o Firebase Realtime Database para armazenar todos os dados. Siga estes passos:

1. Acesse o Console do Firebase e crie um novo projeto.

2. No menu do projeto, vá para Build > Realtime Database e crie uma nova base de dados. Pode começar no modo de teste para permitir leituras e escritas.

3. Vá para Configurações do Projeto (ícone de engrenagem) > Contas de serviço.

4. Clique em "Gerar nova chave privada". Será feito o download de um ficheiro .json.

5. **IMPORTANTE**: Renomeie este ficheiro para projetorefatorado-firebase-adminsdk-fbsvc-d9be3a5d92.json e coloque-o na pasta raiz do seu projeto. O ficheiro .gitignore já está configurado para impedir que este ficheiro sensível seja enviado para o GitHub.

# Como Executar
Após concluir a configuração, execute o ficheiro principal para iniciar o menu interativo:
```bash
python evento.py
```
# Arquitetura e Padrões de Projeto
O projeto foi desenhado com uma arquitetura limpa e multi-camada, separando as responsabilidades para garantir um código flexível, manutenível e de alta qualidade.

## Estrutura de Ficheiros
O código-fonte está organizado nas seguintes pastas principais:

- criacionais/: Contém os padrões responsáveis pela criação de objetos (Singleton, Factory, Builder).

- comportamentais/: Contém os padrões que gerem a comunicação e o fluxo da aplicação (Command, Observer, State).

- estruturais/: Contém os padrões que lidam com a composição e a relação entre objetos (Decorator, Facade, Adapter).

- tratar/: Onde as exceções personalizadas (exceptions.py) podem residir.

- sistemaEvento.py: O coração do sistema, contendo a lógica de negócio principal.

- evento.py: O ponto de entrada da aplicação, responsável por iniciar a Facade.

### Padrões de Projeto Utilizados
Abaixo está um detalhe de cada padrão implementado, onde encontrá-lo e como ele funciona.

## Padrões Criacionais
Padrões que abstraem o processo de instanciação de objetos.

1. Singleton

- Onde: criacionais/firebaseServico.py

- Propósito: Garante que existe apenas uma única instância da ligação com o Firebase em toda a aplicação. Isto otimiza recursos e evita conflitos de ligação.

- Como: O método __new__ da classe FirebaseServico verifica se uma instância (_instance) já existe. Se não, ele cria uma nova, inicia a ligação com o Firebase e guarda as referências da base de dados. Em todas as chamadas subsequentes, ele retorna a instância que já existe.

```python

# em criacionais/firebaseServico.py
class FirebaseServico:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseServico, cls).__new__(cls)
            # ... (lógica de inicialização do Firebase) ...
            cls._instance.eventos_ref = db.reference('eventos')
        return cls._instance

firebase_service_instance = FirebaseServico() # A instância única
```
2. Factory Method

- Onde: criacionais/factory.py

- Propósito: Centraliza a lógica de criação de diferentes tipos de Participante (Regular, VIP, Estudante). O cliente (neste caso, o SistemaEventos) pede um participante de um "tipo" sem precisar de saber qual classe concreta será instanciada.

- Como: Um método estático criar_participante recebe o tipo e retorna a instância da classe correta (ParticipanteVIP, ParticipanteRegular, etc.).

```python

# em criacionais/factory.py
class ParticipanteFactory:
    @staticmethod
    def criar_participante(tipo, nome, email):
        if tipo.lower() == 'vip':
            participanteBase = ParticipanteVIP(nome, email)
        elif tipo.lower() == 'regular':
            participanteBase =  ParticipanteRegular(nome, email)
        # ...
        return participanteDecorator # Retorna o participante decorado
```
3. Builder

- Onde: criacionais/builder.py

- Propósito: Simplifica a criação de um objeto complexo (neste caso, o dicionário de dados de um Evento) passo a passo. Permite que o mesmo processo de construção crie representações diferentes (ex: um evento com ou sem orçamento).

- Como: A classe EventoBuilder é inicializada com os dados essenciais (nome, data). Métodos como com_orcamento(valor) podem ser encadeados para adicionar partes opcionais. O método build() finaliza o processo e retorna o dicionário completo, pronto para o Firebase.

```python

# em criacionais/builder.py
class EventoBuilder:
    def __init__(self, nome, data):
        self._evento_data = { 'nome': nome, 'data': data, ... }

    def com_orcamento(self, valor):
        self._evento_data['orcamento'] = float(valor)
        return self # Retorna self para encadeamento
    
    def build(self):
        return self._evento_data
```
## Padrões Comportamentais
Padrões que gerem a comunicação e a distribuição de responsabilidades entre os objetos.

1. State

- Onde: comportamentais/state.py

- Propósito: Gere o fluxo da aplicação como uma máquina de estados finitos. Cada menu (Menu Principal, Gerir Eventos, etc.) é um "Estado". Isto organiza a navegação, elimina menus aninhados e torna claro o fluxo do programa.

- Como: O SistemaEventos (o Contexto) mantém uma referência ao estado atual (self._state). Cada classe de estado (ex: MenuPrincipalState) tem um método run() que contém o seu próprio loop de menu. Quando o utilizador escolhe uma opção de navegação, o estado chama self.sistema.set_state(...) para fazer a transição para o próximo estado.

```python

# em comportamentais/state.py
class MenuPrincipalState(MaquinaEstados):
    def run(self):
        # ... (mostra o menu) ...
        if op == '1':
            # Transição para o próximo estado
            self.sistema.set_state(GestaoEventoState(self.sistema))
            break
```

2. Command

- Onde: comportamentais/command.py

- Propósito: Encapsula cada ação do utilizador (como "criar evento") num objeto Commando. Isto desacopla quem invoca a ação (o menu, no State) de quem a executa (a Facade). Elimina a necessidade de blocos if/elif gigantes.

- Como: Cada estado (state.py) cria um dicionário que mapeia a escolha do utilizador (ex: '1') para uma instância de um Commando (ex: CriarEventoCommand(facade)). Quando o utilizador faz uma escolha, o estado apenas executa o comando (comando.executar()), sem precisar de saber o que ele faz.

```python

# em comportamentais/command.py
class CriarEventoCommand(Commando):
    def __init__(self, facade: 'SistemaFacade'):
        self.facade = facade
    def executar(self):
        self.facade.criar_evento() # Delega a chamada para a Facade
```

3. Observer

- Onde: comportamentais/observer.py e sistemaEvento.py

- Propósito: Desacopla a lógica de cancelamento de um evento da lógica de notificação. Quando um evento é cancelado, o SistemaEventos (o Subject) notifica todos os Observers (como o NotificacaoObservador) que estão "anexados" a ele.

- Como: O SistemaEventos mantém uma lista _observadores. A Facade anexa o NotificacaoObservador a esta lista. Quando cancelar_evento é chamado, o SistemaEventos chama self.notificar(...), que itera sobre a lista e chama o método atualizar() de cada observador.

```python

# em comportamentais/observer.py
class NotificacaoObservador:
    def atualizar(self, nomeEvento, listaEmail):
        # ... (lógica para criar notificações no Firebase) ...
        self.notificacoes_ref.push(notificacaoData)

# em sistemaEvento.py
class SistemaEventos:
    def anexar(self, observador):
        self._observadores.append(observador)
    
    def notificar(self, nomeEvento, listaEmail):
        for observador in self._observadores:
            observador.atualizar(nomeEvento, listaEmail)
```
## Padrões Estruturais
Padrões que lidam com a composição e a relação entre objetos.

1. Facade

- Onde: estruturais/facade.py

- Propósito: Fornece um ponto de entrada único e simplificado para todo o subsistema. O cliente (o evento.py) interage apenas com a SistemaFacade, que esconde toda a complexidade de inicializar o SistemaEventos, configurar o Observer, etc..

- Como: A SistemaFacade é a única classe que o evento.py importa. No seu __init__, a Facade cria a instância do SistemaEventos e chama _configurarServicos() para anexar os observadores. O método iniciarAplicacao() da facade é o único que o evento.py chama para executar o programa.

```python

# em estruturais/facade.py
class SistemaFacade:
    def __init__(self):
        self._sistema = SistemaEventos()
        self._configurarServicos()

    def _configurarServicos(self):
        notificacaoServico = NotificacaoObservador(...)
        self._sistema.anexar(notificacaoServico)
    
    def iniciarAplicacao(self):
        self._sistema.ExecutarEstado()
```
2. Decorator

- Onde: estruturais/decorator.py e criacionais/factory.py

- Propósito: Adiciona benefícios e responsabilidades extras (como "Camisa" ou "Certificado") a objetos Participante dinamicamente. Isto evita a "explosão de subclasses" (ex: VipComCamisa, RegularComCertificado, etc.).

- Como: O ParticipanteDecorator herda de Participante e "embrulha" um objeto participante. Decoradores concretos (ex: BeneficioCamisaDecorator) sobrescrevem o método to_dict() para adicionar os benefícios aos dados. O padrão é usado pela ParticipanteFactory, que aplica os decoradores padrão automaticamente com base no tipo de participante.

```python

# em estruturais/decorator.py
class ParticipanteDecorator(Participante):
    def __init__(self, participanteEmbrulhado):
        self._participante = participanteEmbrulhado
    
    def __getattr__(self, name): # Delega atributos como 'ingresso'
        return getattr(self._participante, name)

class BeneficioCamisaDecorator(ParticipanteDecorator):
    def to_dict(self):
        data = self._participante.to_dict()
        data['beneficios'] = data.get('beneficios', []) + ['Camisa Oficial']
        return data
```
3. Adapter

- Onde: estruturais/adapter.py

- Propósito: Atua como um "tradutor" para permitir que o sistema importe dados de fontes externas com interfaces incompatíveis (como ficheiros CSV).

- Como: Classes como LocaisCsvAdapter ou ParticipanteCsvAdapter são criadas. Elas sabem como ler um formato de ficheiro específico (ex: um CSV com colunas nome_do_espaco, morada_completa) e "traduzem" esses dados para o formato que o SistemaEventos entende (um dicionário com chaves nome, endereco, etc.).

```python

# em estruturais/adapter.py (exemplo do adaptador de fornecedor)
class FornecedorCsvAdapter:
    def obter_fornecedores(self):
        fornecedores_adaptados = []
        with open(self._caminho_arquivo, ...) as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                # "Tradução" dos dados do CSV para o formato do sistema
                fornecedor_data = {
                    'nome': linha['fornecedor'],
                    'servico': linha['servico'],
                    'contato': linha['contato'],
                    'status': 'Pendente'
                }
                fornecedores_adaptados.append(fornecedor_data)
        return fornecedores_adaptados
```
# Implementação do tratamento de exceções
O sistema usa exceções personalizadas para garantir que a lógica de negócio permaneça limpa e que o utilizador receba feedback claro.

## Tratamentos usados
 No arquivo 'excessões.py' estão classes que eu usei para fazer tratamentos específicos:

Propósito: Este ficheiro centraliza a definição de todos os erros que são específicos da lógica do seu sistema. Em vez de usar erros genéricos como ValueError para tudo, você criou erros nomeados que descrevem exatamente o que deu errado.

Classe Base (ErroBase): Esta classe ErroBase que herda de Exception. Permite que as outras camadas do código (como a Facade) possam, se necessário, apanhar qualquer erro de negócio usando um único except ErroDeNegócio as e:, tornando o código mais limpo.

### Exceções Específicas:

- EventoJaExistenteError, DataInvalidaError, NomeInvalidoError: São usadas para validação de dados na entrada do utilizador.

- OrcamentoInvalidoError, EmailInvalidoError: Permitem um controle muito específico sobre diferentes tipos de falhas, cada uma podendo ser tratada de forma diferente se necessário.


### Usados em código: 

## Específicos: 

Onde: sistemaEvento.py

- EmailInvalidoError:

```python

    def adicionar_speaker_evento(self):
        sel = self.selecionar_evento()
        if not sel: return
        try:    
            # Coleta as informações do palestrante
            nome = input("Nome do palestrante: ")
            if not nome:
                raise NomeInvalidoError("O campo nome não pode estar vazio!")
            if nome.isdigit():
                raise NomeInvalidoError("O nome não pode ser um número!")
            bio = input("Bio: ")

            if not bio or bio.isdigit():
                raise NomeInvalidoError("O campo não pode ser um número ou estar vazio!")
            email = input("Email: ")

            if "@" not in email:
                raise EmailInvalidoError("O email deve conter o @!")
            topico = input("Tópico da palestra: ")
            ...

```

- EventoJaExistenteError, NomeInvalidoError, DataInvalidaError, OrcamentoInvalidoError e genérica (Exeception): 

```python

    def criar_evento(self):
        print("\n--- Criação de Novo Evento ---")
   
        nome = input("Nome do evento: ")
        if not nome:
            raise NomeInvalidoError("O nome não pode estar vazio")
        if nome.isdigit():
            raise NomeInvalidoError("O nome do evento não pode ser um número!")
        
        eventoExistente = self.eventos_ref.child(nome).get()
        if eventoExistente:
            raise EventoJaExistenteError(f"Já existe um evento com o nome: {nome}")
        
        data = input("Data (dd/mm/aaaa): ")
        if not data:
            raise DataInvalidaError("A data do evento não pode estar vazia")
        
        try:
            dataEvento = datetime.strptime(data, '%d/%m/%Y').date()
            if dataEvento < datetime.now().date():
                raise DataInvalidaError("A data do evento não pode ser uma data no passado.")
        except ValueError:
            raise DataInvalidaError("O formato da data deve ser dd/mm/aaaa e a data deve ser válida.")
        
        orcamento_str = input("Definir orçamento inicial (opcional): ")

        try:
            builder = EventoBuilder(nome, data)
            
            if orcamento_str:
                try:
                    builder.com_orcamento(orcamento_str)
                except ValueError:
                    
                    raise OrcamentoInvalidoError(f"Valor de orçamento '{orcamento_str}' inválido. Use apenas números.")

            novo_evento_data = builder.build()
            self.eventos_ref.child(nome).set(novo_evento_data)
            
            
            print(f"SUCESSO: Evento '{nome}' criado com sucesso!")

        except OrcamentoInvalidoError as e:
            
            raise e
        except Exception as e:
            # Apanha erros de gravação no Firebase
            raise Exception(f"Erro ao salvar o evento no Firebase: {e}")

```
## Nativos do python

Onde: estruturais/adapter.py

- FileNotFoundError

```python

class FornecedorCsvAdapter:
    def __init__(self, caminho_arquivo):
        self._caminho_arquivo = caminho_arquivo
    
    def obterFornecedores(self):
        
        fornecedores = []

        try:
            with open(self._caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
                leitor_csv = csv.DictReader(arquivo)
                
                print("\nA ler ficheiro CSV de fornecedores...")
                for linha in leitor_csv:
                    try:
                        fornecedor_data = {
                            'nome': linha['fornecedor'],
                            'servico': linha['servico'], 
                            'contato': linha['contato'],
                            'status': 'Pendente'  
                        }
                        
                        fornecedores.append(fornecedor_data)

                    except KeyError as e:
                        print(f"Erro de Adaptador: A coluna {e} não foi encontrada no arquivo CSV. A verificar a próxima linha.")
                        continue

            return fornecedores

        except FileNotFoundError:
            print(f"Erro do Adaptador: arquivo não encontrado em '{self._caminho_arquivo}'")
            return None
        except Exception as e:
            print(f"Erro do Adaptador ao processar o arquivo: {e}")
            return None


```

- ValueError

Onde: sistemaEvento.py

```python

    def selecionar_evento(self):
        eventos = self.eventos_ref.get()
        if not eventos:
            print("Nenhum evento registado no Firebase.")
            return None

        eventos_lista = list(eventos.items())

        print("\nEventos disponíveis:")
        for i, (nome_evento, dados_evento) in enumerate(eventos_lista):
           
            data_evento = dados_evento.get('data', 'Sem data')
            print(f"{i}. {nome_evento} (Data: {data_evento})")

        try:
            idx_str = input("Selecione o evento pelo número: ")
         
            if not idx_str.isdigit():
                print("Seleção inválida. Por favor, digite um número.")
                return None
            
            idx = int(idx_str)
            if 0 <= idx < len(eventos_lista):
                return eventos_lista[idx][0]
            else:
                print("Seleção inválida.")
                return None
                
        except ValueError: 
            print("Seleção inválida.")
            return None
```