#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import shutil

HOME = os.environ.get("HOME")
CONFIG = os.path.join(HOME, ".painel_termux_config.json")
BASHRC = os.path.join(HOME, ".bashrc")
BACKUP = os.path.join(HOME, ".bashrc.backup_painel")

CORES = {
    1: ("vermelho", "\033[91m"),
    2: ("verde", "\033[92m"),
    3: ("amarelo", "\033[93m"),
    4: ("azul", "\033[94m"),
    5: ("magenta", "\033[95m"),
    6: ("ciano", "\033[96m"),
    7: ("branco", "\033[97m")
}

RESET = "\033[0m"
BOLD = "\033[1m"

def carregar():
    if os.path.exists(CONFIG):
        with open(CONFIG, "r") as f:
            return json.load(f)
    return {
        "nome": "TERMUX",
        "cor_nome": 6,
        "cor_hora": 3,
        "cor_prompt": 2,
        "mostrar_hora_banner": True,
        "mostrar_hora_prompt": False
    }

def salvar(cfg):
    with open(CONFIG, "w") as f:
        json.dump(cfg, f, indent=4)

def instalar_figlet():
    os.system("pkg install figlet -y > /dev/null 2>&1")

def gerar_bloco_bash(cfg):
    instalar_figlet()

    nome = cfg["nome"]
    cor_nome = CORES[cfg["cor_nome"]][1]
    cor_hora = CORES[cfg["cor_hora"]][1]
    cor_prompt = CORES[cfg["cor_prompt"]][1]

    bloco = []
    bloco.append("clear")

    # BANNER COM NOME
    bloco.append(f'echo -e "{cor_nome}{BOLD}"')
    bloco.append(f'figlet "{nome}"')
    bloco.append(f'echo -e "{RESET}"')

    # HORA NO TOPO
    if cfg["mostrar_hora_banner"]:
        bloco.append(f'echo -e "{cor_hora}Hora: $(date +\'%H:%M:%S\'){RESET}"')
        bloco.append("echo")

    # PROMPT
    ps1 = ""
    if cfg["mostrar_hora_prompt"]:
        ps1 += f"{cor_hora}$(date +'%H:%M:%S') "

    ps1 += f"{cor_prompt}{nome} \\w{RESET} $ "

    bloco.append(f"PS1='{ps1}'")

    return "\n".join(bloco)

def aplicar(cfg):
    bloco = gerar_bloco_bash(cfg)

    inicio = "# === PAINEL PERSONALIZADO INICIO ===\n"
    fim = "# === PAINEL PERSONALIZADO FIM ===\n"

    if os.path.exists(BASHRC) and not os.path.exists(BACKUP):
        shutil.copy2(BASHRC, BACKUP)

    linhas = []
    if os.path.exists(BASHRC):
        with open(BASHRC, "r") as f:
            linhas = f.readlines()

    i_inicio = i_fim = -1
    for i, l in enumerate(linhas):
        if l == inicio:
            i_inicio = i
        if l == fim:
            i_fim = i
            break

    novo_bloco = [
        inicio,
        bloco + "\n",
        fim
    ]

    if i_inicio != -1 and i_fim != -1:
        linhas[i_inicio:i_fim+1] = novo_bloco
    else:
        linhas.extend(novo_bloco)

    with open(BASHRC, "w") as f:
        f.writelines(linhas)

def escolher_cor():
    print("\nEscolha a cor:")
    for numero, (nome, _) in CORES.items():
        print(f"{numero} - {nome}")
    escolha = int(input("Número: "))
    if escolha in CORES:
        return escolha
    return 6

def menu():
    cfg = carregar()

    while True:
        os.system("clear")
        print(f"{BOLD}╔════════════════════════════════════╗")
        print("║     PAINEL AVANÇADO DO TERMUX     ║")
        print("╚════════════════════════════════════╝" + RESET)

        print(f"\nNome atual: {cfg['nome']}")
        print(f"Hora no banner: {cfg['mostrar_hora_banner']}")
        print(f"Hora no prompt: {cfg['mostrar_hora_prompt']}")

        print("\n1 - Alterar nome")
        print("2 - Cor do nome")
        print("3 - Cor da hora")
        print("4 - Cor do prompt")
        print("5 - Ativar/Desativar hora no topo")
        print("6 - Ativar/Desativar hora no prompt")
        print("7 - Aplicar e sair")
        print("0 - Sair")

        op = input("\nEscolha: ")

        if op == "1":
            cfg["nome"] = input("Novo nome: ")
        elif op == "2":
            cfg["cor_nome"] = escolher_cor()
        elif op == "3":
            cfg["cor_hora"] = escolher_cor()
        elif op == "4":
            cfg["cor_prompt"] = escolher_cor()
        elif op == "5":
            cfg["mostrar_hora_banner"] = not cfg["mostrar_hora_banner"]
        elif op == "6":
            cfg["mostrar_hora_prompt"] = not cfg["mostrar_hora_prompt"]
        elif op == "7":
            salvar(cfg)
            aplicar(cfg)
            print("\nAplicado. Reinicie o Termux ou use: source ~/.bashrc")
            break
        elif op == "0":
            break

if __name__ == "__main__":
    menu()
