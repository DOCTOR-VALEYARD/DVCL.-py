#!/data/data/com.termux/files/usr/bin/python
# -*- coding: utf-8 -*-

"""
PAINEL DE PERSONALIZAÇÃO DO TERMUX - VERSÃO 2.0
Criado por: DOCTOR VALEYARD CORINGA LUNÁTICO
Descrição: Agora com banners 3D, caixinhas modernas, mais modelos e total personalização.
"""

import os
import json
import sys
import shutil
import random

# ========== CONFIGURAÇÕES ==========
HOME = os.environ.get('HOME', '/data/data/com.termux/files/home')
CONFIG_FILE = os.path.join(HOME, '.termux_painel_v2.json')
BASHRC = os.path.join(HOME, '.bashrc')
BACKUP_BASHRC = os.path.join(HOME, '.bashrc.backup_v2')

# Cores ANSI
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
    'preto': '\033[90m',
    'laranja': '\033[38;5;208m',
    'roxo': '\033[38;5;129m',
    'rosa': '\033[38;5;213m',
}

CORES_DISPONIVEIS = ['vermelho', 'verde', 'amarelo', 'azul', 'magenta', 'ciano', 'branco', 'preto', 'laranja', 'roxo', 'rosa']

# ========== BANNERS 3D ==========
BANNERS = {
    '1': '''
    ██████╗  ██████╗  ██████╗████████╗ ██████╗ ██████╗ 
    ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
    ██║  ██║██║   ██║██║        ██║   ██║   ██║██████╔╝
    ██║  ██║██║   ██║██║        ██║   ██║   ██║██╔══██╗
    ██████╔╝╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
    ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    ''',
    '2': '''
    ╔══╗╔══╗╔╗─╔╗╔══╗╔══╗╔╗─╔╗╔══╗
    ║╔╗║║╔╗║║║─║║║╔╗║╚║║╝║║─║║║╔═╝
    ║╚╝║║╚╝║║╚═╝║║╚╝║─║║─║╚═╝║║╚═╗
    ╚══╝╚══╝╚═╗╔╝╚══╝─╚╝─╚═╗╔╝╚══╝
    ────────╔═╝║──────╔═╝║────
    ────────╚══╝──────╚══╝────
    ''',
    '3': '''
    ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
    ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
    ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
    ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
    ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
    ''',
    '4': '''
    ╔═╗╔═╗╔╦╗╔═╗╦═╗╔╦╗╔═╗
    ║ ║╠═╝ ║ ║╣ ╠╦╝ ║ ╚═╗
    ╚═╝╩   ╩ ╚═╝╩╚═ ╩ ╚═╝
    ''',
    '5': '''
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    ██░▄▄░█░▄▄▀█▄░▄██░▄▄▀█░██░██
    ██░██░█░▀▀░██░███░▀▀▄█░▀▀░██
    ██░▀▀░█░██░██░███░██░█▀▄▄▀██
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    ''',
    '6': '''
    ┌─┐┌─┐┌┬┐┌─┐┬─┐┌─┐┌─┐┌┬┐
    │ ┬├┤  │ ├┤ ├┬┘├─┘├─┤ │ 
    └─┘└─┘ ┴ └─┘┴└─┴  ┴ ┴ ┴ 
    '''
}

# ========== MOLDURAS E CAIXINHAS ==========
MOLDURAS = {
    '1': ('╔════════════════════════╗', '╚════════════════════════╝'),
    '2': ('┌────────────────────────┐', '└────────────────────────┘'),
    '3': ('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄', '▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀'),
    '4': ('[========================]', '[========================]'),
    '5': ('╭────────────────────────╮', '╰────────────────────────╯'),
    '6': ('┏━━━━━━━━━━━━━━━━━━━━━━━━┓', '┗━━━━━━━━━━━━━━━━━━━━━━━━┛'),
    '7': ('🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲', '🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳'),
    '8': ('', ''),  # sem moldura
}

# ========== MODELOS DE PROMPT ==========
MODELOS = {
    '1': r'\u@\h \w ',                     # usuario@host ~/pasta
    '2': r'\u \w ',                         # usuario ~/pasta
    '3': r'┌─[\u]─[\w]\n└─',                # com linha
    '4': r'【\u】 \w ',                       # 【usuario】 ~/pasta
    '5': r'\[\e[91m\]\u\[\e[92m\]@\h:\w\[\e[0m\] ',  # colorido
    '6': r'\n┌─[\u]─[$(date +%H:%M)]─[\w]\n└─',  # com hora
    '7': r'╭─[\u]─[\w]\n╰─',                  # estilo bonito
}

# ========== FUNÇÕES UTILITÁRIAS ==========
def limpar_tela():
    os.system('clear')

def exibir_titulo():
    print(CORES['magenta'] + CORES['bold'] + """
╔══════════════════════════════════════════════════════════╗
║         PAINEL DE PERSONALIZAÇÃO DO TERMUX V2.0         ║
║            DOCTOR VALEYARD CORINGA LUNÁTICO             ║
╚══════════════════════════════════════════════════════════╝
""" + CORES['reset'])

def carregar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                defaults = {
                    'nome': os.environ.get('USER', 'termux'),
                    'banner': '1',
                    'moldura_sup': '╔════════════════════════╗',
                    'moldura_inf': '╚════════════════════════╝',
                    'cor_nome': 'verde',
                    'cor_diretorio': 'azul',
                    'cor_prompt': 'ciano',
                    'modelo': '2',
                    'cifrao': '$',
                    'cor_cifrao': 'amarelo',
                    'exibir_banner': True,
                    'exibir_moldura': True,
                }
                for key, value in defaults.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            pass
    return {
        'nome': os.environ.get('USER', 'termux'),
        'banner': '1',
        'moldura_sup': '╔════════════════════════╗',
        'moldura_inf': '╚════════════════════════╝',
        'cor_nome': 'verde',
        'cor_diretorio': 'azul',
        'cor_prompt': 'ciano',
        'modelo': '2',
        'cifrao': '$',
        'cor_cifrao': 'amarelo',
        'exibir_banner': True,
        'exibir_moldura': True,
    }

def salvar_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except:
        return False

def gerar_ps1(config):
    """Gera o PS1 completo com base na configuração."""
    nome = config['nome']
    cor_nome = CORES[config['cor_nome']]
    cor_dir = CORES[config['cor_diretorio']]
    cor_prompt = CORES[config['cor_prompt']]
    cifrao = config['cifrao']
    cor_cifrao = CORES[config['cor_cifrao']]
    reset = CORES['reset']
    bold = CORES['bold']

    # Modelo base (substitui \u pelo nome personalizado)
    modelo = MODELOS.get(config['modelo'], MODELOS['2'])
    modelo = modelo.replace(r'\u', nome)

    # Aplicar cores de forma inteligente (simplificado)
    # Vamos construir o prompt manualmente para ter controle total
    prompt = ""
    
    # Banner (se ativo)
    if config['exibir_banner'] and config['banner'] in BANNERS:
        banner = BANNERS[config['banner']]
        # Aplicar cor aleatória ou fixa? Vamos usar ciano por padrão
        prompt += CORES['ciano'] + banner + reset + "\n"
    
    # Moldura superior (se ativa)
    if config['exibir_moldura'] and config['moldura_sup']:
        prompt += config['moldura_sup'] + "\n"
    
    # Linha principal: nome colorido + : + diretório colorido + espaço + cifrão colorido
    prompt += cor_nome + bold + nome + reset
    prompt += cor_prompt + ":" + reset
    prompt += cor_dir + r"\w" + reset
    prompt += " " + cor_cifrao + cifrao + reset + " "
    
    # Moldura inferior (se ativa)
    if config['exibir_moldura'] and config['moldura_inf']:
        prompt += "\n" + config['moldura_inf']
    
    return prompt

def aplicar_config(config):
    ps1 = gerar_ps1(config)
    
    # Backup
    if os.path.exists(BASHRC) and not os.path.exists(BACKUP_BASHRC):
        shutil.copy2(BASHRC, BACKUP_BASHRC)
    
    if os.path.exists(BASHRC):
        with open(BASHRC, 'r') as f:
            linhas = f.readlines()
    else:
        linhas = []
    
    marcador_inicio = "# --- PAINEL DOUTOR VALEYARD V2 INÍCIO ---\n"
    marcador_fim = "# --- FIM V2 ---\n"
    
    inicio_idx = -1
    fim_idx = -1
    for i, linha in enumerate(linhas):
        if linha == marcador_inicio:
            inicio_idx = i
        elif linha == marcador_fim:
            fim_idx = i
            break
    
    nova_linha_ps1 = f"PS1='{ps1}'\n"
    
    if inicio_idx != -1 and fim_idx != -1:
        linhas[inicio_idx+1:fim_idx] = [nova_linha_ps1]
    else:
        if linhas and not linhas[-1].endswith('\n'):
            linhas[-1] += '\n'
        linhas.append(marcador_inicio)
        linhas.append(nova_linha_ps1)
        linhas.append(marcador_fim)
    
    with open(BASHRC, 'w') as f:
        f.writelines(linhas)
    return True

# ========== MENUS ==========
def menu_principal(config):
    while True:
        limpar_tela()
        exibir_titulo()
        print("⚙️  CONFIGURAÇÕES ATUAIS:\n")
        print(f"👤 Nome: {config['nome']}")
        print(f"🖼️  Banner: {config['banner']} (ativo: {config['exibir_banner']})")
        print(f"📦 Moldura: {config['moldura_sup'][:20]}... (ativo: {config['exibir_moldura']})")
        print(f"🎨 Cor nome: {config['cor_nome']}")
        print(f"📁 Cor diretório: {config['cor_diretorio']}")
        print(f"💬 Cor prompt: {config['cor_prompt']}")
        print(f"📝 Modelo: {config['modelo']}")
        print(f"💲 Cifrão: '{config['cifrao']}' (cor: {config['cor_cifrao']})")
        print("\n" + "="*50)
        print("🔹 ESCOLHA UMA OPÇÃO:")
        print("1. Alterar nome")
        print("2. Escolher banner 3D")
        print("3. Escolher moldura/caixinha")
        print("4. Escolher cor do nome")
        print("5. Escolher cor do diretório")
        print("6. Escolher cor do prompt (texto)")
        print("7. Escolher modelo de prompt")
        print("8. Personalizar símbolo do cifrão")
        print("9. Escolher cor do cifrão")
        print("10. Ativar/desativar banner")
        print("11. Ativar/desativar moldura")
        print("12. Visualizar prévia completa")
        print("13. SALVAR E APLICAR (sair)")
        print("0. Sair sem salvar")
        opcao = input("\n👉 Digite o número: ").strip()
        
        if opcao == '1':
            config['nome'] = input("Digite o nome desejado: ").strip() or config['nome']
        elif opcao == '2':
            config = menu_banner(config)
        elif opcao == '3':
            config = menu_moldura(config)
        elif opcao == '4':
            config = menu_cor("nome", config)
        elif opcao == '5':
            config = menu_cor("diretorio", config)
        elif opcao == '6':
            config = menu_cor("prompt", config)
        elif opcao == '7':
            config = menu_modelo(config)
        elif opcao == '8':
            config['cifrao'] = input("Digite o símbolo desejado (ex: $, #, >, λ): ").strip() or config['cifrao']
        elif opcao == '9':
            config = menu_cor("cifrao", config)
        elif opcao == '10':
            config['exibir_banner'] = not config['exibir_banner']
            print(f"Banner agora está {'ATIVADO' if config['exibir_banner'] else 'DESATIVADO'}")
            input("Pressione Enter...")
        elif opcao == '11':
            config['exibir_moldura'] = not config['exibir_moldura']
            print(f"Moldura agora está {'ATIVADA' if config['exibir_moldura'] else 'DESATIVADA'}")
            input("Pressione Enter...")
        elif opcao == '12':
            visualizar_previa(config)
        elif opcao == '13':
            if salvar_config(config) and aplicar_config(config):
                print("\n✅ Configurações salvas e aplicadas com sucesso!")
                print("Reinicie o Termux ou execute 'source ~/.bashrc'.")
            else:
                print("\n❌ Erro ao salvar.")
            input("Pressione Enter para sair...")
            break
        elif opcao == '0':
            print("\nSaindo sem salvar.")
            break
        else:
            input("Opção inválida. Pressione Enter...")

def menu_banner(config):
    limpar_tela()
    exibir_titulo()
    print("🎨 ESCOLHA UM BANNER 3D:\n")
    for chave, banner in BANNERS.items():
        print(f"{chave}. {banner[:50]}...")
    print("0. Voltar")
    opcao = input("\n👉 Número do banner: ").strip()
    if opcao in BANNERS:
        config['banner'] = opcao
    elif opcao == '0':
        pass
    else:
        input("Opção inválida.")
    return config

def menu_moldura(config):
    limpar_tela()
    exibir_titulo()
    print("📦 ESCOLHA UMA MOLDURA/CAIXINHA:\n")
    for chave, (sup, inf) in MOLDURAS.items():
        print(f"{chave}. Sup: '{sup[:20]}...' Inf: '{inf[:20]}...'")
    print("9. Personalizar (digitar superior e inferior)")
    print("0. Voltar")
    opcao = input("\n👉 Número: ").strip()
    if opcao in MOLDURAS:
        config['moldura_sup'], config['moldura_inf'] = MOLDURAS[opcao]
    elif opcao == '9':
        config['moldura_sup'] = input("Digite a moldura superior: ").strip()
        config['moldura_inf'] = input("Digite a moldura inferior: ").strip()
    elif opcao == '0':
        pass
    else:
        input("Opção inválida.")
    return config

def menu_cor(tipo, config):
    limpar_tela()
    exibir_titulo()
    print(f"🎨 ESCOLHA A COR PARA {tipo.upper()}:\n")
    for i, cor in enumerate(CORES_DISPONIVEIS, 1):
        print(f"{i}. {CORES[cor]}{cor}{CORES['reset']}")
    print("0. Voltar")
    opcao = input("\n👉 Número: ").strip()
    try:
        idx = int(opcao) - 1
        if 0 <= idx < len(CORES_DISPONIVEIS):
            if tipo == "nome":
                config['cor_nome'] = CORES_DISPONIVEIS[idx]
            elif tipo == "diretorio":
                config['cor_diretorio'] = CORES_DISPONIVEIS[idx]
            elif tipo == "prompt":
                config['cor_prompt'] = CORES_DISPONIVEIS[idx]
            elif tipo == "cifrao":
                config['cor_cifrao'] = CORES_DISPONIVEIS[idx]
    except:
        pass
    return config

def menu_modelo(config):
    limpar_tela()
    exibir_titulo()
    print("📝 ESCOLHA UM MODELO DE PROMPT:\n")
    for chave, modelo in MODELOS.items():
        exemplo = modelo.replace(r'\u', config['nome'])
        print(f"{chave}. {exemplo[:50]}...")
    print("0. Voltar")
    opcao = input("\n👉 Número: ").strip()
    if opcao in MODELOS:
        config['modelo'] = opcao
    return config

def visualizar_previa(config):
    limpar_tela()
    exibir_titulo()
    print("🔍 PRÉVIA DO SEU TERMINAL PERSONALIZADO:\n")
    ps1 = gerar_ps1(config)
    # Para exibir, substituímos \w por um diretório exemplo
    preview = ps1.replace(r'\w', '~/projetos')
    # Também substituímos escapes de cor do bash por cores do Python para visualização
    # (isso é complexo, faremos uma versão simplificada)
    print(preview)
    print("\n" + CORES['reset'] + "(Isso é uma simulação. No Termux real, o diretório será dinâmico.)")
    input("\nPressione Enter para voltar.")

def main():
    if not os.path.exists('/data/data/com.termux'):
        print("Este script foi feito para rodar no Termux.")
        sys.exit(1)
    config = carregar_config()
    menu_principal(config)

if __name__ == "__main__":
    main()
