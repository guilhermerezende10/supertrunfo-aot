# Super Trunfo - Attack on Titan
# Atributos: Ataque, Defesa, Velocidade, Regeneração, Estratégia (escala 0-10)
# Super Trunfo: Titã Fundador

import random

from exibicao import exibir_carta, introducao

cartas = [
    ["Titã Fundador",          True,  10, 10,  8, 10, 8],
    ["Titã de Ataque (Éren)",  False, 10,  8,  9,  9,  7],
    ["Titã Colossal",          False,  9,  7,  2,  6,  3],
    ["Titã Blindado",          False,  7, 10,  5,  5,  4],
    ["Titã Fêmea",             False,  8,  8,  7,  7,  8],
    ["Titã Bestial",           False,  8,  6,  5,  6,  9],
    ["Titã Mandíbula",         False,  5,  3, 10,  7,  4],
    ["Titã Carroceiro",        False,  2,  4,  8,  5,  6],
    ["Titã Martelo de Guerra", False,  9,  9,  3,  6,  6],
    ["Capitão Levi",           False,  9,  5, 10,  1,  8],
    ["Mikasa Ackerman",        False,  8,  4,  9,  1,  7],
    ["Erwin Smith",            False,  4,  2,  6,  0, 10],
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

def single_player():
    cartas_jogador, cartas_cpu = dar_cartas()
    # Lógica do jogo para jogador vs CPU
    
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

