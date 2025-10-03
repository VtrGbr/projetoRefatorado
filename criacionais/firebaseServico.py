# firebase_service.py
import firebase_admin
from firebase_admin import credentials, db

class FirebaseServico:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("A criar a instância do FirebaseService...")
            cls._instance = super(FirebaseServico, cls).__new__(cls)
            try:
                #Credencial
                cred = credentials.Certificate("projetorefatorado-firebase-adminsdk-fbsvc-d9be3a5d92.json")
                # URL do banco de dados
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://projetorefatorado-default-rtdb.firebaseio.com/'
                })
                print("Conexão Firebase iniciada com sucesso.")
            except ValueError as e:
                print(f"Firebase já iniciado: {e}")
            
            # Referências do banco de dados
            cls._instance.eventos_ref = db.reference('eventos')
            cls._instance.locais_ref = db.reference('locais')
            cls._instance.notificacoes_ref = db.reference('notificacoes')
            
        return cls._instance

# Exporta a instância única
firebase_service_instance = FirebaseServico()