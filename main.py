# Super Trunfo - Attack on Titan
# Atributos: Ataque, Defesa, Velocidade, Regeneração, Estratégia (escala 0-10)
# Super Trunfo: Titã Fundador
# Trunfo couter: Capitão Levi Ackerman

import random

from exibicao import (
    exibir_carta,
    introducao,
    inicio_rodada,
    selecionar_atributo_carta,
    resultado_rodada,
    fim_de_jogo,
    atributos,
)

# Os 5 atributos ocupam as posições 3 a 7 de cada carta
# [nome, super_trunfo, counter, ataque, defesa, velocidade, regeneração, estratégia]
INDICE_PRIMEIRO_ATRIBUTO = 3

# [nome, super_trunfo, counter, ataque, defesa, velocidade, regeneração, estratégia]
cartas = [
    ["Titã Fundador",                       True,  False, 10, 10,  8, 10,  8],
    ["Titã de Ataque (Eren Yeager)",        False, False, 10,  8,  9,  9,  7],
    ["Titã Colossal (Bertholdt Hoover)",    False, False,  9,  7,  2,  6,  3],
    ["Titã Blindado (Reiner Braun)",        False, False,  7, 10,  5,  5,  4],
    ["Titã Fêmea (Annie Leonhart)",         False, False,  8,  8,  7,  7,  8],
    ["Titã Bestial (Zeke Yeager)",          False, False,  8,  6,  5,  6,  9],
    ["Titã Mandíbula (Porco Galliard)",     False, False,  5,  3, 10,  7,  4],
    ["Titã Carroceiro (Pieck Finger)",      False, False,  2,  4,  8,  5,  6],
    ["Titã Martelo de Guerra (Lara Tybur)", False, False,  9,  9,  3,  6,  6],
    ["Capitão Levi",                        False, True,   9,  5, 10,  1,  8],
    ["Mikasa Ackerman",                     False, False,  8,  4,  9,  1,  7],
    ["Erwin Smith",                         False, False,  4,  2,  6,  0, 10],
]

def embaralhar_cartas(cartas):
    random.shuffle(cartas)
    return cartas

def dividir_cartas(cartas):
    return cartas[:len(cartas)//2], cartas[len(cartas)//2:]

def dar_cartas():
    cartas_embaralhadas = embaralhar_cartas(cartas)
    cartas_jogador, cartas_cpu = dividir_cartas(cartas_embaralhadas)
    return cartas_jogador, cartas_cpu

def modo_de_jogo():
    print("Escolha o modo de jogo:")
    print("1 - Jogador vs CPU")
    print("2 - Jogador vs Jogador")
    escolha = input("Digite 1 ou 2: ")
    while escolha not in ["1", "2"]:
        escolha = input("Entrada inválida. Digite 1 ou 2: ")
    return escolha

def escolher_atributo_jogador(carta):
    """O jogador escolhe o atributo direto na própria carta.

    Use as setas ↑/↓ para mover a seleção e ENTER para confirmar.
    """
    print("\nSua carta — escolha o atributo para disputar:")
    return selecionar_atributo_carta(carta)

def escolher_atributo_cpu(carta_cpu):
    """A CPU escolhe o atributo em que a sua carta é mais forte."""
    valores = carta_cpu[INDICE_PRIMEIRO_ATRIBUTO:]
    melhor = valores.index(max(valores))
    print(f"\nA CPU escolheu o atributo: {atributos[melhor].capitalize()}")
    return INDICE_PRIMEIRO_ATRIBUTO + melhor

def comparar_cartas(carta_a, carta_b, indice_atributo):
    """
    Compara duas cartas e devolve (vencedor, motivo).
    vencedor: 'a', 'b' ou 'empate'.
    """
    # Regra especial: o counter (Capitão Levi) derruba o Super Trunfo
    if carta_a[1] and carta_b[2]:
        return "b", "O counter (Capitão Levi) derruba o Super Trunfo!"
    if carta_b[1] and carta_a[2]:
        return "a", "O counter (Capitão Levi) derruba o Super Trunfo!"

    # Regra especial: o Super Trunfo vence qualquer outra carta
    if carta_a[1]:
        return "a", "Super Trunfo vence automaticamente!"
    if carta_b[1]:
        return "b", "Super Trunfo vence automaticamente!"

    # Comparação normal pelo atributo escolhido
    valor_a = carta_a[indice_atributo]
    valor_b = carta_b[indice_atributo]
    if valor_a > valor_b:
        return "a", ""
    if valor_b > valor_a:
        return "b", ""
    return "empate", ""

def single_player():
    # Passo 1: embaralhar e dividir as cartas entre jogador e CPU
    cartas_jogador, cartas_cpu = dar_cartas()

    mesa = []              # cartas acumuladas quando uma rodada empata
    vez_do_jogador = True  # na 1ª rodada quem escolhe o atributo é o jogador
    rodada = 1
    MAX_RODADAS = 100      # trava de segurança contra partidas infinitas

    # Passo 2: jogar rodadas enquanto os dois jogadores tiverem cartas
    while cartas_jogador and cartas_cpu and rodada <= MAX_RODADAS:
        inicio_rodada(rodada, len(cartas_jogador), len(cartas_cpu))

        # Passo 3: cada jogador vira a carta do topo da sua pilha
        carta_jogador = cartas_jogador.pop(0)
        carta_cpu = cartas_cpu.pop(0)

        # Passo 4 e 5: quem tem a vez escolhe o atributo (carta da CPU escondida)
        if vez_do_jogador:
            indice = escolher_atributo_jogador(carta_jogador)
        else:
            print("\nSua carta:")
            exibir_carta(carta_jogador)
            print("\nÉ a vez da CPU escolher o atributo...")
            indice = escolher_atributo_cpu(carta_cpu)

        # Passo 6: revelar a carta da CPU
        print("\nCarta da CPU:")
        exibir_carta(carta_cpu, inimiga=True)

        # Passo 7: comparar as cartas pelo atributo escolhido
        nome_atributo = atributos[indice - INDICE_PRIMEIRO_ATRIBUTO].capitalize()
        print(f"\nAtributo disputado: {nome_atributo}")
        print(f"  Você: {carta_jogador[indice]}  x  CPU: {carta_cpu[indice]}")

        resultado, motivo = comparar_cartas(carta_jogador, carta_cpu, indice)
        if motivo:
            print(f"  {motivo}")

        # Passo 8: distribuir as cartas conforme o resultado
        if resultado == "a":
            resultado_rodada("jogador")
            cartas_jogador.append(carta_jogador)
            cartas_jogador.append(carta_cpu)
            cartas_jogador.extend(mesa)  # leva também o que estava na mesa
            mesa = []
            vez_do_jogador = True        # o vencedor escolhe na próxima rodada
        elif resultado == "b":
            resultado_rodada("cpu")
            cartas_cpu.append(carta_cpu)
            cartas_cpu.append(carta_jogador)
            cartas_cpu.extend(mesa)
            mesa = []
            vez_do_jogador = False
        else:
            resultado_rodada("empate")
            mesa.append(carta_jogador)
            mesa.append(carta_cpu)       # a vez continua com quem escolheu

        rodada += 1
        input("\nPressione ENTER para a próxima rodada...")

    # Passo 9: anunciar o vencedor da partida
    if not cartas_jogador:
        fim_de_jogo("cpu", "A CPU conquistou todas as cartas.")
    elif not cartas_cpu:
        fim_de_jogo("jogador", "Você conquistou todas as cartas!")
    elif len(cartas_jogador) > len(cartas_cpu):
        fim_de_jogo("jogador", "Limite de rodadas atingido — você ficou com mais cartas.")
    elif len(cartas_cpu) > len(cartas_jogador):
        fim_de_jogo("cpu", "Limite de rodadas atingido — a CPU ficou com mais cartas.")
    else:
        fim_de_jogo("empate", "Limite de rodadas atingido com o placar empatado.")


def multiplayer():
    cartas_jogador1, cartas_jogador2 = dar_cartas()
    # Lógica do jogo para jogador vs jogador
    
def jogar():
    introducao()
    modo = modo_de_jogo()
    
    if modo == "1":
        single_player()
    else:
        multiplayer()


jogar()

