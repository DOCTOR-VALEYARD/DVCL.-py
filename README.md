```markdown
# 🎨 DVCL.-py — Painel de Personalização do Termux

<div align="center">
  <img src="https://img.shields.io/badge/version-1.0-blue.svg" alt="Version 1.0">
  <img src="https://img.shields.io/badge/python-3.x-green.svg" alt="Python 3">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/platform-Termux-brightgreen.svg" alt="Platform Termux">
</div>

<p align="center">
  <b>Deixe seu Termux com a sua cara! 🚀</b><br>
  Criado por <b>DOCTOR VALEYARD CORINGA LUNÁTICO</b>
</p>

---

## 📌 Sobre o Projeto

O **DVCL.-py** é um script interativo em Python que permite personalizar completamente o prompt (`PS1`) do Termux. Com ele, você pode:

- ✏️ Alterar o nome exibido no terminal
- 🖼️ Adicionar molduras superior e inferior
- 🎨 Escolher cores para o nome, prompt e símbolo do cifrão
- 🔧 Selecionar entre diversos modelos prontos de prompt
- 💲 Customizar o símbolo do cifrão (qualquer caractere)
- 👀 Visualizar uma prévia antes de salvar
- 💾 Salvar as configurações permanentemente (mesmo após fechar o Termux)

---

## ⚙️ Funcionalidades Detalhadas

| Opção | Descrição |
|-------|-----------|
| **Nome personalizado** | Substitui o nome de usuário padrão pelo que você quiser. |
| **Molduras** | 9 estilos prontos ou crie as suas próprias. |
| **Cores** | 8 cores disponíveis para nome, prompt e cifrão. |
| **Modelos de prompt** | 7 modelos diferentes (incluindo linhas, horário, etc.). |
| **Símbolo do cifrão** | Use `$`, `#`, `>`, `λ` ou qualquer outro símbolo. |
| **Prévia interativa** | Veja como ficará antes de aplicar. |
| **Backup automático** | O arquivo `.bashrc` original é salvo como `.bashrc.backup_painel`. |

---

## 📲 Como Instalar e Usar

### Pré‑requisitos
- Termux instalado e atualizado
- Python 3 (já vem por padrão no Termux)

### Passo a passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/DOCTOR-VALEYARD/DVCL.-py.git
```

1. Acesse a pasta
   ```bash
   cd DVCL.-py
   ```
2. Dê permissão de execução (opcional)
   ```bash
   chmod +x Dvcl.py
   ```
3. Execute o painel
   ```bash
   python Dvcl.py
   ```
4. Navegue pelo menu interativo e personalize do seu jeito.
5. Salve as alterações (opção 9) e reinicie o Termux ou execute:
   ```bash
   source ~/.bashrc
   ```

---

🎯 Exemplo de Prompt Personalizado

Aqui está um exemplo do que você pode criar:

```
╔══════════════════════╗
🔹 DOCTOR VALEYARD:~/projetos λ
╚══════════════════════╝
```

(As possibilidades são infinitas!)

---

🔄 Restaurar Configurações Originais

Se quiser voltar ao prompt padrão do Termux, basta restaurar o backup:

```bash
cp ~/.bashrc.backup_painel ~/.bashrc
```

Ou remova manualmente as linhas entre os marcadores # --- PAINEL DOUTOR VALEYARD INÍCIO --- e # --- FIM --- no arquivo ~/.bashrc.

---

📁 Estrutura do Projeto

```
DVCL.-py/
├── Dvcl.py              # Script principal
├── README.md            # Este arquivo
└── .gitignore           (opcional)
```

---

🧑‍💻 Autor

DOCTOR VALEYARD CORINGA LUNÁTICO
GitHub

---

📄 Licença

Este projeto está licenciado sob a licença MIT – veja o arquivo LICENSE para mais detalhes.

---

⭐ Contribua

Gostou do projeto? Deixe uma estrela ⭐ no GitHub e compartilhe com outros usuários do Termux!
Sugestões e melhorias são bem‑vindas – fique à vontade para abrir uma issue ou enviar um pull request.

---

<div align="center">
  <i>Feito com 💚 e muito código para a comunidade Termux</i>
</div>
```

---
