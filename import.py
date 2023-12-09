import random
import matplotlib.pyplot as plt
import numpy as np

# Definindo as classes Usuário e Motorista

class Usuario:
    def __init__(self, id, nome, localizacao_atual):
        self.id = id
        self.nome = nome
        self.localizacao_atual = localizacao_atual
        self.historico_viagens = []

class Motorista:
    def __init__(self, id_motorista, nome, localizacao_atual, local_casa, avaliacao_inicial, tempo_locomocao):
        self.id_motorista = id_motorista
        self.localizacao_atual = localizacao_atual
        self.nome = nome
        self.historico_corridas = []
        self.pontos_avaliacao = avaliacao_inicial
        self.tempo_locomocao = tempo_locomocao
        self.local_casa = local_casa
        self.tempo_disponibilidade = random.randint(1, 24)  # Tempo de disponibilidade aleatório

# Criando um usuário
usuario = Usuario(1, "Usuário 1", (random.randint(0, 100), random.randint(0, 100)))

# Criando 10 motoristas com atributos aleatórios
motoristas = [Motorista(i, f"Motorista {i}", (random.randint(0, 100), random.randint(0, 100)), (random.randint(0, 100), random.randint(0, 100)), 
                        random.uniform(3, 5), random.uniform(20, 60)) for i in range(1, 11)]

(usuario, motoristas[0].__dict__)  # Exibindo o usuário e o primeiro motorista para verificação

# ---------------------------------------------------------------------------------------------

def calcular_distancia(ponto1, ponto2):
    """
    Calcula a distância euclidiana entre dois pontos no plano cartesiano.
    """
    return np.sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)

# Definindo um destino aleatório para a viagem do usuário
destino = (random.randint(0, 100), random.randint(0, 100))

# Função para encontrar o melhor motorista
def encontrar_melhor_motorista(motoristas, usuario, destino):
    melhor_pontuacao = float('-inf')
    melhor_motorista = None

    for motorista in motoristas:
        distancia_usuario_destino = calcular_distancia(usuario.localizacao_atual, destino)
        distancia_motorista_usuario = calcular_distancia(motorista.localizacao_atual, usuario.localizacao_atual)
        distancia_destino_casa_motorista = calcular_distancia(destino, motorista.local_casa)

        pontuacao = distancia_usuario_destino - (distancia_motorista_usuario + distancia_destino_casa_motorista)

        # Verificar se este motorista é melhor ou igual ao atual melhor
        if pontuacao > melhor_pontuacao or (
            pontuacao == melhor_pontuacao and 
            (motorista.tempo_locomocao < melhor_motorista.tempo_locomocao or 
             motorista.pontos_avaliacao > melhor_motorista.pontos_avaliacao)):

            melhor_pontuacao = pontuacao
            melhor_motorista = motorista

    return melhor_motorista

# Encontrando o melhor motorista
melhor_motorista = encontrar_melhor_motorista(motoristas, usuario, destino)
melhor_motorista.__dict__, destino  # Exibindo os detalhes do melhor motorista e o destino

# ---------------------------------------------------------------------------------------------

# Atualizando a plotagem para incluir o ponto de destino

# Configurando a plotagem novamente
plt.figure(figsize=(10, 10))
ax = plt.gca()

# Plotando a localização de todos os motoristas
for motorista in motoristas:
    ax.plot(*motorista.localizacao_atual, 'bo')  # pontos azuis
    ax.text(*motorista.localizacao_atual, f'M{motorista.id_motorista}', color='blue', fontsize=8)

# Plotando a localização do usuário
ax.plot(*usuario.localizacao_atual, 'ro')  # ponto vermelho
ax.text(*usuario.localizacao_atual, 'Usuário', color='red', fontsize=10)

# Plotando a casa do motorista escolhido
ax.plot(*melhor_motorista.local_casa, 'go')  # ponto verde
ax.text(*melhor_motorista.local_casa, 'Casa Motorista', color='green', fontsize=10)

# Plotando o destino
ax.plot(*destino, 'yo')  # ponto amarelo
ax.text(*destino, 'D', color='yellow', fontsize=12)

# Linhas representando a viagem
# Linha entre o motorista escolhido e o usuário
ax.plot([melhor_motorista.localizacao_atual[0], usuario.localizacao_atual[0]], 
        [melhor_motorista.localizacao_atual[1], usuario.localizacao_atual[1]], 'k--')

# Linha entre o usuário e o destino
ax.plot([usuario.localizacao_atual[0], destino[0]], 
        [usuario.localizacao_atual[1], destino[1]], 'k--')

# Linha entre o destino e a casa do motorista
ax.plot([destino[0], melhor_motorista.local_casa[0]], 
        [destino[1], melhor_motorista.local_casa[1]], 'k--')

plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title('Simulação de Seleção de Motorista com Destino')
plt.grid(True)
plt.show()
