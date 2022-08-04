class Veiculo:
    def __init__(self, nome, capacidade):
        self.nome = nome
        self.capacidade = capacidade
        self.statusAtividade = True
    
    def status(self, capacidade):
        print('     * Status do Veículo')
        print(f'Nome: {self.nome}')
        print(f'Capacidade: {capacidade}')
        print(f'Status da atividade: {self.statusAtividade}')

    def getNome(self): return self.nome

    def getCapacidade(self): return self.capacidade
    def setCapacidade(self, valor): self.capacidade = valor
    
    def getStatusAtividade(self): return self.statusAtividade
    def setStatusAtividade(self, valor): self.statusAtividade = valor