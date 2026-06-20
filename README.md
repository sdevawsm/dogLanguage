## 🧾 Programas exigidos pelo trabalho

Os três programas pedidoss no trabalho da faculdade estão incluídos no repositório. Você pode executá-los com `python3 dog_translator.py <arquivo>`:

- `hello_world.dog` — imprime "Hello, World!"
- `99_garrafas.dog` — versão do problema "99 garrafas"
- `main.dog` — exemplo principal que demonstra classes e I/O

Exemplo de execução:

```bash
# Executa o Hello World
## Exemplos de código

Apresentamos abaixo três trechos representativos que também estão disponíveis como arquivos no repositório (`hello_world.dog`, `main.dog`, `99_garrafas.dog`). Os exemplos estão formatados para leitura; o interpretador aceita `;` ou quebra de linha como finalizador.

### Hello World (`hello_world.dog`)

```dog
uivar canil() AU
    latir("Hello, World!\n");
    trazer_bolinha 0;
UAU
```

Executar:

```bash
python3 dog_translator.py hello_world.dog
```

### Exemplo principal com classes e I/O (`main.dog`)

Trecho simplificado (o arquivo completo está em `main.dog`):

```dog
// Classe GoldenRetriever com energia e métodos
matilha GoldenRetriever AU
    pinscher energia;

    instinto(pinscher e) AU
        eu_mesmo.energia = e;
    UAU

    funcao latir_baixo() AU
        latir("woof...\n");
    UAU

    funcao latir_alto() AU
        latir("WOOF WOOF!\n");
    UAU

    funcao descansar() AU
        latir("Rex está descansando...\n");
        eu_mesmo.energia = eu_mesmo.energia + 3;
    UAU
UAU

uivar canil() AU
    // tipos de dados
    pedigree idade = 3;
    carne altura = 0.5;
    raça peso = 2.5;
    pelo nome = "Rex";

    latir("Idade: %d anos\n", idade);
    latir("Altura: %.1f metros\n", altura);
    latir("Peso: %.1f kg\n", peso);
    latir("Nome: %s\n", nome);

    // leitura de entrada
    latir("Qual seu nome? ");
    pelo nome_input = farejar();
    latir("Olá, %s!\n", nome_input);

    // exemplo de uso da classe
    vira_lata rex = novo GoldenRetriever(2);
    dar_a_pata (rex.energia < 3) AU
        latir("Rex está cansado...\n");
        rex.descansar();
    UAU ou_fingir_de_morto AU
        latir("Rex quer brincar!\n");
    UAU

    trazer_bolinha 0;
UAU
```

Executar:

```bash
python3 dog_translator.py main.dog
```

### 99 Garrafas (`99_garrafas.dog`)

Implementação do clássico problema "99 garrafas":

```dog
pedigree garrafas = 99;

perseguir (garrafas > 0) AU
    latir("%d garrafas de cerveja na parede, %d garrafas de cerveja.\n", garrafas, garrafas);
    latir("Pegue uma, passe adiante, %d garrafas de cerveja na parede.\n\n", garrafas - 1);
    garrafas = garrafas - 1;
UAU

latir("Sem mais garrafas de cerveja na parede.\n");
trazer_bolinha 0;
```

Executar:

```bash
python3 dog_translator.py 99_garrafas.dog
```

---

Observações:

- Os exemplos acima são apenas trechos formatados para leitura; os arquivos completos estão no repositório.
- O emoji `🐾` aparece na documentação como marcador visual, mas não é necessário nas fontes e não é reconhecido como finalizador pelo interpretador.





## 🐶 Sintaxe básica

### Programa mínimo

```dog
pedigree x = 10🐾
latir("Valor: %d\n", x)🐾
trazer_bolinha 0🐾
```

### Tipos e variáveis

- `vira_lata` — variável genérica
- `pedigree` — inteiro
- `pelo` — string
- `carne` — float
- `raça` — double

#### Conversão de tipos

```dog
pedigree n = pedigree(farejar());
pelo s = pelo(123);
carne f = carne("3.14");
```

### Entrada do usuário

Use `farejar()` para ler texto. Para número inteiro:

```dog
latir("Digite um número: ");
pedigree escaneado = pedigree(farejar());
latir("Você digitou: %d\n", escaneado);
```

### Leitura e gravação de arquivos

Use `enterrar(caminho, conteudo)` para gravar texto em um arquivo, `enterrar_mais(caminho, conteudo)` para acrescentar no final e `cavar(caminho)` para ler o conteúdo de um arquivo:

```dog
enterrar("saida.txt", "Olá do DogLanguage!\n");
enterrar_mais("saida.txt", "Nova linha de log\n");
pelo texto = cavar("saida.txt");
latir("Conteúdo lido:\n%s", texto);
```

No exemplo acima, `enterrar_mais` funciona bem para um sistema de log, pois adiciona novas entradas sem apagar o que já estava no arquivo.

### Saída

```dog
latir("Olá, %s!\n", nome);
```

### Operações matemáticas

```dog
pedigree a = 10;
pedigree b = 3;
pedigree soma = a + b;
pedigree sub = a - b;
pedigree mult = a * b;
pedigree div = a / b;
pedigree resto = a % b;
latir("%d + %d = %d\n", a, b, soma);
```

### Arrays

```dog
vira_lata numeros = [1, 2, 3];
latir("Primeiro: %d\n", numeros[0]);
numeros[1] = 10;
```

### Controle de fluxo

Use `dar_a_pata (condição) AU ... UAU` para `if` e `UAU ou_fingir_de_morto AU` para o `else`.

A repetição em DogLanguage é feita com `focar_no_esquilo (condição) AU ... UAU`, que funciona como um `while`.
Há também um alias alternativo: `perseguir (condição) AU ... UAU`.

```dog
pedigree x = 3🐾

dar_a_pata (x > 0) AU
    latir("Positivo\n")🐾
UAU ou_fingir_de_morto AU
    latir("Não positivo\n")🐾
UAU

focar_no_esquilo (x < 5) AU
    x = x + 1🐾
    latir("x = %d\n", x)🐾
UAU
```

### Estruturas de repetição

```dog
vira_lata contador = 0;
perseguir (contador < 5) AU
    latir("contador = %d\n", contador);
    contador = contador + 1;
UAU
```

### Funções

```dog
uivar soma(pedigree a, pedigree b) AU
    trazer_bolinha a + b;
UAU

latir("A soma de 5 e 7 é: %d\n", soma(5, 7))
```

### Classes e objetos

```dog
matilha Cachorro AU
    pedigree energia;
    instinto(pedigree e) AU
        eu_mesmo.energia = e;
    UAU
    funcao latir() AU
        latir("Woof!\n");
    UAU
UAU

vira_lata dog = novo Cachorro(5);
dog.latir();
```

### Importação

```dog
chamar_matilha biblioteca.dog
```




## Códigos 


Código Hello, World

```dog
uivar canil() AU

  latir("Hello, World!\n")🐾
  
UAU

```


Código de exemplo com algumas implementações da linguagem
```dog

//Classe GoldenRetriever com energia e métodos de latir e descansar
matilha GoldenRetriever AU
    pinscher energia;

    instinto(pinscher e) AU
        eu_mesmo.energia = e;
    UAU

    funcao latir_baixo() AU
        latir("woof...\n");
    UAU

    funcao latir_alto() AU
        latir("WOOF WOOF!\n");
    UAU

    funcao descansar() AU
        latir("Rex está descansando...\n");
        eu_mesmo.energia = eu_mesmo.energia + 3;
    UAU
UAU



uivar canil() AU
    //tipos de dados
    pedigree idade = 3🐾
    carne altura = 0.5🐾
    raça peso = 2.5🐾
    pelo nome = "Rex"🐾

   
    latir("Idade: %d anos\n", idade)🐾
    latir("Altura: %.1f metros\n", altura)🐾
    latir("Peso: %.1f kg\n", peso)🐾
    latir("Nome: %s\n", nome)🐾
    latir("\n\n")🐾

    //Dados de entrada
    latir("Qual seu nome? ")🐾
    pelo nome = farejar()🐾
    latir("Olá, %s!\n", nome)🐾
    latir("\n\n")🐾

    // Exemplo de uso da classe GoldenRetriever
    vira_lata rex = novo GoldenRetriever(2);

    dar_a_pata (rex.energia < 3) AU
        latir("Rex está cansado...\n");
        rex.descansar();
    UAU ou_fingir_de_morto AU
        latir("Rex quer brincar!\n");

        focar_no_esquilo (rex.energia > 0) AU
            latir("Correndo atrás da bolinha...\n");
            rex.energia = rex.energia - 1;
        UAU

        rex.latir_alto();
    UAU

    dar_a_pata (rex.energia >= 3) AU
        rex.latir_baixo();
    UAU

    //return 0;
    trazer_bolinha 0;
UAU

```


Código 99 Garrafas
```dog
pedigree garrafas = 99🐾

perseguir (garrafas > 0) AU
    latir(garrafas)🐾
    latir(" garrafas de cerveja na parede, ")🐾
    latir(garrafas)🐾
    latir(" garrafas de cerveja.\n")🐾

    latir("Pegue uma, passe adiante, ")🐾
    latir(garrafas - 1)🐾
    latir(" garrafas de cerveja na parede.\n\n")🐾

    garrafas = garrafas - 1🐾
UAU

latir("Sem mais garrafas de cerveja na parede.\n")🐾
trazer_bolinha 0🐾
``` 