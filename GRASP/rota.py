class Rota:
    def __init__(self, veiculo, rota, distancia):
        self.veiculo = veiculo
        self.rota = rota
        self.distancia = distancia

    def exibirRota(self):
        print('     * Rota')
        print(f'Veiculo: {self.veiculo}')
        print(f'Rota: {self.rota}')
        print(f'Custo: {self.distancia}')