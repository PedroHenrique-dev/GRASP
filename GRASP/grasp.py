from rota import Rota
from veiculo import Veiculo
from deposito import Deposito
from cliente import Cliente
from math import sqrt
from random import randint, shuffle

class GRASP:
    def __init__(self, matriz, deposito, capacidadeVeiculo):
        self.deposito = Deposito(deposito[0], deposito[1], deposito[2], deposito[3])
        self.matriz = matriz
        self.cliente = salvarClientes(self.matriz)
        self.rotas = []
        self.capacidadeVeiculo = capacidadeVeiculo
        self.veiculo = []
        self.soluçãoDistancias = []
        self.distanciaCaminhosSolução = 0

    def exibirVeiculos(self):
        for i in range(len(self.veiculo)):
            self.veiculo[i].status(self.capacidadeVeiculo)
            print('_'*50)

    def exibirRotas(self):
        print('     * Rotas')
        print(f'Distâncial total das rotas: {self.distanciaCaminhosSolução}')
        print('_'*50)
        for i in range(len(self.rotas)):
            self.rotas[i].exibirRota()
            print('_'*50)
    
    def statusDeposito(self): self.deposito.status()

    def statusCliente(self, posicao): self.cliente[posicao].status()
    
    def statusClientes(self):
        for i in range(len(self.cliente)):
            self.cliente[i].status()
            print('_'*50)
    
    def criarRotas(self):
        maxInteracoesNovo = len(self.cliente)
        maxEntrega = maxClientesEntrega(self.cliente, self.capacidadeVeiculo)
        teste = testeAtendimento(self.cliente)
        soluçãoCaminhos,soluçãoDistancias = [],[]
        distanciaCaminhosSolução = 40000000000000000
        maxInteracoes = 10
        contadorVeiculos = 0
        self.veiculo.append(Veiculo(contadorVeiculos, self.capacidadeVeiculo))
        for j in range(maxInteracoes):
            caminhos,distancias = [],[]
            self.cliente = salvarClientes(self.matriz)
            teste = testeAtendimento(self.cliente)
            while teste != False:
                caminho,distancia = soluçãoInicial(self.deposito, self.cliente, self.veiculo[contadorVeiculos], maxEntrega)
                testeClientesDisponiveis = verificarQuantClientesDiponiveis(self.cliente)
                if testeClientesDisponiveis > maxEntrega:
                    for i in range(maxInteracoesNovo):
                        novo = gerarNovo(caminho, self.cliente)
                        novoCaminho = adicionar(novo, self.deposito, caminho, self.cliente, self.veiculo[contadorVeiculos])
                        caminho, distancia = melhorCaminho(caminho, distancia, novoCaminho, self.deposito, self.cliente)
                caminhos.append(caminho)
                distancias.append(distancia)
                for i in range(1, len(caminho)-1):
                    self.cliente[caminho[i]-1].setDemanda(0)
                    self.cliente[caminho[i]-1].setStatusAtividade(False)
                teste = testeAtendimento(self.cliente)
            aux = 0
            for i in range(len(distancias)): aux += distancias[i]
            if aux < distanciaCaminhosSolução: 
                distanciaCaminhosSolução = aux
                soluçãoCaminhos = caminhos
                soluçãoDistancias = distancias
        retirarDeposito = 0
        self.veiculo = []
        for i in range(len(soluçãoCaminhos)):
            aux = 0
            self.veiculo.append(Veiculo(i+1, self.capacidadeVeiculo))
            for j in range(1, len(soluçãoCaminhos[i])-1):
                local = soluçãoCaminhos[i][j]
                aux += self.matriz[local-1][3]
            self.veiculo[i].setCapacidade(self.veiculo[i].getCapacidade()-aux)
            retirarDeposito += aux
        self.deposito.setQuantidadeProdutos(self.deposito.getQuantidadeProdutos() - retirarDeposito)
        self.rotas = salvarRotas(self.veiculo, soluçãoCaminhos, soluçãoDistancias)
        self.distanciaCaminhosSolução = distanciaCaminhosSolução
#******************************************
def salvarRotas(veiculo, rotas, custo):
    caminhos = []
    for i in range(len(rotas)): caminhos.append(Rota(veiculo[i].getNome(), rotas[i], custo[i]))
    return caminhos
#******************************************
def salvarClientes(matriz):
    cliente = []
    for i in range(len(matriz)): cliente.append(Cliente(matriz[i][0], matriz[i][1], matriz[i][2], matriz[i][3], True))
    return cliente
#******************************************
def maxClientesEntrega(cliente, capacidade):
    maxEntrega,aux = 0,0
    auxVetor = []
    for i in range(len(cliente)):
        if cliente[i].getStatusAtividade() == True: auxVetor.append(cliente[i].getDemanda())
    auxVetor = sorted(auxVetor)
    final = len(auxVetor) - 1
    for i in range(len(auxVetor)):
        aux += auxVetor[final-i]
        if aux > capacidade: return maxEntrega
        else: maxEntrega += 1
    return maxEntrega

def testeAtendimento(cliente):
    for i in range(len(cliente)):
        if cliente[i].getStatusAtividade() == True: return True
    return False
#******************************************
def soluçãoInicial(deposito, cliente, veiculo, maxEntrega):
    produtosSolução = veiculo.getCapacidade()+1
    while produtosSolução > veiculo.getCapacidade(): 
        solução = soluçãoRandom(maxEntrega, cliente)
        produtosSolução = quantProdutosSolução(solução, cliente)
    caminho = formarCaminho(solução)
    distancia = distanciaCaminho(caminho, deposito, cliente)
    return caminho, distancia

def soluçãoRandom(maxEntrega, cliente):
    clienteDisponivel,sorteados = [],[]
    for i in range(len(cliente)):
        if cliente[i].getStatusAtividade() == True: clienteDisponivel.append(cliente[i].getNome())
    shuffle(clienteDisponivel)
    if len(clienteDisponivel) <= maxEntrega: return clienteDisponivel
    else:
        for i in range(maxEntrega): sorteados.append(clienteDisponivel[i])
        return sorteados

def quantProdutosSolução(solução, cliente):
    produtosSolução = 0
    for i in range(len(solução)):
        for j in range(len(cliente)):
            if solução[i] == cliente[j].getNome(): produtosSolução += cliente[j].getDemanda()
    return produtosSolução

def formarCaminho(solução):
    caminho = [0]
    for i in range(len(solução)): caminho.append(solução[i])
    caminho.append(caminho[0])
    return caminho

def distanciaCaminho(caminho, deposito, cliente):
    distancia = 0
    for i in range(len(caminho)-1):
        if i == 0: distancia += calcularDistancia(deposito.getCoordenadaX(), deposito.getCoordenadaY(), cliente[caminho[1]-1].getCoordenadaX(), cliente[caminho[1]-1].getCoordenadaY())
        elif i == len(caminho)-2: distancia += calcularDistancia(cliente[caminho[i]-1].getCoordenadaX(), cliente[caminho[i]-1].getCoordenadaY(), deposito.getCoordenadaX(), deposito.getCoordenadaY())
        else: distancia += calcularDistancia(cliente[caminho[i]-1].getCoordenadaX(), cliente[caminho[i]-1].getCoordenadaY(), cliente[caminho[i+1]-1].getCoordenadaX(), cliente[caminho[i+1]-1].getCoordenadaY())
    return distancia

def calcularDistancia(x1, x2, y1, y2):
    x = [x1, x2]
    y = [y1, y2]
    return euclidiana(x, y)

def euclidiana(x, y): return sqrt(pow(x[0]-y[0],2)+pow(x[1]-y[1],2))
    
def coordenada(vetor): return vetor[1], vetor[2]
#******************************************
def verificarQuantClientesDiponiveis(cliente):
    contador = 0
    for i in range(len(cliente)):
        if cliente[i].getStatusAtividade() == True: contador += 1
    return contador
#******************************************
def gerarNovo(caminho, clientes):
    teste = True
    novo = randint(1, len(clientes))
    while teste == True:
        teste = checar(novo, caminho, clientes)
        if teste == True: novo = randint(1, len(clientes))
    return novo

def checar(novo, solução, clientes):
    teste = False
    if clientes[novo-1].getStatusAtividade() == False: return True
    for i in range(len(solução)):
        if novo == solução[i]: return True
    return teste
#******************************************
def adicionar(novo, deposito, caminho, cliente, veiculo):
    novoCaminho = gerarVetor(caminho)
    teste = verificarMenor(cliente[novo-1].getCoordenadaX(), cliente[novo-1].getCoordenadaY(), deposito.getCoordenadaX(), deposito.getCoordenadaY(), cliente[novoCaminho[1]-1].getCoordenadaX(), cliente[novoCaminho[1]-1].getCoordenadaY())
    if teste == False:
        for i in range(2, len(novoCaminho)-1):
            teste = verificarMenor(cliente[novo-1].getCoordenadaX(), cliente[novo-1].getCoordenadaY(), cliente[novoCaminho[i-1]-1].getCoordenadaX(), cliente[novoCaminho[i-1]-1].getCoordenadaY(), cliente[novoCaminho[i]-1].getCoordenadaX(), cliente[novoCaminho[i]-1].getCoordenadaY())
            if teste == True:
                novoCaminho[i] = novo
                return novoCaminho
        return caminho
    else: 
        novoCaminho[1] = novo
        return novoCaminho

def gerarVetor(caminho):
    vetor = []
    for i in range(len(caminho)): vetor.append(caminho[i])
    return vetor

def verificarMenor(z1, z2, x1, x2, y1, y2):
    x = [x1, x2]
    y = [y1, y2]
    z = [z1, z2]
    distancia1 = euclidiana(x, y)
    distancia2 = euclidiana(x, z)
    if distancia1 <= distancia2: return False
    else: return True
#******************************************
def melhorCaminho(caminho, distancia, novoCaminho, deposito, cliente):
    novaDistancia = distanciaCaminho(novoCaminho, deposito, cliente)
    if novaDistancia < distancia: return novoCaminho, novaDistancia
    else: return caminho, distancia