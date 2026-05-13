# Super Trunfo - Attack on Titan
# Atributos: Ataque, Defesa, Velocidade, Regeneração, Estratégia (escala 0-10)
# Super Trunfo: Titã Fundador

cartas = [
    {
        "nome": "Titã Fundador",
        "super_trunfo": True,
        "atributos": {
            "ataque": 10,
            "defesa": 10,
            "velocidade": 8,
            "regeneracao": 10,
            "estrategia": 10,
        },
    },
    {
        "nome": "Titã de Ataque (Éren)",
        "super_trunfo": False,
        "atributos": {
            "ataque": 10,
            "defesa": 8,
            "velocidade": 9,
            "regeneracao": 9,
            "estrategia": 7,
        },
    },
    {
        "nome": "Titã Colossal",
        "super_trunfo": False,
        "atributos": {
            "ataque": 9,
            "defesa": 7,
            "velocidade": 2,
            "regeneracao": 6,
            "estrategia": 3,
        },
    },
    {
        "nome": "Titã Blindado",
        "super_trunfo": False,
        "atributos": {
            "ataque": 7,
            "defesa": 10,
            "velocidade": 5,
            "regeneracao": 5,
            "estrategia": 4,
        },
    },
    {
        "nome": "Titã Fêmea",
        "super_trunfo": False,
        "atributos": {
            "ataque": 8,
            "defesa": 8,
            "velocidade": 7,
            "regeneracao": 7,
            "estrategia": 8,
        },
    },
    {
        "nome": "Titã Bestial",
        "super_trunfo": False,
        "atributos": {
            "ataque": 8,
            "defesa": 6,
            "velocidade": 5,
            "regeneracao": 6,
            "estrategia": 9,
        },
    },
    {
        "nome": "Titã Mandíbula",
        "super_trunfo": False,
        "atributos": {
            "ataque": 5,
            "defesa": 3,
            "velocidade": 10,
            "regeneracao": 7,
            "estrategia": 4,
        },
    },
    {
        "nome": "Titã Carroceiro",
        "super_trunfo": False,
        "atributos": {
            "ataque": 2,
            "defesa": 4,
            "velocidade": 8,
            "regeneracao": 5,
            "estrategia": 6,
        },
    },
    {
        "nome": "Titã Martelo de Guerra",
        "super_trunfo": False,
        "atributos": {
            "ataque": 9,
            "defesa": 9,
            "velocidade": 3,
            "regeneracao": 6,
            "estrategia": 6,
        },
    },
    {
        "nome": "Capitão Levi",
        "super_trunfo": False,
        "atributos": {
            "ataque": 9,
            "defesa": 5,
            "velocidade": 10,
            "regeneracao": 1,
            "estrategia": 8,
        },
    },
    {
        "nome": "Mikasa Ackerman",
        "super_trunfo": False,
        "atributos": {
            "ataque": 8,
            "defesa": 4,
            "velocidade": 9,
            "regeneracao": 1,
            "estrategia": 7,
        },
    },
    {
        "nome": "Erwin Smith",
        "super_trunfo": False,
        "atributos": {
            "ataque": 4,
            "defesa": 2,
            "velocidade": 6,
            "regeneracao": 0,
            "estrategia": 10,
        },
    },
]

if __name__ == "__main__":
    for c in cartas:
        marca = " ⭐ SUPER TRUNFO" if c["super_trunfo"] else ""
        print(f"\n{c['nome']}{marca}")
        for atr, val in c["atributos"].items():
            print(f"  {atr.capitalize():<12} {val}")