# Event-Planning-Management-System
Atualização do projeto de p2

Structured project implementation of an Event Planning Management System for the Software Project subject.
How to execute?

    Download and run the file main.py (evento-ps.py)

Implemented Features
 Event Management

    Class Evento

        criar_evento(), cancelar_evento(), listar_eventos()

 Attendee Management

    Class Participante

        adicionar_participante_evento(), listar_participantes_evento(), excluir_participante_evento()

        Each participant receives a unique ticket (ingresso)

 Feedback and Survey Collection

    Class Survey

        criar_survey_evento() to create a satisfaction survey

    Class Feedback

        coletar_feedback_evento() to collect responses from participants

        listar_feedbacks_evento() to review feedback

 Speaker and Agenda Management

    Class Speaker

        adicionar_speaker_evento(), listar_speakers_evento(), remover_speaker_evento()

        Each speaker has a bio, topic, and scheduled time

 Financial Management

    Class Despesa

        definir_orcamento_evento(), registrar_despesa_evento(), ver_financas_evento()

        Budget planning, expense tracking, and current balance

 Vendor Coordination

    Class Fornecedor

        adicionar_fornecedor_evento(), listar_fornecedores_evento(), atualizar_status_fornecedor_evento()

        Vendor status tracking (e.g. Pendente, Confirmado)
teste