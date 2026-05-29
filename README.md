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
pedigree x = 10;
latir("Latindo em Dog! Valor de x: %d\n", x);
trazer_bolinha 0;
```

### Palavras-chave suportadas

- `chamar_matilha` → `#include` (não faz nada no interpretador atual)
- `AU` → `{`
- `UAU` → `}`
- `latir` → `printf`
- `farejar` → `scanf`
- `vira_lata` → variável genérica
- `pedigree` → inteiro (`int`)
- `pelo` → texto (`string`)
- `carne` → ponto flutuante (`float`)
- `raça` → ponto flutuante (`double`)
- `dar_a_pata` → `if`
- `ou_fingir_de_morto` → `else`
- `focar_no_esquilo` → `while`
- `trazer_bolinha` → `return`

Também é possível fazer cast usando os nomes de tipo como funções:
- `pedigree("10")`
- `carne("3.14")`
- `raça("2.5")`
- `pelo(123)`

### Classes e orientação a objetos

A linguagem agora suporta classes, instâncias, atributos e métodos!

#### Declaração de classe

```dog
matilha Cachorro AU
    pedigree energia;
    
    funcao latir_alto() AU
        latir("WOOF WOOF!\n");
    UAU
    
    funcao descansar() AU
        latir("Zzzzz...\n");
        energia = energia + 5;
    UAU
UAU
```

#### Criação de instância

```dog
vira_lata rex = novo Cachorro();
```

#### Acesso a atributos e métodos

```dog
rex.energia = 10;
latir(rex.energia);
rex.latir_alto();
rex.descansar();
```

#### Exemplo completo

```dog
matilha GoldenRetriever AU
    pedigree energia;
    
    funcao brincar() AU
        dar_a_pata (energia > 0) AU
            latir("Correndo atrás da bolinha!\n");
            energia = energia - 1;
        UAU ou_fingir_de_morto AU
            latir("Muito cansado para brincar...\n");
        UAU
    UAU
UAU

funcao canil() AU
    vira_lata dog = novo GoldenRetriever();
    dog.energia = 5;
    dog.brincar();
    trazer_bolinha 0;
UAU
```

Especificação da Linguagem .dog
Sintaxe Básica:

• Importação: `chamar_matilha <biblioteca.h>`

• Blocos: `AU` (abre) e `UAU` (fecha)

• Finalizador: `🐾` (emoji de pata) ou `;` ou  sem pata ou ;`  

```Decimal: 128062
UTF‑8 bytes: F0 9F 90 BE
HTML: 🐾 ou 🐾
Python string: '\U0001F43E'
Digitar no teclado:
- Linux: Ctrl+Shift+U → 1f43e → Enter
- Windows: Win + . (emoji picker) → pesquisar "paw"
- macOS: Ctrl + Cmd + Space (emoji picker)
```

Tipagem:

• `pedigree` -> int

• `pelo` -> string

• `carne` / `raça` -> float/double

• Casts podem ser feitos como funções de tipo:
  - `pedigree(valor)` → inteiro
  - `carne(valor)` / `raça(valor)` → ponto flutuante
  - `pelo(valor)` → string

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