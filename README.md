# DogLanguage 🐕

DogLanguage é uma linguagem de programação canina que executa diretamente via interpretador Python, sem necessidade de compilação para C.

## 🚀 Uso Rápido

Agora DogLanguage é interpretado diretamente em Python - nenhuma compilação necessária!

```bash
# Opção 1: Usar o interpretador diretamente
python3 dog_translator.py main.dog

# Opção 2: Usar o script auxiliar (mais simples)
python3 dogc.py main.dog
```

É isso! ✅ Não precisa mais de C ou compilação!

### Antes (C):
```bash
gcc -o dogc dog_translator.c  # Compilar o tradutor
./dogc main.dog               # Traduzir para C
gcc traduzido.c -o programa   # Compilar C
./programa                    # Executar
```

### Agora (Python - Direto):
```bash
python3 dog_translator.py main.dog  # Executa direto!
```

## 📂 O que já existe

- ✅ **Interpretador Python** (`dog_translator.py`) - Novo! Executa código .dog diretamente
- ✅ **Script Auxiliar** (`dogc.py`) - Interface simples para execução
- ✅ Arquivo de exemplo `main.dog` com demonstração completa
- ✅ Extensão VS Code em `dog-extension` com gramática TextMate para destaque de sintaxe
- 📖 **Guia de Migração** (`MIGRACAO_PYTHON.md`) - Histórico da conversão de C para Python

## Sintaxe básica da linguagem

### Estrutura de programa

```dog
chamar_matilha <stdio.h>

canil() AU
    pedigree x = 10;
    latir("Latindo em Dog! Valor de x: %d\n", x);
    trazer_bolinha 0;
UAU
```

### Palavras-chave suportadas

- `chamar_matilha` → `#include`
- `canil()` → `int main()`
- `AU` → `{`
- `UAU` → `}`
- `latir` → `printf`
- `farejar` → `scanf`
- `pedigree` → `int`
- `pelo` → `char`
- `carne` → `float`
- `raça` → `double`
- `se_tiver_petisco` → `if`
- `ou_rosnar` → `else`
- `perseguir` → `while`
- `trazer_bolinha` → `return`
- `classe` → `typedef struct` / `struct`
- `novo` → aloca com `malloc`
- `this` → `self`

### Classes e orientação a objetos


Especificação da Linguagem .dog
Sintaxe Básica:

• Importação: `chamar_matilha <biblioteca.h>`

• Blocos: `AU` (abre) e `UAU` (fecha)

• Finalizador: `🐾` (emoji de pata)

Tipagem:

• `pedigree` -> int

• `pelo` -> string

• `raça` -> float/double

• `bom_garoto` -> true

• `mal_educado` -> false

Fluxo e Controle:

• `se_tiver_petisco` / `ou_rosnar` -> if / else

• `perseguir` -> while

• `trazer_bolinha` -> return

• `tentar_pegar` / `fugiu_o_gato` -> try / catch

I/O:

• `latir()` -> print

• `farejar()` -> input

OO:

• `Matilha` -> class

• `novo` -> new

• `eu_mesmo` -> this/self