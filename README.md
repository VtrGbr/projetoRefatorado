# Sistema de Gestão de Eventos

Uma implementação em Python de um sistema de gestão de eventos, utilizando Firebase como base de dados e aplicando padrões de projeto de software para uma arquitetura robusta e escalável. Este projeto foi desenvolvido para a disciplina de Projeto de Software.

## Funcionalidades Implementadas

* **Gestão de Eventos:** Criação, cancelamento e listagem de eventos.
* **Gestão de Participantes:** Adição de participantes (com diferentes tipos), listagem e remoção.
* **Gestão de Locais:** Adição e listagem de locais disponíveis para os eventos.
* **Notificações:** Sistema de notificação (via Firebase) para o cancelamento de eventos.
* **Gestão Financeira:** Definição de orçamento e registo de despesas por evento.
* **Coordenação de Fornecedores:** Adição, listagem e atualização de status de fornecedores.
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
O código foi refatorado para seguir uma arquitetura mais limpa e aplicar padrões de projeto criacionais, melhorando a manutenibilidade e a flexibilidade do sistema.

Estrutura de Ficheiros
O projeto está organizado da seguinte forma:

- evento.py: Contém a classe principal SistemaEventos que gere a lógica e os menus da aplicação.

- firebaseServico.py: Implementa um serviço para a ligação com o Firebase.

- builder.py: Contém a implementação do padrão Builder.

- factory.py: Contém a implementação do padrão Factory Method.

- local.py: Contém a classe Local.

## Padrões de Projeto Criacionais Utilizados
- Singleton (firebaseServico.py): Garante que existe apenas uma única instância da ligação com a base de dados Firebase em toda a aplicação. Isto evita a inicialização múltipla e o consumo desnecessário de recursos.

- Factory Method (factory.py): Utilizado para criar diferentes tipos de participantes (Regular, VIP, Estudante). A classe ParticipanteFactory delega a criação do objeto correto, permitindo que o sistema seja facilmente estendido com novos tipos de participantes sem alterar o código principal.

- Builder (builder.py): Empregado para a construção de objetos de Evento. O EventoBuilder permite a criação de um evento passo a passo (definindo nome, data, orçamento, etc.), simplificando um processo de criação que poderia ser complexo e tornando o código mais legível.

## Padrões de Projeto Comportamentais Utilizados
- Command (command.py): Utilizado para substituir os 'ifs' dentro das opções "gerenciar_evento","gerenciar_participante", "gerenciar_financas", "gerenciar_palestrante" e "gerenciar_locais". Assim garantimos que o código fica mais exuto e limpo  

- Observer (observer.py): Na função "cancelar_evento", a lógica de cancelamento está diretamente acoplada à lógica de criação de notificações no Firebase. O padrão Observer permite que um objeto (o "Observado", ou Subject) notifique automaticamente uma lista de objetos dependentes (os "Observadores", ou Observers) quando o seu estado muda, sem que o Subject precise de saber quem são os Observers.

- Stage (stage.py) : O padrão stage atua como uma máquina de estados finitos. Já que o código muitas vezes navega entre "munu Principal" depois "Estado de geração de evento" depois para " Estado de geração de participantes" e assim por diante; este padrão permite que um objeto altere o seu comportamento quando o seu estado interno muda.

## Padrões de Projeto Estruturais Utilizados
- Decorator (decorator.py): Fiz uma junção com o factory, para que quando um participante for adicionado ele obtenha benefícios de acordo com o seu tipo