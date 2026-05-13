import os

if os.name == "nt":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

RESET  = "\033[0m"
BOLD   = "\033[1m"
GOLD   = "\033[38;5;220m"
CYAN   = "\033[38;5;45m"
GREEN  = "\033[38;5;46m"
YELLOW = "\033[38;5;226m"
RED    = "\033[38;5;196m"
GRAY   = "\033[38;5;240m"
DARKBLUE  = "\033[38;5;19m"

atributos = ["ataque", "defesa", "velocidade", "regeneração", "estratégia"]


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


def _cor_valor(v):
    if v >= 8:
        return GREEN
    if v >= 5:
        return YELLOW
    return RED


def exibir_carta(carta):
    nome = carta[0]
    super_trunfo = carta[1]

    cor_borda = GOLD if super_trunfo else CYAN
    marcador = "★" if super_trunfo else "◆"
    largura = 40

    titulo_visivel = f"{marcador} {nome} {marcador}"
    pad_esq = (largura - len(titulo_visivel)) // 2
    pad_dir = largura - len(titulo_visivel) - pad_esq

    print(f"{cor_borda}╔{'═' * largura}╗{RESET}")
    print(
        f"{cor_borda}║{RESET}{' ' * pad_esq}"
        f"{BOLD}{cor_borda}{titulo_visivel}{RESET}"
        f"{' ' * pad_dir}{cor_borda}║{RESET}"
    )
    if super_trunfo:
        rotulo = "SUPER TRUNFO"
        pad = (largura - len(rotulo)) // 2
        print(
            f"{cor_borda}║{RESET}{' ' * pad}{BOLD}{GOLD}{rotulo}{RESET}"
            f"{' ' * (largura - len(rotulo) - pad)}{cor_borda}║{RESET}"
        )
    print(f"{cor_borda}╠{'═' * largura}╣{RESET}")

    for i in range(2, 7):
        rotulo = atributos[i - 2].capitalize()
        valor = carta[i]
        cor = _cor_valor(valor)
        # visível: "  {rotulo:<12} ██████████ {valor:>2}  " = 2+12+1+10+1+2+2 = 30
        falta = largura - 30
        conteudo_colorido = (
            f"  {BOLD}{rotulo:<12}{RESET} "
            f"{cor}{'█' * valor}{GRAY}{'░' * (10 - valor)}{RESET} "
            f"{BOLD}{cor}{valor:>2}{RESET}  "
        )
        print(f"{cor_borda}║{RESET}{conteudo_colorido}{' ' * falta}{cor_borda}║{RESET}")

    print(f"{cor_borda}╚{'═' * largura}╝{RESET}")
