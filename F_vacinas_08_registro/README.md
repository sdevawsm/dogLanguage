# F Vacinas 08 - Registro e Revisão

Este programa em DogLang registra vacinas de pets em um arquivo e exibe o histórico sempre que possível.

## Como executar

1. Certifique-se de que o Python 3.14 ou superior esteja instalado.
2. Abra o terminal na pasta `F_vacinas_08_registro`.
3. Execute:

```bash
python dog_translator.py registro_vacinas.dog
```

Ou

```bash
python3 dog_translator.py registro_vacinas.dog
```

## Como funciona

- Ao iniciar, o programa lê o arquivo `dados.txt`.
- Se o arquivo existir, o histórico de vacinas é exibido.
- Se não existir, o arquivo é criado automaticamente quando uma nova vacina é registrada.
- O usuário é perguntado se deseja registrar uma nova vacina.
- Se responder `s`, o programa pede:
  - nome do pet
  - nome da vacina
  - dia da vacina
- O registro é gravado no final de `dados.txt` no formato:
  - `Pet: <nome> | Vacina: <nome> | Dia: <dia>`

## Observações

- O programa usa sempre o mesmo arquivo `dados.txt`.
- Não há suporte a edição ou remoção de registros no menu atual.
- Não há suporte para alternar de pet sem reiniciar o programa.

## Exemplo de registro

```text
Pet: Luna | Vacina: Raiva | Dia: 2026-06-15
Pet: Thor | Vacina: V8 | Dia: 2026-06-18
Pet: Mel | Vacina: Giárdia | Dia: 2026-06-20
```
