import os
import sys

WINDOWS = os.name == "nt"

if WINDOWS:
    import ctypes
    import msvcrt
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

RESET   = "\033[0m"
BOLD    = "\033[1m"
REVERSE = "\033[7m"
GOLD    = "\033[38;5;220m"
CYAN    = "\033[38;5;45m"
GREEN   = "\033[38;5;46m"
YELLOW  = "\033[38;5;226m"
RED     = "\033[38;5;196m"
GRAY    = "\033[38;5;240m"
DARKBLUE  = "\033[38;5;19m"

atributos = ["ataque", "defesa", "velocidade", "regeneração", "estratégia"]


def _linha_caixa(texto, largura, cor_borda, cor_texto="", negrito=True):
    """Monta uma linha de caixa com o texto centralizado.

    O `texto` deve vir sem códigos de cor, porque o alinhamento é calculado
    a partir do seu tamanho visível.
    """
    pad_esq = (largura - len(texto)) // 2
    pad_dir = largura - len(texto) - pad_esq
    estilo = f"{BOLD if negrito else ''}{cor_texto}"
    return (
        f"{cor_borda}║{RESET}{' ' * pad_esq}"
        f"{estilo}{texto}{RESET}"
        f"{' ' * pad_dir}{cor_borda}║{RESET}"
    )


def introducao():
    titulo = "SUPER TRUNFO — ATTACK ON TITAN"
    largura = 64
    pad_esq = (largura - len(titulo)) // 2
    pad_dir = largura - len(titulo) - pad_esq

    print(f"{GOLD}╔{'═' * largura}╗{RESET}")
    print(f"{GOLD}║{' ' * pad_esq}{BOLD}{titulo}{RESET}{' ' * pad_dir}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * largura}╝{RESET}")
    print()
    print(f"{CYAN}  Cada carta representa um personagem ou titã da série Attack on Titan.{RESET}")
    print(f"{CYAN}  Os atributos são:{RESET} {RED}Ataque{RESET}, {YELLOW}Defesa{RESET}, {DARKBLUE}Velocidade{RESET}, {GREEN}Regeneração{RESET} e {GRAY}Estratégia{RESET}.")
    print(f"{CYAN}  Escolha um atributo mais forte que o do adversário para vencer a rodada.{RESET}")
    print(f"{CYAN}  O Titã Fundador é o Super Trunfo e vence quase qualquer carta.{RESET}")
    print()
    print(f"{BOLD}{GOLD}                  >> Vamos começar a jogar! <<{RESET}")
    print()


def inicio_rodada(numero, total_jogador, total_cpu):
    """Cabeçalho de início de rodada, no mesmo estilo de caixa do título."""
    largura = 64
    titulo = f"RODADA {numero}"

    # versão sem cores: usada só para calcular o alinhamento da linha
    placar = f"Você: {total_jogador} cartas      CPU: {total_cpu} cartas"
    placar_colorido = (
        f"{CYAN}Você: {BOLD}{total_jogador}{RESET}{CYAN} cartas{RESET}"
        f"      "
        f"{RED}CPU: {BOLD}{total_cpu}{RESET}{RED} cartas{RESET}"
    )
    pad_esq = (largura - len(placar)) // 2
    pad_dir = largura - len(placar) - pad_esq

    print()
    print(f"{GOLD}╔{'═' * largura}╗{RESET}")
    print(_linha_caixa(titulo, largura, GOLD, GOLD))
    print(f"{GOLD}╠{'═' * largura}╣{RESET}")
    print(f"{GOLD}║{RESET}{' ' * pad_esq}{placar_colorido}{' ' * pad_dir}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * largura}╝{RESET}")
    print()


def _cor_valor(v):
    if v >= 8:
        return GREEN
    if v >= 5:
        return YELLOW
    return RED


def _linhas_carta(carta, inimiga=False, indice_selecionado=None,
                  numerado=False, rodape=None, cor_rodape=GRAY):
    """Monta a carta como uma lista de linhas prontas para imprimir.

    - inimiga: borda e detalhes em vermelho.
    - indice_selecionado: índice (3-7) do atributo destacado como selecionado.
    - numerado: numera os atributos de 1 a 5 (usado no modo de digitação).
    - rodape: texto opcional mostrado dentro da carta, antes da borda inferior.
    """
    nome = carta[0]
    super_trunfo = carta[1]

    # o adversário é sempre mostrado em vermelho para se diferenciar da sua carta
    if inimiga:
        cor_borda = RED
    elif super_trunfo:
        cor_borda = GOLD
    else:
        cor_borda = CYAN
    marcador = "★" if super_trunfo else "◆"
    largura = 40

    linhas = [f"{cor_borda}╔{'═' * largura}╗{RESET}"]
    linhas.append(_linha_caixa(f"{marcador} {nome} {marcador}", largura, cor_borda, cor_borda))
    if inimiga:
        linhas.append(_linha_caixa("▼ CARTA DA CPU ▼", largura, cor_borda, RED))
    if super_trunfo:
        linhas.append(_linha_caixa("SUPER TRUNFO", largura, cor_borda, GOLD))
    linhas.append(f"{cor_borda}╠{'═' * largura}╣{RESET}")

    for posicao, i in enumerate(range(3, 8)):
        rotulo = atributos[i - 3].capitalize()
        valor = carta[i]
        cor = _cor_valor(valor)
        falta = largura - 30   # a parte visível da linha ocupa 30 colunas

        if i == indice_selecionado:
            # linha destacada: barra de seleção em vídeo reverso
            barra = "█" * valor + "░" * (10 - valor)
            texto = f"▶ {rotulo:<12} {barra} {valor:>2}  " + " " * falta
            linhas.append(
                f"{cor_borda}║{RESET}{REVERSE}{BOLD}{cor_borda}{texto}{RESET}"
                f"{cor_borda}║{RESET}"
            )
        else:
            # número (modo digitação) ou dois espaços (linha comum)
            prefixo = f"{BOLD}{GOLD}{posicao + 1}{RESET} " if numerado else "  "
            conteudo = (
                f"{prefixo}{BOLD}{rotulo:<12}{RESET} "
                f"{cor}{'█' * valor}{GRAY}{'░' * (10 - valor)}{RESET} "
                f"{BOLD}{cor}{valor:>2}{RESET}  "
            )
            linhas.append(
                f"{cor_borda}║{RESET}{conteudo}{' ' * falta}{cor_borda}║{RESET}"
            )

    if rodape is not None:
        linhas.append(f"{cor_borda}╠{'═' * largura}╣{RESET}")
        linhas.append(_linha_caixa(rodape, largura, cor_borda, cor_rodape, negrito=False))
    linhas.append(f"{cor_borda}╚{'═' * largura}╝{RESET}")
    return linhas


def exibir_carta(carta, inimiga=False):
    """Imprime a carta no terminal."""
    for linha in _linhas_carta(carta, inimiga=inimiga):
        print(linha)


def _ler_tecla():
    """Lê uma tecla do teclado e devolve 'cima', 'baixo', 'enter' ou None."""
    if WINDOWS:
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):          # prefixo de tecla especial (setas)
            return {b"H": "cima", b"P": "baixo"}.get(msvcrt.getch())
        if ch in (b"\r", b"\n"):
            return "enter"
        if ch == b"\x03":                      # Ctrl+C
            raise KeyboardInterrupt
        return None

    # POSIX (Linux / macOS)
    import termios
    import tty
    fd = sys.stdin.fileno()
    estado = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":                       # início de sequência de escape
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, estado)
    if ch == "\x1b[A":
        return "cima"
    if ch == "\x1b[B":
        return "baixo"
    if ch in ("\r", "\n"):
        return "enter"
    if ch == "\x03":
        raise KeyboardInterrupt
    return None


def _selecionar_atributo_numerico(carta):
    """Escolha de atributo por digitação (terminais sem leitura de setas)."""
    for linha in _linhas_carta(carta, numerado=True):
        print(linha)

    total = len(atributos)
    opcoes = [str(n) for n in range(1, total + 1)]
    escolha = input(f"\nDigite o número do atributo (1-{total}): ")
    while escolha not in opcoes:
        escolha = input(f"Entrada inválida. Digite de 1 a {total}: ")
    return 3 + int(escolha) - 1


def selecionar_atributo_carta(carta):
    """Mostra a carta e deixa o jogador escolher o atributo direto nela.

    Use ↑/↓ para mover a seleção e ENTER para confirmar. Devolve o índice
    (3 a 7) do atributo escolhido. Se o terminal não suportar leitura de
    teclas, recorre ao menu numérico.
    """
    primeiro = 3
    total = len(atributos)

    try:
        interativo = sys.stdin.isatty()
    except (OSError, ValueError):
        interativo = False
    if not interativo:
        return _selecionar_atributo_numerico(carta)

    selecao = 0
    try:
        primeira_vez = True
        while True:
            linhas = _linhas_carta(
                carta,
                indice_selecionado=primeiro + selecao,
                rodape="↑/↓ mover  •  ENTER confirmar",
            )
            if not primeira_vez:
                print(f"\033[{len(linhas)}A", end="")   # volta ao topo da carta
            for linha in linhas:
                print(f"\033[2K{linha}")                 # limpa e redesenha a linha
            primeira_vez = False

            tecla = _ler_tecla()
            if tecla == "cima":
                selecao = (selecao - 1) % total
            elif tecla == "baixo":
                selecao = (selecao + 1) % total
            elif tecla == "enter":
                # redesenha uma última vez, confirmando a escolha
                print(f"\033[{len(linhas)}A", end="")
                for linha in _linhas_carta(
                    carta,
                    indice_selecionado=primeiro + selecao,
                    rodape="✔ atributo escolhido",
                    cor_rodape=GREEN,
                ):
                    print(f"\033[2K{linha}")
                return primeiro + selecao
    except OSError:
        # o terminal não permitiu a leitura direta de teclas
        return _selecionar_atributo_numerico(carta)


def resultado_rodada(vencedor):
    """Mostra o resultado da rodada numa faixa destacada.

    vencedor: 'jogador', 'cpu' ou 'empate'.
    """
    largura = 64

    if vencedor == "jogador":
        cor = GREEN
        texto = "★  VOCÊ VENCEU A RODADA!  ★"
    elif vencedor == "cpu":
        cor = RED
        texto = "✖  A CPU VENCEU A RODADA  ✖"
    else:
        cor = GRAY
        texto = "◆  EMPATE — AS CARTAS VÃO PARA A MESA  ◆"

    print()
    print(f"{cor}╔{'═' * largura}╗{RESET}")
    print(_linha_caixa(texto, largura, cor, cor))
    print(f"{cor}╚{'═' * largura}╝{RESET}")


def fim_de_jogo(resultado, motivo=""):
    """Tela de encerramento da partida.

    resultado: 'jogador', 'cpu' ou 'empate'.
    motivo: linha opcional explicando como a partida terminou.
    """
    largura = 64

    if resultado == "jogador":
        cor = GOLD
        titulo = "V I T Ó R I A"
        subtitulo = "Você venceu a partida!"
    elif resultado == "cpu":
        cor = RED
        titulo = "D E R R O T A"
        subtitulo = "A CPU venceu a partida."
    else:
        cor = GRAY
        titulo = "E M P A T E"
        subtitulo = "A batalha terminou sem um vencedor."

    print()
    print(f"{cor}╔{'═' * largura}╗{RESET}")
    print(_linha_caixa("", largura, cor, negrito=False))
    print(_linha_caixa("FIM DE JOGO", largura, cor, cor, negrito=False))
    print(_linha_caixa(titulo, largura, cor, cor))
    print(f"{cor}╠{'═' * largura}╣{RESET}")
    print(_linha_caixa(subtitulo, largura, cor, cor, negrito=False))
    if motivo:
        print(_linha_caixa(motivo, largura, cor, GRAY, negrito=False))
    print(_linha_caixa("", largura, cor, negrito=False))
    print(f"{cor}╚{'═' * largura}╝{RESET}")
    print()
