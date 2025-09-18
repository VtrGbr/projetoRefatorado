class Local:
    def __init__(self, nome, endereco, capacidade):
        self.nome = nome
        self.endereco = endereco
        self.capacidade = capacidade
        self.disponibilidade = True

    def verificar_disponibilidade(self):
        return self.disponibilidade

    def reservar(self):
        self.disponibilidade = False
        print(f"Local '{self.nome}' reservado.")