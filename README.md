# DogLanguage

DogLanguage é uma linguagem de programação canina simples com um tradutor para C e suporte de syntax highlighting no VS Code.

## O que já existe

- Um tradutor em C (`dog_translator.c`) que faz substituições diretas de palavras-chave Dog para C.
- Um arquivo de exemplo `main.dog` com função principal, declaração de variável, impressão e retorno.
- Uma extensão VS Code básica em `dog-extension` com gramática TextMate para destaque de sintaxe.

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

A linguagem Dog agora suporta declarações de classe simples como açúcar sintático para `struct` em C.

Exemplo:

```dog
chamar_matilha <stdio.h>
chamar_matilha <stdlib.h>

classe Cachorro AU
    propriedade pedigree idade;
UAU

canil() AU
    Cachorro *c = novo Cachorro;
    c->idade = 5;
    latir("Idade: %d\n", c->idade);
    trazer_bolinha 0;
UAU
```

Esse código gera algo parecido com:

```c
typedef struct Cachorro Cachorro;
struct Cachorro {
    int idade;
};

int main() {
    Cachorro *c = (Cachorro *)malloc(sizeof(Cachorro));
    c->idade = 5;
    printf("Idade: %d\n", c->idade);
    return 0;
}
```

### Comentários e strings

- Comentários de linha são reconhecidos pelo grammar do VS Code com `//`.
- Strings usam aspas duplas `"..."`.

## Como usar o tradutor

1. Compile o tradutor C:
   ```bash
   gcc dog_translator.c -o dog_translator
   ```
2. Traduza o arquivo Dog para C:
   ```bash
   ./dog_translator main.dog
   ```
3. Compile o arquivo C gerado:
   ```bash
   gcc traduzido.c -o programa
   ```
4. Execute o programa:
   ```bash
   ./programa
   ```

## Como usar a extensão VS Code

1. Abra `dog-extension` no VS Code.
2. Pressione `F5` para iniciar a janela de desenvolvimento.
3. Abra qualquer arquivo `.dog` para ver os destaques de sintaxe.
4. Se quiser instalar a extensão como pacote VSIX:
   - `npm install -g @vscode/vsce`
   - `vsce package`
   - Instale em Extensões > Install from VSIX...

## O que falta para a linguagem ser mais completa

1. Um analisador léxico e sintático real, em vez de substituição simples de palavras.
2. Suporte a operadores aritméticos e lógicos (`+`, `-`, `*`, `/`, `%`, `==`, `!=`, `&&`, `||`).
3. Suporte a declarações de funções além de `canil()` (funções definidas pelo usuário).
4. Melhoria do tratamento de `#include` e arquivos de cabeçalho, para gerar C mais robusto.
5. Geração de saída com nome de arquivo configurável e mensagens de erro mais claras.
6. Suporte a arrays, ponteiros, estruturas e tipos compostos.
7. Suporte a comentários de bloco e ao parsing de strings com escapes mais avançados.
8. Um analisador semântico para detectar erros antes da tradução.

## Exemplo de programa Dog

```dog
chamar_matilha <stdio.h>

canil() AU
    pedigree x = 10;
    se_tiver_petisco (x > 5) AU
        latir("x é maior que 5\n");
    UAU
    trazer_bolinha 0;
UAU
```

## Próximos passos sugeridos

- Adicionar suporte a `para` / `for`.
- Permitir `canil()` com argumentos e retorno de função.
- Fazer o tradutor gerar código C formatado e modular.
- Expandir o grammar do VS Code para classes de token mais precisas.

