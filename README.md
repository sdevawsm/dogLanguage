# DogLanguage 🐕

DogLanguage é uma linguagem de programação canina que executa diretamente via interpretador Python, sem necessidade de compilação para C.

## 🚀 Uso Rápido

DogLanguage é executado diretamente via Python, sem compilação ou arquivos auxiliares.

```bash
python3 dog_translator.py main.dog
```

## 📂 O que existe neste repositório

- ✅ `dog_translator.py` — interpretador Python para arquivos `.dog`
- ✅ `main.dog` — exemplo de programa DogLanguage

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