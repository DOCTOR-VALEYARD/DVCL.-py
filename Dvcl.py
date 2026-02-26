#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import sys
import shutil

HOME = os.environ.get('HOME', '/data/data/com.termux/files/home')
CONFIG_FILE = os.path.join(HOME, '.termux_painel_config.json')
BASHRC = os.path.join(HOME, '.bashrc')
BACKUP_BASHRC = os.path.join(HOME, '.bashrc.backup_painel')

CORES = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'vermelho': '\033[91m',
    'verde': '\033[92m',
    'amarelo': '\033[93m',
    'azul': '\033[94m',
    'magenta': '\033[95m',
    'ciano': '\033[96m',
    'branco': '\033[97m',
}

CORES_DISPONIVEIS = list(CORES.keys())
CORES_DISPONIVEIS.remove('reset')
CORES_DISPONIVEIS.remove('bold')


# ---------------- CONFIG ---------------- #

def carregar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass

    return {
        'nome': os.environ.get('USER', 'termux'),
        'cor_nome': 'verde',
        'cor_prompt': 'azul',
        'cor_hora': 'amarelo',
        'mostrar_hora_banner': True,
        'mostrar_hora_prompt': True,
        'moldura_sup': '',
        'moldura_inf': ''
    }


def salvar_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


# ---------------- BANNER ---------------- #

def gerar_banner(config):
    os.system("pkg install figlet -y > /dev/null 2>&1")

    nome = config['nome']
    cor_nome = CORES[config['cor_nome']]
    cor_hora = CORES[config['cor_hora']]
    reset = CORES['reset']

    banner = "clear\n"
    banner += f"echo -e \"{cor_nome}\"\n"
    banner += f"figlet \"{nome}\"\n"
    banner += f"echo -e \"{reset}\"\n"

    if config['mostrar_hora_banner']:
        banner += f"echo -e \"{cor_hora}Hora: $(date +'%H:%M:%S'){reset}\"\n"
        banner += "echo\n"

    return banner


# ---------------- PROMPT ---------------- #

def gerar_ps1(config):
    nome = config['nome']
    cor_nome = CORES[config['cor_nome']]
    cor_prompt = CORES[config['cor_prompt']]
    cor_hora = CORES['cor_hora']
    reset = CORES['reset']
    bold = CORES['bold']

    prompt = ""

    if config['moldura_sup']:
        prompt += config['moldura_sup'] + "\n"

    if config['mostrar_hora_prompt']:
        prompt += f"{CORES[cor_hora]}$(date +%H:%M:%S){reset} "

    prompt += f"{cor_nome}{bold}{nome}{reset}"
    prompt += f"{cor_prompt}:\\w{reset} $ "

    if config['moldura_inf']:
        prompt += "\n" + config['moldura_inf']

    return prompt


# ---------------- APLICAR ---------------- #

def aplicar_config(config):
    banner = gerar_banner(config)
    ps1 = gerar_ps1(config)

    if os.path.exists(BASHRC) and not os.path.exists(BACKUP_BASHRC):
        shutil.copy2(BASHRC, BACKUP_BASHRC)

    marcador_inicio = "# --- PAINEL V2 INICIO ---\n"
    marcador_fim = "# --- PAINEL V2 FIM ---\n"

    linhas = []
    if os.path.exists(BASHRC):
        with open(BASHRC, 'r') as f:
            linhas = f.readlines()

    inicio = fim = -1
    for i, linha in enumerate(linhas):
        if linha == marcador_inicio:
            inicio = i
        if linha == marcador_fim:
            fim = i
            break

    bloco = [
        marcador_inicio,
        banner,
        f"PS1='{ps1}'\n",
        marcador_fim
    ]

    if inicio != -1 and fim != -1:
        linhas[inicio:fim+1] = bloco
    else:
        linhas.extend(bloco)

    with open(BASHRC, 'w') as f:
        f.writelines(linhas)


# ---------------- MENU ---------------- #

def escolher_cor(tipo, config):
    print("\nEscolha a cor:")
    for i, cor in enumerate(CORES_DISPONIVEIS, 1):
        print(f"{i}. {CORES[cor]}{cor}{CORES['reset']}")

    opc = input("Número: ").strip()
    try:
        idx = int(opc) - 1
        if 0 <= idx < len(CORES_DISPONIVEIS):
            config[tipo] = CORES_DISPONIVEIS[idx]
    except:
        pass


def menu():
    config = carregar_config()

    while True:
        print("\n===== PAINEL TERMUX 2.0 =====")
        print("1. Alterar nome")
        print("2. Cor do nome")
        print("3. Cor do prompt")
        print("4. Cor da hora")
        print("5. Ativar/desativar hora no banner")
        print("6. Ativar/desativar hora no prompt")
        print("7. Aplicar e sair")
        print("0. Sair")

        op = input("Escolha: ").strip()

        if op == '1':
            config['nome'] = input("Novo nome: ").strip()
        elif op == '2':
            escolher_cor('cor_nome', config)
        elif op == '3':
            escolher_cor('cor_prompt', config)
        elif op == '4':
            escolher_cor('cor_hora', config)
        elif op == '5':
            config['mostrar_hora_banner'] = not config['mostrar_hora_banner']
        elif op == '6':
            config['mostrar_hora_prompt'] = not config['mostrar_hora_prompt']
        elif op == '7':
            salvar_config(config)
            aplicar_config(config)
            print("Aplicado com sucesso!")
            print("Reinicie o Termux ou use: source ~/.bashrc")
            break
        elif op == '0':
            break


# ---------------- MAIN ---------------- #

def main():
    if not os.path.exists('/data/data/com.termux'):
        print("Execute apenas no Termux.")
        sys.exit(1)

    menu()


if __name__ == "__main__":
    main()
