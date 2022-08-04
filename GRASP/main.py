from grasp import GRASP

capacidade = 4
veiculo = ['', capacidade]
#clientes = [id, coordenada1, coordenada2, demanda, atividade]
matriz =   [[1, 1, 1, 2],
            [2, 2, 2, 2],
            [3, 3, 3, 2],
            [4, 4, 4, 1],
            [5, 5, 5, 2],
            [6, 6, 6, 1],
            [7, 7, 7, 1]]
#deposito = [id, coordenada1, coordenada2, quantidadeProdutos, atividade]
deposito = [0, 0, 0, 20] 

viagem = GRASP(matriz, deposito, capacidade)
viagem.criarRotas()
viagem.exibirRotas()