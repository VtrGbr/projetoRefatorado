import csv
from criacionais.builder import EventoBuilder
from criacionais.factory import ParticipanteFactory 

class LocaisCsvAdapter():
    def __init__(self, caminhoFicheiro):
        self._caminhoFicheiro = caminhoFicheiro
    
    def obterLocais(self):
        locais ={}

        try:
            with open(self._caminhoFicheiro, mode = 'r', encoding='utf-8') as ficheiro:
                leitor_csv = csv.DictReader(ficheiro)
                for linha in leitor_csv:
                    #"Tradução"
                    nome_local = linha['nome_do_espaco']
                    locais[nome_local]= {
                        'nome': nome_local,
                        'endereco': linha['morada_completa'],
                        'capacidade': int(linha['lotacao_maxima'])
                    }
            
            return locais
        except FileNotFoundError:
            print(f"Erro do adaptador: Ficheiro não encontrado em {self._caminhoFicheiro}")
            return None
        except Exception as e:
            print(f"Erro do Adaptador ao processar o ficheiro: {e}")
            return None

