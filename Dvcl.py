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
    "vermelho": "\\033[91m",
    "verde": "\\033[92m",
    "amarelo": "\\033[93m",
    "azul": "\\033[94m",
    "magenta": "\\033[95m",
    "ciano": "\\033[96m",
    "branco": "\\033[97m",
    "bold": "\\033[1m",
    "reset": "\\033[0m"
}

def carregar():
    if os.path.exists(CONFIG):
        with open(CONFIG, "r") as f:
            return json.load(f)
    return {
        "nome": "TERMUX",
        "cor_nome": "ciano",
        "cor_hora": "amarelo",
        "cor_prompt": "verde",
        "mostrar_hora_banner": True,
        "mostrar_hora_prompt": True
    }

def salvar(cfg):
    with open(CONFIG, "w") as f:
        json.dump(cfg, f, indent=4)

def instalar_figlet():
    os.system("pkg install figlet -y > /dev/null 2>&1")

def gerar_bloco_bash(cfg):
    instalar_figlet()

    nome = cfg["nome"]
    cor_nome = CORES[cfg["cor_nome"]]
    cor_hora = CORES[cfg["cor_hora"]]
    cor_prompt = CORES[cfg["cor_prompt"]]
    reset = CORES["reset"]

    bloco = []
    bloco.append("clear")

    # NOME GIGANTE
    bloco.append(f"echo -e \"{cor_nome}{CORES['bold']}\"")
    bloco.append(f"figlet \"{nome}\"")
    bloco.append(f"echo -e \"{reset}\"")

    # HORA NO TOPO
    if cfg["mostrar_hora_banner"]:
        bloco.append(f"echo -e \"{cor_hora}Hora: $(date +'%H:%M:%S'){reset}\"")
        bloco.append("echo")

    # PROMPT
    # PROMPT
ps1 = ""

# Hora NÃO vai mais no prompt (já está no banner)
ps1 += f"{cor_prompt}        {cfg['nome']}   \\w{reset} $ "


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

def menu():
    cfg = carregar()

    while True:
        os.system("clear")
        print("\033[95m\033[1m")
        print("╔════════════════════════════════════╗")
        print("║     PAINEL AVANÇADO DO TERMUX     ║")
        print("╚════════════════════════════════════╝")
        print("\033[0m")

        print(f"Nome: {cfg['nome']}")
        print(f"Hora no banner: {cfg['mostrar_hora_banner']}")
        print(f"Hora no prompt: {cfg['mostrar_hora_prompt']}")
        print("")
        print("1 - Alterar nome")
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
            cfg["cor_nome"] = input("Cor (vermelho, verde, amarelo, azul, magenta, ciano, branco): ")
        elif op == "3":
            cfg["cor_hora"] = input("Cor da hora: ")
        elif op == "4":
            cfg["cor_prompt"] = input("Cor do prompt: ")
        elif op == "5":
            cfg["mostrar_hora_banner"] = not cfg["mostrar_hora_banner"]
        elif op == "6":
            cfg["mostrar_hora_prompt"] = not cfg["mostrar_hora_prompt"]
        elif op == "7":
            salvar(cfg)
            aplicar(cfg)
            print("Aplicado. Reinicie o Termux ou use: source ~/.bashrc")
            break
        elif op == "0":
            break

if __name__ == "__main__":
    menu()
