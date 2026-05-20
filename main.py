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
    ["Titã de Ataque (Eren Yeager)",        False, False, 10,  7,  8, 10,  7],
    ["Titã Colossal (Bertholdt Hoover)",    False, False, 10,  8,  2,  4,  4],
    ["Titã Blindado (Reiner Braun)",        False, False,  7, 10,  6,  8,  4],
    ["Titã Fêmea (Annie Leonhart)",         False, False,  8,  8,  8,  8,  9],
    ["Titã Bestial (Zeke Yeager)",          False, False,  8,  6,  5,  7,  9],
    ["Titã Mandíbula (Porco Galliard)",     False, False,  8,  3, 10,  7,  4],
    ["Titã Carroceiro (Pieck Finger)",      False, False,  2,  6,  9,  5,  8],
    ["Titã Martelo de Guerra (Lara Tybur)", False, False,  9,  9,  5,  6,  5],
    ["Capitão Levi",                        False, True,  10,  5, 10,  1,  8],
    ["Mikasa Ackerman",                     False, False,  9,  4,  9,  1,  7],
    ["Erwin Smith",                         False, False,  4,  2,  6,  1, 10],
]


# --------------------------------------------------------------------------
# Preparação das cartas
# --------------------------------------------------------------------------
def embaralhar_cartas(cartas):
    random.shuffle(cartas)
    return cartas

def dividir_cartas(cartas):
    return cartas[:len(cartas)//2], cartas[len(cartas)//2:]

def dar_cartas():
    """Embaralha o baralho e devolve dois montes iguais."""
    cartas_embaralhadas = embaralhar_cartas(cartas)
    return dividir_cartas(cartas_embaralhadas)


# --------------------------------------------------------------------------
# Jogadores
# --------------------------------------------------------------------------
def criar_jogador(nome, deck, humano=True):
    """Cria um jogador: nome, a sua pilha de cartas e se é humano ou CPU."""
    return {"nome": nome, "deck": deck, "humano": humano}


# --------------------------------------------------------------------------
# Escolha de atributo
# --------------------------------------------------------------------------
def escolher_atributo_jogador(carta, nome="Você", inimiga=False):
    """Mostra a carta e deixa um jogador humano escolher o atributo.

    Use as setas ↑/↓ para mover a seleção e ENTER para confirmar.
    Devolve o índice (3 a 7) do atributo escolhido.
    """
    print(f"\n{nome} — escolha o atributo na sua carta:")
    return selecionar_atributo_carta(carta, inimiga=inimiga)

def escolher_atributo_cpu(carta):
    """A CPU escolhe o atributo em que a sua carta é mais forte."""
    valores = carta[INDICE_PRIMEIRO_ATRIBUTO:]
    melhor = valores.index(max(valores))
    print(f"\nA CPU escolheu o atributo: {atributos[melhor].capitalize()}")
    return INDICE_PRIMEIRO_ATRIBUTO + melhor

def escolher_atributo(jogador, carta, inimiga=False):
    """Pede o atributo da rodada ao jogador (humano ou CPU) e devolve o índice."""
    if jogador["humano"]:
        return escolher_atributo_jogador(carta, jogador["nome"], inimiga=inimiga)
    return escolher_atributo_cpu(carta)


# --------------------------------------------------------------------------
# Regras da disputa
# --------------------------------------------------------------------------
def comparar_cartas(carta_a, carta_b, indice_atributo):
    """Compara duas cartas e devolve (vencedor, motivo).

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


# --------------------------------------------------------------------------
# Fluxo da partida (reutilizável por single player e multiplayer)
# --------------------------------------------------------------------------
def jogar_rodada(jog_a, jog_b, mesa, escolhe_a):
    """Joga uma rodada completa entre dois jogadores.

    jog_a, jog_b : dicionários de jogador -> {"nome", "deck", "humano"}
    mesa         : cartas acumuladas de empates anteriores
    escolhe_a    : True se quem escolhe o atributo nesta rodada é jog_a

    Distribui as cartas (atualiza os decks) e devolve (vencedor, nova_mesa),
    onde vencedor é jog_a, jog_b ou None em caso de empate.
    """
    # Passo 1: cada jogador vira a carta do topo da sua pilha
    carta_a = jog_a["deck"].pop(0)
    carta_b = jog_b["deck"].pop(0)

    # Passo 2: define quem escolhe o atributo e quem só revela a carta
    if escolhe_a:
        ativo, carta_ativo = jog_a, carta_a
        outro, carta_outro = jog_b, carta_b
    else:
        ativo, carta_ativo = jog_b, carta_b
        outro, carta_outro = jog_a, carta_a

    # Passo 3: o jogador da vez escolhe o atributo.
    #   - humano: a carta já aparece dentro da própria seleção
    #   - CPU: a carta precisa ser exibida à parte
    if not ativo["humano"]:
        print(f"\nCarta de {ativo['nome']}:")
        exibir_carta(carta_ativo, inimiga=(ativo is jog_b))
    indice = escolher_atributo(ativo, carta_ativo, inimiga=(ativo is jog_b))

    # Passo 4: revelar a carta do outro jogador
    print(f"\nCarta de {outro['nome']}:")
    exibir_carta(carta_outro, inimiga=(outro is jog_b))

    # Passo 5: comparar as cartas pelo atributo escolhido
    nome_atributo = atributos[indice - INDICE_PRIMEIRO_ATRIBUTO].capitalize()
    print(f"\nAtributo disputado: {nome_atributo}")
    print(f"  {jog_a['nome']}: {carta_a[indice]}  x  {jog_b['nome']}: {carta_b[indice]}")

    resultado, motivo = comparar_cartas(carta_a, carta_b, indice)
    if motivo:
        print(f"  {motivo}")

    # Passo 6: distribuir as cartas conforme o resultado
    if resultado == "a":
        resultado_rodada(jog_a["nome"], derrota=not jog_a["humano"])
        jog_a["deck"].extend([carta_a, carta_b, *mesa])
        return jog_a, []
    if resultado == "b":
        resultado_rodada(jog_b["nome"], derrota=not jog_b["humano"])
        jog_b["deck"].extend([carta_b, carta_a, *mesa])
        return jog_b, []
    # empate: as cartas vão para a mesa e ficam para o próximo vencedor
    resultado_rodada()
    return None, mesa + [carta_a, carta_b]

def anunciar_vencedor(jog_a, jog_b):
    """Mostra a tela de fim de jogo a partir do tamanho dos decks."""
    deck_a, deck_b = jog_a["deck"], jog_b["deck"]

    if not deck_a:
        vencedor, motivo = jog_b, f"{jog_b['nome']} conquistou todas as cartas."
    elif not deck_b:
        vencedor, motivo = jog_a, f"{jog_a['nome']} conquistou todas as cartas."
    elif len(deck_a) > len(deck_b):
        vencedor, motivo = jog_a, "Limite de rodadas atingido — terminou com mais cartas."
    elif len(deck_b) > len(deck_a):
        vencedor, motivo = jog_b, "Limite de rodadas atingido — terminou com mais cartas."
    else:
        vencedor, motivo = None, "Limite de rodadas atingido com o placar empatado."

    if vencedor is None:
        fim_de_jogo(None, motivo)
    else:
        fim_de_jogo(vencedor["nome"], motivo, derrota=not vencedor["humano"])

def partida(jog_a, jog_b, max_rodadas=100):
    """Roda uma partida completa entre dois jogadores até alguém ficar sem cartas.

    Serve tanto para Jogador vs CPU quanto para Jogador vs Jogador: basta
    montar os dois jogadores com criar_jogador() e chamar esta função.
    """
    mesa = []              # cartas acumuladas quando uma rodada empata
    escolhe_a = True       # na 1ª rodada quem escolhe o atributo é jog_a
    rodada = 1

    while jog_a["deck"] and jog_b["deck"] and rodada <= max_rodadas:
        inicio_rodada(rodada, len(jog_a["deck"]), len(jog_b["deck"]))

        vencedor, mesa = jogar_rodada(jog_a, jog_b, mesa, escolhe_a)
        if vencedor is jog_a:
            escolhe_a = True       # o vencedor escolhe na próxima rodada
        elif vencedor is jog_b:
            escolhe_a = False
        # empate: quem escolheu continua escolhendo (escolhe_a inalterado)

        rodada += 1
        input("\nPressione ENTER para a próxima rodada...")

    anunciar_vencedor(jog_a, jog_b)


# --------------------------------------------------------------------------
# Modos de jogo
# --------------------------------------------------------------------------
def modo_de_jogo():
    print("Escolha o modo de jogo:")
    print("1 - Jogador vs CPU")
    print("2 - Jogador vs Jogador")
    escolha = input("Digite 1 ou 2: ")
    while escolha not in ["1", "2"]:
        escolha = input("Entrada inválida. Digite 1 ou 2: ")
    return escolha

def single_player():
    deck_jogador, deck_cpu = dar_cartas()
    jogador = criar_jogador("Você", deck_jogador, humano=True)
    cpu = criar_jogador("CPU", deck_cpu, humano=False)
    partida(jogador, cpu)

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


# só inicia o jogo quando este arquivo é executado diretamente;
# assim outros módulos podem importar as funções sem disparar a partida
if __name__ == "__main__":
    jogar()
