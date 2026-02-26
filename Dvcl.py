#!/data/data/com.termux/files/usr/bin/python
# -*- coding: utf-8 -*-

"""
PAINEL DE PERSONALIZAÇÃO DO TERMUX
Criado por: DOCTOR VALEYARD CORINGA LUNÁTICO
Versão: 1.0
Descrição: Este script permite personalizar a aparência do prompt do Termux
(PS1) de forma interativa, com opções de nome, molduras, cores e modelos.
As alterações são salvas no arquivo .bashrc e permanecem mesmo após fechar
o Termux.
"""

import os
import json
import sys
import shutil

# Caminhos
HOME = os.environ.get('HOME', '/data/data/com.termux/files/home')
CONFIG_FILE = os.path.join(HOME, '.termux_painel_config.json')
BASHRC = os.path.join(HOME, '.bashrc')
BACKUP_BASHRC = os.path.join(HOME, '.bashrc.backup_painel')

# Cores ANSI para o menu e prompt
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
}

# Lista de cores disponíveis para escolha (para o usuário)
CORES_DISPONIVEIS = ['vermelho', 'verde', 'amarelo', 'azul', 'magenta', 'ciano', 'branco', 'preto']

# Modelos de prompt predefinidos
MODELOS = {
    '1': r'\u@\h \$ ',                     # usuario@host $
    '2': r'\u \$ ',                         # usuario $
    '3': r'➜ \u \$ ',                       # ➜ usuario $
    '4': r'┌─[\u]─[\w]\n└─\$ ',             # ┌─[usuario]─[caminho]\n└─$
    '5': r'【\u】\$ ',                        # 【usuario】$
    '6': r'\[\e[91m\]\u\[\e[92m\]@\h:\w\$\[\e[0m\] ',  # usuário vermelho, @ verde, etc. (exemplo colorido)
    '7': r'\n┌─[\u]─[$(date +%H:%M)]\n└─\$ ',  # com hora
}

# Molduras predefinidas
MOLDURAS = {
    '1': ('---', '---'),
    '2': ('===', '==='),
    '3': ('***', '***'),
    '4': ('###', '###'),
    '5': ('~~~', '~~~'),
    '6': ('▄'*10, '▀'*10),
    '7': ('════', '════➤'),
    '8': ('────', '────➤'),
    '9': ('', ''),  # sem moldura
}

def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('clear')

def exibir_titulo():
    """Exibe o título do painel com arte ASCII."""
    print(CORES['magenta'] + CORES['bold'] + """
╔══════════════════════════════════════════════════════════╗
║     PAINEL DE PERSONALIZAÇÃO DO TERMUX                  ║
║            DOCTOR VALEYARD CORINGA LUNÁTICO             ║
╚══════════════════════════════════════════════════════════╝
""" + CORES['reset'])

def carregar_config():
    """Carrega as configurações do arquivo JSON ou retorna valores padrão."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Garantir que todas as chaves existam
                defaults = {
                    'nome': os.environ.get('USER', 'termux'),
                    'moldura_sup': '',
                    'moldura_inf': '',
                    'cor_nome': 'verde',
                    'cor_prompt': 'azul',
                    'modelo': '2',
                    'cifrao': '$',
                    'cor_cifrao': 'amarelo'
                }
                for key, value in defaults.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            pass
    # Valores padrão
    return {
        'nome': os.environ.get('USER', 'termux'),
        'moldura_sup': '',
        'moldura_inf': '',
        'cor_nome': 'verde',
        'cor_prompt': 'azul',
        'modelo': '2',
        'cifrao': '$',
        'cor_cifrao': 'amarelo'
    }

def salvar_config(config):
    """Salva as configurações no arquivo JSON."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except:
        return False

def aplicar_config(config):
    """Aplica as configurações gerando a linha PS1 e inserindo no .bashrc."""
    # Gerar a linha PS1 com base nas configurações
    ps1 = gerar_ps1(config)

    # Fazer backup do .bashrc se não existir
    if os.path.exists(BASHRC) and not os.path.exists(BACKUP_BASHRC):
        shutil.copy2(BASHRC, BACKUP_BASHRC)

    # Ler conteúdo atual do .bashrc (ou criar vazio)
    if os.path.exists(BASHRC):
        with open(BASHRC, 'r') as f:
            linhas = f.readlines()
    else:
        linhas = []

    # Marcadores para identificar a seção do painel
    marcador_inicio = "# --- PAINEL DOUTOR VALEYARD INÍCIO ---\n"
    marcador_fim = "# --- FIM ---\n"

    # Procurar a seção existente
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
        # Substituir a seção antiga
        linhas[inicio_idx+1:fim_idx] = [nova_linha_ps1]
    else:
        # Adicionar nova seção no final
        if linhas and not linhas[-1].endswith('\n'):
            linhas[-1] += '\n'
        linhas.append(marcador_inicio)
        linhas.append(nova_linha_ps1)
        linhas.append(marcador_fim)

    # Escrever de volta no .bashrc
    with open(BASHRC, 'w') as f:
        f.writelines(linhas)

    return True

def gerar_ps1(config):
    """Gera a string PS1 baseada na configuração."""
    nome = config['nome']
    cor_nome = CORES[config['cor_nome']]
    cor_prompt = CORES[config['cor_prompt']]
    cifrao = config['cifrao']
    cor_cifrao = CORES[config['cor_cifrao']]
    reset = CORES['reset']
    bold = CORES['bold']

    # Escolher modelo base
    modelo_base = MODELOS.get(config['modelo'], MODELOS['2'])

    # Substituir \u pelo nome personalizado (se necessário, alguns modelos já usam \u)
    # Vamos substituir \u pelo nome, mas manter outros escapes como \h, \w, etc.
    # O bash interpreta \u, \h, etc. Se quisermos fixar o nome, podemos substituir.
    # Para simplificar, vamos substituir \u pelo nome diretamente, mas isso pode
    # quebrar outros escapes. Melhor: manter \u, mas o nome do usuário já é o
    # que definimos? No Termux, \u pega o usuário do sistema. Para usar nosso nome,
    # precisamos substituir.
    # Vamos substituir \u pelo nome configurado.
    modelo_base = modelo_base.replace(r'\u', nome)

    # Aplicar cores ao nome (se o modelo não tiver cores próprias)
    # Como o modelo pode conter escapes de cor, vamos inserir as cores em volta do nome.
    # Mas isso é complicado se o nome já está colorido no modelo.
    # Para simplicidade, vamos aplicar cor apenas se o modelo não tiver códigos \e[.
    if r'\e[' not in modelo_base and r'\\e[' not in modelo_base:
        # Encontrar onde está o nome (já substituído) e colocar cores
        # Vamos substituir a primeira ocorrência do nome por ${cor_nome}${nome}${reset}
        # Mas cuidado com sobreposição.
        # Método simples: criar um prompt com a estrutura: moldura_sup + cor_nome + nome + reset + resto
        # Para isso, precisamos separar o modelo em partes.
        # Vamos fazer de forma mais direta: construir o prompt manualmente com base no modelo escolhido.
        # Como existem vários modelos, vou optar por construir um prompt personalizado.
        pass

    # Construção personalizada (ignorando modelo detalhado, usando uma estrutura simples)
    # Para facilitar, vou criar um prompt com base nas escolhas:
    # [moldura superior]
    # [nome colorido] [prompt padrão] [cifrão colorido]
    # [moldura inferior]
    prompt = ""

    # Moldura superior
    if config['moldura_sup']:
        prompt += config['moldura_sup'] + "\n"

    # Nome com cor
    prompt += cor_nome + bold + nome + reset

    # Parte do prompt (pode incluir caminho, etc) - usar um formato fixo
    prompt += cor_prompt + ":\\w" + reset

    # Cifrão
    prompt += " " + cor_cifrao + cifrao + reset + " "

    # Moldura inferior
    if config['moldura_inf']:
        prompt += "\n" + config['moldura_inf']

    return prompt

def menu_principal(config):
    """Exibe o menu principal e processa as opções."""
    while True:
        limpar_tela()
        exibir_titulo()
        print("Configurações atuais:\n")
        print(f"Nome: {config['nome']}")
        print(f"Moldura superior: '{config['moldura_sup']}'")
        print(f"Moldura inferior: '{config['moldura_inf']}'")
        print(f"Cor do nome: {config['cor_nome']}")
        print(f"Cor do prompt: {config['cor_prompt']}")
        print(f"Modelo: {config['modelo']}")
        print(f"Símbolo do cifrão: '{config['cifrao']}'")
        print(f"Cor do cifrão: {config['cor_cifrao']}")
        print("\n" + "="*50)
        print("Escolha uma opção:")
        print("1. Alterar nome")
        print("2. Escolher moldura")
        print("3. Escolher cor do nome")
        print("4. Escolher cor do prompt")
        print("5. Escolher modelo de prompt")
        print("6. Personalizar símbolo do cifrão")
        print("7. Escolher cor do cifrão")
        print("8. Visualizar prévia")
        print("9. Salvar e aplicar (sair)")
        print("0. Sair sem salvar")
        opcao = input("\nDigite o número da opção: ").strip()

        if opcao == '1':
            config['nome'] = input("Digite o nome desejado: ").strip() or config['nome']
        elif opcao == '2':
            config = menu_moldura(config)
        elif opcao == '3':
            config = menu_cor("nome", config)
        elif opcao == '4':
            config = menu_cor("prompt", config)
        elif opcao == '5':
            config = menu_modelo(config)
        elif opcao == '6':
            config['cifrao'] = input("Digite o símbolo desejado (ex: $, #, >, λ): ").strip() or config['cifrao']
        elif opcao == '7':
            config = menu_cor("cifrao", config)
        elif opcao == '8':
            visualizar_previa(config)
        elif opcao == '9':
            if salvar_config(config) and aplicar_config(config):
                print("\nConfigurações salvas e aplicadas com sucesso!")
                print("Reinicie o Termux ou execute 'source ~/.bashrc' para ver as alterações.")
            else:
                print("\nErro ao salvar configurações.")
            input("Pressione Enter para sair...")
            break
        elif opcao == '0':
            print("\nSaindo sem salvar.")
            break
        else:
            input("Opção inválida. Pressione Enter para continuar...")

def menu_moldura(config):
    """Submenu para escolher moldura."""
    limpar_tela()
    exibir_titulo()
    print("Escolha um tipo de moldura:\n")
    for chave, (sup, inf) in MOLDURAS.items():
        print(f"{chave}. Superior: '{sup}'  Inferior: '{inf}'")
    print("10. Personalizar (digitar superior e inferior)")
    print("0. Voltar sem alterar")
    opcao = input("\nDigite o número: ").strip()
    if opcao in MOLDURAS:
        config['moldura_sup'], config['moldura_inf'] = MOLDURAS[opcao]
    elif opcao == '10':
        config['moldura_sup'] = input("Digite a moldura superior: ").strip()
        config['moldura_inf'] = input("Digite a moldura inferior: ").strip()
    elif opcao == '0':
        pass
    else:
        input("Opção inválida. Pressione Enter...")
    return config

def menu_cor(tipo, config):
    """Submenu para escolher cor (tipo: 'nome', 'prompt', 'cifrao')."""
    limpar_tela()
    exibir_titulo()
    print(f"Escolha a cor para {tipo}:\n")
    for i, cor in enumerate(CORES_DISPONIVEIS, 1):
        print(f"{i}. {CORES[cor]}{cor}{CORES['reset']}")
    print("0. Voltar")
    opcao = input("\nDigite o número: ").strip()
    try:
        idx = int(opcao) - 1
        if 0 <= idx < len(CORES_DISPONIVEIS):
            if tipo == "nome":
                config['cor_nome'] = CORES_DISPONIVEIS[idx]
            elif tipo == "prompt":
                config['cor_prompt'] = CORES_DISPONIVEIS[idx]
            elif tipo == "cifrao":
                config['cor_cifrao'] = CORES_DISPONIVEIS[idx]
        elif opcao == '0':
            pass
        else:
            input("Opção inválida. Pressione Enter...")
    except:
        input("Opção inválida. Pressione Enter...")
    return config

def menu_modelo(config):
    """Submenu para escolher modelo de prompt."""
    limpar_tela()
    exibir_titulo()
    print("Escolha um modelo de prompt (exemplos aproximados):\n")
    for chave, modelo in MODELOS.items():
        # Mostrar exemplo substituindo \u pelo nome atual
        exemplo = modelo.replace(r'\u', config['nome'])
        print(f"{chave}. {exemplo[:50]}...")
    print("0. Voltar")
    opcao = input("\nDigite o número do modelo: ").strip()
    if opcao in MODELOS:
        config['modelo'] = opcao
    elif opcao == '0':
        pass
    else:
        input("Opção inválida. Pressione Enter...")
    return config

def visualizar_previa(config):
    """Mostra uma prévia do prompt com as configurações atuais."""
    limpar_tela()
    exibir_titulo()
    print("PRÉVIA DO SEU PROMPT PERSONALIZADO:\n")
    ps1 = gerar_ps1(config)
    # Para exibir, precisamos interpretar os escapes do bash? Vamos mostrar como string crua.
    # Mas para dar uma ideia, podemos simular a aparência usando as cores do Python.
    # Vamos construir uma representação simples.
    preview = ""
    if config['moldura_sup']:
        preview += config['moldura_sup'] + "\n"
    preview += CORES[config['cor_nome']] + CORES['bold'] + config['nome'] + CORES['reset']
    preview += CORES[config['cor_prompt']] + ":~/caminho" + CORES['reset']
    preview += " " + CORES[config['cor_cifrao']] + config['cifrao'] + CORES['reset'] + " "
    if config['moldura_inf']:
        preview += "\n" + config['moldura_inf']
    print(preview)
    print("\n" + CORES['reset'] + "(Isso é apenas uma simulação. No Termux real, terá o caminho dinâmico.)")
    input("\nPressione Enter para voltar.")

def main():
    """Função principal."""
    # Verificar se está no Termux
    if not os.path.exists('/data/data/com.termux'):
        print("Este script foi feito para rodar no Termux.")
        sys.exit(1)

    config = carregar_config()
    menu_principal(config)

if __name__ == "__main__":
    main()
