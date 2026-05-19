# 🐕 Dog Language VS Code Extension

Extensão VS Code com suporte completo para DogLanguage - uma linguagem de programação canina divertida e educacional!

## 🎯 Features

- ✅ **Syntax Highlighting** - Cores e destaque para toda a sintaxe Dog
- ✅ **Code Snippets** - Atalhos para estruturas comuns (if, while, funções, etc)
- ✅ **Auto-completion** - Conclusão de palavras-chave e funções
- ✅ **Bracket Matching** - Detecção automática de AU/UAU
- ✅ **Comment Support** - Comentários de linha (//) e bloco (/* */)
- ✅ **Indentation** - Indentação automática e inteligente

## 📦 Instalação

### Opção 1: Via VS Code Marketplace
```
1. Abra VS Code
2. Pressione Ctrl+Shift+X (Extensions)
3. Procure por "Dog Language"
4. Clique em Install
```

### Opção 2: Manual
```bash
# Clone o repositório
git clone https://github.com/dogLanguage/dog-language.git

# Copie a extensão para o diretório de extensões do VS Code
cp -r dog-extension ~/.vscode/extensions/dog-lang-0.1.0
```

## 🎨 Syntax Highlighting

A extensão fornece destaque para:

### Palavras-chave de Controle
- `dar_a_pata` (if)
- `ou_fingir_de_morto` (else)
- `focar_no_esquilo` (while)
- `trazer_bolinha` (return)

### Tipos de Dados
- `pedigree` (int)
- `pelo` (char)
- `carne` (float)
- `raça` (double)
- `vira_lata` (variável)

### Funções Embutidas
- `canil` (main)
- `latir` (print)
- `farejar` (input)

### Blocos
- `AU` (abre bloco {)
- `UAU` (fecha bloco })

## 📝 Snippets Disponíveis

Digite o prefixo e pressione `Tab` para expandir:

| Prefixo | Descrição | Atalho |
|---------|-----------|--------|
| `canil` | Função principal | Main |
| `latir` | Print statement | `latir("texto")` |
| `vira_lata` | Variável genérica | `vira_lata x = 5` |
| `pedigree` | Variável inteira | `pedigree x = 5` |
| `dar_a_pata` | If statement | Condicional |
| `dar_a_pata_senao` | If-else statement | Condicional com else |
| `focar_no_esquilo` | While loop | Loop |
| `funcao` | Função | Função customizada |
| `matilha` | Classe | Orientação a objetos |
| `trazer_bolinha` | Return | Retorno |
| `chamar_matilha` | Import | Importação |
| `programa` | Programa completo | Template |

## 🚀 Quick Start

1. Crie um arquivo `.dog`:
   ```bash
   touch meu_programa.dog
   ```

2. Digite `programa` e pressione `Tab` para gerar um template

3. Edite o código com syntax highlighting automático

4. Execute com:
   ```bash
   python3 dog_translator.py meu_programa.dog
   ```

## 🎓 Exemplo de Código

```dog
// Meu primeiro programa em DogLanguage
chamar_matilha <brinquedos.h>

canil() AU
    vira_lata energia = 10;
    
    dar_a_pata (energia > 5) AU
        latir("Rex tem muita energia!\n");
    UAU ou_fingir_de_morto AU
        latir("Rex está cansado...\n");
    UAU
    
    trazer_bolinha 0;
UAU
```

## 🎨 Temas Suportados

A extensão funciona com qualquer tema do VS Code. Recomendamos:
- One Dark Pro
- Dracula
- Nord
- GitHub Dark

## 🔧 Configuração

Adicione ao seu `settings.json` (Ctrl+,):

```json
"[dog]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "editor.default",
    "editor.tabSize": 4,
    "editor.insertSpaces": true
}
```

## 📚 Recursos

- [DogLanguage Repositório](https://github.com/dogLanguage/dog-language)
- [Documentação da Linguagem](../README.md)
- [Especificação Completa](../ESPECIFICACAO.md)

## 🐛 Bugs e Sugestões

Encontrou um bug? Tem uma sugestão?
[Abra uma issue](https://github.com/dogLanguage/dog-language/issues)

## 📄 Licença

MIT License - veja LICENSE para detalhes

## 🎉 Divirta-se!

Agora você tem todas as ferramentas para programar em Dog com estilo! 🐕

---

**Versão:** 0.2.0  
**Última atualização:** 2026-05-19
