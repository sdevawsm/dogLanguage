# Desenvolvimento da Extensão

Guia para desenvolvedores que querem contribuir ou modificar a extensão Dog Language.

## 📋 Estrutura dos Arquivos

```
dog-extension/
├── package.json                    # Configuração principal da extensão
├── language-configuration.json     # Config de idioma (indentação, comentários)
├── README.md                       # Documentação do usuário
├── CHANGELOG.md                    # Histórico de alterações
├── THEME.md                        # Documentação de cores e temas
├── DEVELOPMENT.md                  # Este arquivo
├── .gitignore                      # Arquivos para ignorar no git
├── syntaxes/
│   └── dog.tmLanguage.json        # Definição de gramática TextMate
├── snippets/
│   └── dog.json                   # Snippets de código
└── dog-lang-0.0.1.vsix            # Pacote da extensão (gerado)
```

## 🛠️ Configuração do Ambiente

### Requisitos
- Node.js 12+
- VS Code 1.50+
- Git

### Instalação
```bash
# Clone o repositório
git clone https://github.com/dogLanguage/dog-language.git
cd dog-language/dog-extension

# Instale dependências (se necessário)
npm install
```

## 📝 Editando a Gramática

A gramática está definida em `syntaxes/dog.tmLanguage.json`. Este é um arquivo JSON que segue o padrão TextMate.

### Estrutura de uma Gramática

```json
{
  "name": "Dog Language",
  "scopeName": "source.dog",
  "patterns": [
    {
      "name": "keyword.control.dog",
      "match": "\\b(palavra-chave)\\b"
    }
  ],
  "repository": {
    "comment": {
      "patterns": [...]
    }
  }
}
```

### Testando a Gramática

1. Abra VS Code na pasta da extensão:
   ```bash
   code .
   ```

2. Pressione `F5` para iniciar a janela de debug

3. Abra um arquivo `.dog` para testar o highlighting

4. Use "Developer: Inspect Editor Tokens and Scopes" (Ctrl+Shift+P) para debug

## ✂️ Editando Snippets

Snippets estão em `snippets/dog.json`. Cada snippet é definido como:

```json
{
  "Nome do Snippet": {
    "prefix": "prefixo",
    "body": [
      "linha 1",
      "linha 2 com ${1:placeholder}"
    ],
    "description": "Descrição do snippet"
  }
}
```

### Placeholders
- `$1`, `$2`, etc - Posições do cursor
- `${1:default}` - Placeholder com valor padrão
- `$0` - Posição final do cursor

## 🔧 Configuração de Idioma

Em `language-configuration.json`:

```json
{
  "comments": {
    "lineComment": "//",
    "blockComment": ["/*", "*/"]
  },
  "brackets": [["AU", "UAU"]],
  "autoClosingPairs": [["(", ")"]],
  "indentationRules": {
    "increaseIndentPattern": "^\\s*(AU)\\b",
    "decreaseIndentPattern": "^\\s*(UAU)\\b"
  }
}
```

## 📦 Empacotando a Extensão

### Instalando o vsce
```bash
npm install -g vsce
```

### Criando o pacote
```bash
# No diretório dog-extension
vsce package

# Isso cria um arquivo dog-lang-0.1.0.vsix
```

### Testando o pacote localmente
```bash
# No VS Code, use:
Extensions: Install from VSIX

# Ou via linha de comando:
code --install-extension dog-lang-0.1.0.vsix
```

## 🚀 Publicando no VS Code Marketplace

### Requisitos
1. Conta Microsoft
2. PAT (Personal Access Token)

### Passos
```bash
# Login
vsce login seu-publisher-name

# Publicar
vsce publish

# Ou publicar com atualização de versão
vsce publish minor  # v0.1.0 → v0.2.0
vsce publish major  # v0.1.0 → v1.0.0
```

## 🐛 Testando Mudanças

### Teste Automático
1. Pressione `F5` na janela de desenvolvimento
2. VS Code abrirá uma nova janela com a extensão carregada
3. Abra um arquivo `.dog` para testar

### Debugging
- Use `console.log()` em arquivos JavaScript
- Veja a saída no console de debug
- Use "Developer Tools" (Ctrl+Shift+I) para inspecionar

## 🎨 Adicionando Suporte a Temas

1. Edite `THEME.md` com os novos scopes
2. Teste com diferentes temas do VS Code:
   - One Dark Pro
   - Dracula
   - Nord
   - GitHub Dark

## 📚 Referências Úteis

- [TextMate Language Documentation](https://macromates.com/manual/en/language_grammars)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [VS Code Syntax Highlighting Guide](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide)
- [Snippet Syntax](https://code.visualstudio.com/docs/editor/userdefinedsnippets)

## 🤝 Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
3. Commit suas mudanças: `git commit -am 'Add feature'`
4. Push para a branch: `git push origin feature/minha-feature`
5. Abra um Pull Request

## 📄 Licença

MIT - veja LICENSE para detalhes
