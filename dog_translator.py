#!/usr/bin/env python3
"""
DogLanguage Interpreter
Executa código .dog diretamente em Python

Este tradutor lê código escrito na linguagem DogLanguage, tokeniza o texto, analisa a
estrutura sintática em comandos internos e interpreta cada comando em tempo de execução.

O fluxo principal é:
1. limpar comentários de linha do código DogLanguage;
2. converter o texto em tokens léxicos com a função tokenizar;
3. parsear esses tokens em uma árvore simples de comandos com parse_programa;
4. executar os comandos usando um interpretador que mantém escopos, funções,
   classes e instâncias;
5. oferecer suporte a importações de arquivos, controle de fluxo, métodos de classe,
   expressões, arrays, índices e casts básicos.

A implementação usa classes internas para representar ambientes (escopos), classes DogLanguage,
instâncias e o próprio interpretador, mantendo a semântica da linguagem Dog com suporte
a comandos como 'latir', 'farejar', 'pedigree' e construção de objetos.
"""

import os
import sys

class Ambiente:
    """Representa o ambiente de execução com variáveis"""
    # Cada ambiente pode ter um pai para formar uma cadeia de escopo.
    # Variáveis são procuradas primeiro no escopo atual e depois nos escopos ancestrais.
    def __init__(self, pai=None):
        self.pai = pai
        self.variaveis = {}

    def set(self, nome, valor):
        # Atribui um valor a uma variável no escopo atual.
        # Se a variável existir em um escopo pai, atualiza lá em vez de criar no escopo atual.
        if nome in self.variaveis:
            self.variaveis[nome] = valor
            return
        if self.pai and self.pai.existe(nome):
            self.pai.set(nome, valor)
            return
        self.variaveis[nome] = valor

    def get(self, nome):
        if nome in self.variaveis:
            return self.variaveis[nome]
        if self.pai:
            valor = self.pai.get(nome)
            if valor is not None:
                return valor
        return None

    def existe(self, nome):
        if nome in self.variaveis:
            return True
        if self.pai:
            return self.pai.existe(nome)
        return False

class DogClass:
    # Representa uma definição de classe em DogLanguage, armazenando campos, métodos e herança.
    def __init__(self, nome, campos, metodos, classe_pai=None):
        self.nome = nome
        self.classe_pai = classe_pai
        self.campos = {nome_campo: (valor if valor is not None else 0) for nome_campo, valor in campos}
        self.metodos = {}
        self.constructor = None
        for nome_metodo, params, corpo in metodos:
            if nome_metodo == 'instinto':
                self.constructor = (params, corpo)
            else:
                self.metodos[nome_metodo] = (params, corpo)
    
    def get_metodo(self, nome):
        """Busca método na classe ou em suas superclasses"""
        # Se não encontrar o método na classe atual, pesquisa recursivamente na classe pai.
        if nome in self.metodos:
            return self.metodos[nome]
        if self.classe_pai:
            return self.classe_pai.get_metodo(nome)
        return None
    
    def get_campos_herdados(self):
        """Retorna todos os campos incluindo os herdados"""
        campos = {}
        if self.classe_pai:
            campos.update(self.classe_pai.get_campos_herdados())
        campos.update(self.campos)
        return campos

class DogInstance:
    # Representa uma instância de uma classe DogLanguage, com seus próprios campos e acesso a métodos.
    def __init__(self, dog_class):
        self.dog_class = dog_class
        self.fields = dict(dog_class.get_campos_herdados())

    def get(self, nome):
        return self.fields.get(nome, 0)

    def set(self, nome, valor):
        self.fields[nome] = valor

    def call_method(self, nome, args, interpreter):
        # Executa um método de instância, criando um escopo temporário para a chamada.
        metodo_info = self.dog_class.get_metodo(nome)
        if not metodo_info:
            raise RuntimeError(f"Método '{nome}' não encontrado em {self.dog_class.nome}")
        params, corpo = metodo_info
        env = Ambiente(interpreter.ambiente_global)
        env.set('eu_mesmo', self)
        env.set('this', self)
        for idx, param in enumerate(params):
            env.set(param, args[idx] if idx < len(args) else 0)
        anterior = interpreter.ambiente_atual
        interpreter.ambiente_atual = env
        try:
            for c in corpo:
                resultado = executar_comando(c, interpreter)
                if isinstance(resultado, tuple) and resultado[0] == 'RETURN':
                    return resultado[1]
        finally:
            interpreter.ambiente_atual = anterior
        return None

class DogInterpreter:
    """Interpretador da linguagem Dog"""

    # Mantém o estado global da interpretação, incluindo funções, classes, escopos e arquivos importados.
    def __init__(self):
        self.ambiente_global = Ambiente()
        self.ambiente_atual = self.ambiente_global
        self.functions = {}
        self.classes = {}
        self.imported_files = set()
        self.builtins = {
            'latir': self.latir,
            'farejar': self.farejar,
            'enterrar': self.enterrar,
            'enterrar_mais': self.enterrar_mais,
            'cavar': self.cavar,
            'pedigree': self.cast_int,
            'pinscher': self.cast_int,
            'pelo': self.cast_str,
            'carne': self.cast_float,
            'raça': self.cast_float,
        }

    def latir(self, *args):
        # Função built-in equivalente a print, com suporte a formatação e escape de nova linha.
        if not args:
            print()
            return
        formato = str(args[0])
        try:
            if len(args) > 1:
                resultado = formato.replace('\\n', '\n')
                if '%' in resultado:
                    resultado = resultado % args[1:]
            else:
                resultado = formato.replace('\\n', '\n')
            print(resultado, end='')
        except (TypeError, ValueError):
            print(formato.replace('\\n', '\n'), end='')

    def farejar(self, prompt=""):
        # Função built-in que lê entrada do usuário, opcionalmente exibindo um prompt.
        try:
            if prompt:
                prompt_str = str(prompt).replace('\\n', '\n')
                return input(prompt_str)
            return input()
        except EOFError:
            return ""

    def enterrar(self, caminho, conteudo):
        # Grava texto em arquivo usando o caminho relativo ao diretório atual do programa.
        caminho = str(caminho)
        if not os.path.isabs(caminho):
            caminho = os.path.normpath(os.path.join(getattr(self, 'current_dir', os.getcwd()), caminho))
        diretorio = os.path.dirname(caminho)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        texto = str(conteudo).replace('\\n', '\n')
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(texto)
        return 1

    def enterrar_mais(self, caminho, conteudo):
        # Acrescenta texto ao final de um arquivo de log ou diário.
        caminho = str(caminho)
        if not os.path.isabs(caminho):
            caminho = os.path.normpath(os.path.join(getattr(self, 'current_dir', os.getcwd()), caminho))
        diretorio = os.path.dirname(caminho)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        texto = str(conteudo).replace('\\n', '\n')
        with open(caminho, 'a', encoding='utf-8') as f:
            f.write(texto)
        return 1

    def cavar(self, caminho):
        # Lê texto de arquivo usando o caminho relativo ao diretório atual do programa.
        caminho = str(caminho)
        if not os.path.isabs(caminho):
            caminho = os.path.normpath(os.path.join(getattr(self, 'current_dir', os.getcwd()), caminho))
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo '{caminho}' não encontrado")

    def cast_int(self, valor=0):
        try:
            return int(valor)
        except Exception:
            return 0

    def cast_str(self, valor=""):
        return str(valor)

    def cast_float(self, valor=0):
        try:
            return float(valor)
        except Exception:
            return 0.0

    def call_function(self, nome, args):
        # Chama uma função definida pelo usuário, criando um novo escopo para parâmetros e execução.
        if nome not in self.functions:
            return 0
        params, corpo = self.functions[nome]
        env = Ambiente(self.ambiente_global)
        for idx, param in enumerate(params):
            env.set(param, args[idx] if idx < len(args) else 0)
        anterior = self.ambiente_atual
        self.ambiente_atual = env
        try:
            for c in corpo:
                resultado = executar_comando(c, self)
                if isinstance(resultado, tuple) and resultado[0] == 'RETURN':
                    return resultado[1]
        finally:
            self.ambiente_atual = anterior
        return None

    def instantiate(self, nome_classe, args):
        if nome_classe not in self.classes:
            raise RuntimeError(f"Classe '{nome_classe}' não encontrada")
        dog_class = self.classes[nome_classe]
        instancia = DogInstance(dog_class)
        if dog_class.constructor:
            params, corpo = dog_class.constructor
            env = Ambiente(self.ambiente_global)
            env.set('eu_mesmo', instancia)
            env.set('this', instancia)
            for idx, param in enumerate(params):
                env.set(param, args[idx] if idx < len(args) else 0)
            anterior = self.ambiente_atual
            self.ambiente_atual = env
            try:
                for c in corpo:
                    resultado = executar_comando(c, self)
                    if isinstance(resultado, tuple) and resultado[0] == 'RETURN':
                        break
            finally:
                self.ambiente_atual = anterior
        return instancia


def tokenizar(codigo):
    """Tokeniza o código Dog"""
    # Converte o texto fonte em uma lista sequencial de tokens que representam palavras-chave,
    # literais e operadores, usada pelo parser para construir a estrutura de comandos.
    tokens = []
    i = 0

    while i < len(codigo):
        if codigo[i].isspace():
            i += 1
            continue

        if codigo[i] == '"':
            j = i + 1
            while j < len(codigo) and codigo[j] != '"':
                if codigo[j] == '\\':
                    j += 2
                else:
                    j += 1
            tokens.append(('STRING', codigo[i+1:j]))
            i = j + 1
            continue

        if codigo[i].isdigit():
            j = i
            while j < len(codigo) and (codigo[j].isdigit() or codigo[j] == '.'):
                j += 1
            num_str = codigo[i:j]
            tokens.append(('NUMERO', float(num_str) if '.' in num_str else int(num_str)))
            i = j
            continue

        if codigo[i].isalpha() or codigo[i] == '_':
            j = i
            while j < len(codigo) and (codigo[j].isalnum() or codigo[j] == '_'):
                j += 1
            palavra = codigo[i:j]
            palavras_chave_map = {
                'vira_lata': 'VAR',
                'pedigree': 'TYPE',
                'pelo': 'TYPE',
                'carne': 'TYPE',
                'raça': 'TYPE',
                'pinscher': 'TYPE',
                'funcao': 'FUNC',
                'uivar': 'FUNC',
                'latido': 'FUNC',
                'matilha': 'CLASS',
                'classe': 'CLASS',
                'novo': 'NEW',
                'eu_mesmo': 'SELF',
                'this': 'SELF',
                'dar_a_pata': 'IF',
                'se_tiver_petisco': 'IF',
                'ou_fingir_de_morto': 'ELSE',
                'ou_rosnar': 'ELSE',
                'focar_no_esquilo': 'WHILE',
                'perseguir': 'WHILE',
                'tentar_pegar': 'TRY',
                'fugiu_o_gato': 'CATCH',
                'trazer_bolinha': 'RETURN',
                'chamar_matilha': 'IMPORT',
                'extende': 'EXTENDS',
                'segue': 'EXTENDS',
            }
            tokens.append((palavras_chave_map.get(palavra, 'ID'), palavra))
            i = j
            continue

        if i + 1 < len(codigo):
            dois = codigo[i:i+2]
            if dois in ('==', '!=', '<=', '>='):
                tokens.append(('OP', dois))
                i += 2
                continue

        if codigo[i] in '+-*/%<>(){}[];,.=':
            tokens.append(('OP', codigo[i]))
            i += 1
            continue

        i += 1

    return tokens


def parse_programa(tokens):
    # Constrói uma representação interna do programa DogLanguage em comandos e expressões.
    # A função principal usa parsing recursivo descendente para traduzir tokens em instruções.
    pos = [0]

    def atual():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def proximo():
        pos[0] += 1

    def consume(tipo, valor=None):
        token = atual()
        if token and token[0] == tipo and (valor is None or token[1] == valor):
            proximo()
            return token
        return None

    def parse_bloco():
        # Analisa um bloco de código que começa em 'AU' e termina em 'UAU'.
        comandos = []
        if atual() and atual()[1] == 'AU':
            proximo()
        while atual() and atual()[1] != 'UAU':
            cmd = parse_comando()
            if cmd:
                comandos.append(cmd)
        if atual() and atual()[1] == 'UAU':
            proximo()
        return comandos

    def parse_parametros():
        params = []
        if atual() and atual()[1] == '(':
            proximo()
            while atual() and atual()[1] != ')':
                if atual()[0] == 'TYPE':
                    proximo()
                if atual() and atual()[0] == 'ID':
                    params.append(atual()[1])
                    proximo()
                if atual() and atual()[1] == ',':
                    proximo()
            if atual() and atual()[1] == ')':
                proximo()
        return params

    def parse_declaracao():
        nome = consume('ID')
        if not nome:
            return None
        valor = None
        if atual() and atual()[1] == '=':
            proximo()
            valor = parse_atribuicao()
        if atual() and atual()[1] == ';':
            proximo()
        return ('DECL', nome[1], valor)

    def parse_class_body():
        corpo = []
        while atual() and atual()[1] != 'UAU':
            if atual()[0] in ('VAR', 'TYPE'):
                proximo()
                decl = parse_declaracao()
                if decl:
                    corpo.append(decl)
                continue
            if atual()[0] == 'FUNC' or (atual()[0] == 'ID' and pos[0] + 1 < len(tokens) and tokens[pos[0] + 1][1] == '('):
                if atual()[0] == 'FUNC':
                    proximo()
                nome = consume('ID')
                params = parse_parametros()
                bloco = parse_bloco()
                if nome:
                    corpo.append(('FUNC_DEF', nome[1], params, bloco))
                continue
            proximo()
        return corpo

    def parse_comando():
        # Analisa um único comando de alto nível, incluindo declarações, funções,
        # classes, fluxo de controle e importações.
        token = atual()
        if not token:
            return None

        if token[0] == 'IMPORT':
            proximo()
            if atual() and atual()[0] == 'ID':
                nome_arquivo = atual()[1]
                proximo()
                if atual() and atual()[1] == ';':
                    proximo()
                return ('IMPORT', nome_arquivo)
            if atual() and atual()[1] == '<':
                proximo()
                nome_tokens = []
                while atual() and atual()[1] != '>':
                    nome_tokens.append(atual()[1])
                    proximo()
                if atual() and atual()[1] == '>':
                    proximo()
                nome_arquivo = ''.join(nome_tokens)
                return ('IMPORT', nome_arquivo)
            return None

        if token[0] in ('VAR', 'TYPE'):
            proximo()
            return parse_declaracao()

        if token[0] == 'FUNC':
            proximo()
            nome = consume('ID')
            params = parse_parametros()
            corpo = parse_bloco()
            return ('FUNC_DEF', nome[1] if nome else None, params, corpo)

        if token[0] == 'CLASS':
            proximo()
            nome = consume('ID')
            classe_pai = None
            # Skip 'AU' if it comes right after the class name
            if atual() and atual()[1] == 'AU':
                proximo()
            # Now check for 'extende'
            if atual() and atual()[0] == 'EXTENDS':
                proximo()
                pai_token = consume('ID')
                if pai_token:
                    classe_pai = pai_token[1]
            # Skip another 'AU' if present
            if atual() and atual()[1] == 'AU':
                proximo()
            corpo = parse_class_body()
            if atual() and atual()[1] == 'UAU':
                proximo()
            return ('CLASS_DEF', nome[1] if nome else None, corpo, classe_pai)

        if token[0] == 'IF':
            proximo()
            if atual() and atual()[1] == '(':
                proximo()
                condicao = parse_expressao()
                if atual() and atual()[1] == ')':
                    proximo()
                bloco = parse_bloco()
                else_bloco = None
                if atual() and atual()[0] == 'ELSE':
                    proximo()
                    else_bloco = parse_bloco()
                return ('IF', condicao, bloco, else_bloco)

        if token[0] == 'WHILE':
            proximo()
            if atual() and atual()[1] == '(':
                proximo()
                condicao = parse_expressao()
                if atual() and atual()[1] == ')':
                    proximo()
                bloco = parse_bloco()
                return ('WHILE', condicao, bloco)

        if token[0] == 'TRY':
            proximo()
            bloco = parse_bloco()
            catch_bloco = None
            if atual() and atual()[0] == 'CATCH':
                proximo()
                catch_bloco = parse_bloco()
            return ('TRY', bloco, catch_bloco)

        if token[0] == 'RETURN':
            proximo()
            valor = parse_expressao()
            if atual() and atual()[1] == ';':
                proximo()
            return ('RETURN', valor)

        expr = parse_atribuicao()
        if atual() and atual()[1] == ';':
            proximo()
        return expr

    def parse_atribuicao():
        expr = parse_equality()
        if atual() and atual()[1] == '=' and isinstance(expr, tuple) and expr[0] in ('VAR', 'FIELD', 'INDEX'):
            proximo()
            valor = parse_atribuicao()
            return ('ASSIGN', expr, valor)
        return expr

    def parse_expressao():
        return parse_equality()

    def parse_equality():
        expr = parse_comparison()
        while atual() and atual()[0] == 'OP' and atual()[1] in ('==', '!='):
            op = atual()[1]
            proximo()
            direita = parse_comparison()
            expr = ('BINOP', op, expr, direita)
        return expr

    def parse_comparison():
        expr = parse_termo()
        while atual() and atual()[0] == 'OP' and atual()[1] in ('<', '>', '<=', '>='):
            op = atual()[1]
            proximo()
            direita = parse_termo()
            expr = ('BINOP', op, expr, direita)
        return expr

    def parse_termo():
        expr = parse_fator()
        while atual() and atual()[0] == 'OP' and atual()[1] in ('+', '-'):
            op = atual()[1]
            proximo()
            direita = parse_fator()
            expr = ('BINOP', op, expr, direita)
        return expr

    def parse_fator():
        expr = parse_unario()
        while atual() and atual()[0] == 'OP' and atual()[1] in ('*', '/', '%'):
            op = atual()[1]
            proximo()
            direita = parse_unario()
            expr = ('BINOP', op, expr, direita)
        return expr

    def parse_unario():
        if atual() and atual()[0] == 'OP' and atual()[1] == '-':
            proximo()
            valor = parse_unario()
            return ('NEG', valor)
        return parse_primary()

    def parse_primary():
        # Analisa a parte mais básica de uma expressão, como literais, variáveis,
        # chamadas, novos objetos e acessos a campos/índices.
        token = atual()
        if not token:
            return 0

        def parse_postfix(expr):
            while atual() and atual()[1] in ('.', '['):
                if atual()[1] == '.':
                    proximo()
                    atributo = consume('ID')
                    if not atributo:
                        break
                    if atual() and atual()[1] == '(':
                        proximo()
                        args = []
                        while atual() and atual()[1] != ')':
                            args.append(parse_expressao())
                            if atual() and atual()[1] == ',':
                                proximo()
                        if atual() and atual()[1] == ')':
                            proximo()
                        expr = ('CALL', ('FIELD', expr, atributo[1]), args)
                    else:
                        expr = ('FIELD', expr, atributo[1])
                else:
                    proximo()
                    index = parse_expressao()
                    if atual() and atual()[1] == ']':
                        proximo()
                    expr = ('INDEX', expr, index)
            return expr

        if token[1] == '[':
            proximo()
            elements = []
            while atual() and atual()[1] != ']':
                elements.append(parse_expressao())
                if atual() and atual()[1] == ',':
                    proximo()
            if atual() and atual()[1] == ']':
                proximo()
            return parse_postfix(('ARRAY', elements))

        if token[0] == 'NUMERO':
            proximo()
            return token[1]

        if token[0] == 'STRING':
            proximo()
            return token[1]

        if token[0] == 'SELF':
            proximo()
            expr = ('SELF',)
            return parse_postfix(expr)

        if token[0] == 'NEW':
            proximo()
            nome_classe = consume('ID')
            args = []
            if atual() and atual()[1] == '(':
                proximo()
                while atual() and atual()[1] != ')':
                    args.append(parse_expressao())
                    if atual() and atual()[1] == ',':
                        proximo()
                if atual() and atual()[1] == ')':
                    proximo()
            return ('NEW', nome_classe[1] if nome_classe else None, args)

        if token[0] in ('ID', 'TYPE'):
            nome = token[1]
            proximo()
            expr = ('VAR', nome)
            if atual() and atual()[1] == '(':
                proximo()
                args = []
                while atual() and atual()[1] != ')':
                    args.append(parse_expressao())
                    if atual() and atual()[1] == ',':
                        proximo()
                if atual() and atual()[1] == ')':
                    proximo()
                expr = ('CALL', nome, args)
            return parse_postfix(expr)

        if token[1] == '(':
            proximo()
            valor = parse_expressao()
            if atual() and atual()[1] == ')':
                proximo()
            return valor

        proximo()
        return 0

    comandos = []
    while pos[0] < len(tokens):
        cmd = parse_comando()
        if cmd:
            comandos.append(cmd)
    return comandos


def executar_comando(cmd, interpreter):
    # Executa um comando da AST no interpretador, atualizando variáveis,
    # controlando o fluxo e chamando funções ou métodos conforme necessário.
    if not cmd:
        return None

    tipo_cmd = cmd[0]

    if tipo_cmd == 'DECL':
        nome, valor = cmd[1], avaliar_expr(cmd[2], interpreter) if cmd[2] is not None else 0
        interpreter.ambiente_atual.set(nome, valor)
        return None

    if tipo_cmd == 'ASSIGN':
        alvo, valor = cmd[1], avaliar_expr(cmd[2], interpreter)
        if alvo[0] == 'VAR':
            interpreter.ambiente_atual.set(alvo[1], valor)
            return None
        if alvo[0] == 'FIELD':
            base = avaliar_expr(alvo[1], interpreter)
            if isinstance(base, DogInstance):
                base.set(alvo[2], valor)
                return None
            if isinstance(base, dict):
                base[alvo[2]] = valor
                return None
            raise RuntimeError(f"Não é possível atribuir campo em {base}")
        if alvo[0] == 'INDEX':
            base = avaliar_expr(alvo[1], interpreter)
            indice = avaliar_expr(alvo[2], interpreter)
            if isinstance(base, list):
                base[indice] = valor
                return None
            if isinstance(base, dict):
                base[indice] = valor
                return None
            raise RuntimeError(f"Não é possível atribuir índice em {base}")

    if tipo_cmd == 'IF':
        condicao, bloco, else_bloco = cmd[1], cmd[2], cmd[3]
        if avaliar_expr(condicao, interpreter):
            for c in bloco:
                resultado = executar_comando(c, interpreter)
                if resultado is not None:
                    return resultado
        elif else_bloco:
            for c in else_bloco:
                resultado = executar_comando(c, interpreter)
                if resultado is not None:
                    return resultado
        return None

    if tipo_cmd == 'WHILE':
        condicao, bloco = cmd[1], cmd[2]
        while avaliar_expr(condicao, interpreter):
            for c in bloco:
                resultado = executar_comando(c, interpreter)
                if resultado is not None:
                    return resultado
        return None

    if tipo_cmd == 'TRY':
        try:
            for c in cmd[1]:
                resultado = executar_comando(c, interpreter)
                if resultado is not None:
                    return resultado
        except Exception:
            if cmd[2]:
                for c in cmd[2]:
                    resultado = executar_comando(c, interpreter)
                    if resultado is not None:
                        return resultado
        return None

    if tipo_cmd == 'RETURN':
        return ('RETURN', avaliar_expr(cmd[1], interpreter))

    if tipo_cmd == 'FUNC_DEF':
        nome, params, corpo = cmd[1], cmd[2], cmd[3]
        interpreter.functions[nome] = (params, corpo)
        return None

    if tipo_cmd == 'CLASS_DEF':
        nome, corpo = cmd[1], cmd[2]
        classe_pai = cmd[3] if len(cmd) > 3 else None
        campos = []
        metodos = []
        for item in corpo:
            if item and item[0] == 'DECL':
                campos.append((item[1], item[2]))
            elif item and item[0] == 'FUNC_DEF':
                metodos.append((item[1], item[2], item[3]))
        
        # Busca referência da classe pai se existir
        classe_pai_obj = None
        if classe_pai:
            if classe_pai not in interpreter.classes:
                raise RuntimeError(f"Classe pai '{classe_pai}' não encontrada")
            classe_pai_obj = interpreter.classes[classe_pai]
        
        interpreter.classes[nome] = DogClass(nome, campos, metodos, classe_pai_obj)
        return None

    if tipo_cmd == 'IMPORT':
        nome_arquivo = cmd[1]
        if not nome_arquivo.endswith('.dog'):
            nome_arquivo = f"{nome_arquivo}.dog"
        if not os.path.isabs(nome_arquivo):
            base_dir = getattr(interpreter, 'current_dir', os.getcwd())
            nome_arquivo = os.path.normpath(os.path.join(base_dir, nome_arquivo))
        if nome_arquivo in interpreter.imported_files:
            return None
        interpreter.imported_files.add(nome_arquivo)
        previous_dir = getattr(interpreter, 'current_dir', None)
        interpreter.current_dir = os.path.dirname(nome_arquivo)
        try:
            try:
                with open(nome_arquivo, 'r', encoding='utf-8') as f:
                    codigo_importado = f.read()
            except FileNotFoundError:
                raise RuntimeError(f"Arquivo de import '{nome_arquivo}' não encontrado")
            tokens_importado = tokenizar(codigo_importado)
            comandos_importado = parse_programa(tokens_importado)
            for c in comandos_importado:
                resultado = executar_comando(c, interpreter)
                if isinstance(resultado, tuple) and resultado[0] == 'RETURN':
                    break
        finally:
            interpreter.current_dir = previous_dir
        return None

    if tipo_cmd == 'CALL':
        avaliar_expr(cmd, interpreter)
        return None

    return None


def avaliar_expr(expr, interpreter):
    # Avalia uma expressão recursivamente usando o ambiente atual e retorna o valor calculado.
    # Suporta variáveis, campos, arrays, chamadas, operações binárias e objetos.
    if isinstance(expr, (int, float, str)):
        return expr

    if isinstance(expr, tuple):
        if expr[0] == 'VAR':
            valor = interpreter.ambiente_atual.get(expr[1])
            return valor if valor is not None else 0

        if expr[0] == 'FIELD':
            base = avaliar_expr(expr[1], interpreter)
            if isinstance(base, DogInstance):
                return base.get(expr[2])
            if isinstance(base, dict):
                return base.get(expr[2], 0)
            return 0

        if expr[0] == 'SELF':
            return interpreter.ambiente_atual.get('eu_mesmo') or interpreter.ambiente_atual.get('this')

        if expr[0] == 'ARRAY':
            return [avaliar_expr(item, interpreter) for item in expr[1]]

        if expr[0] == 'CALL':
            destino = expr[1]
            args = [avaliar_expr(arg, interpreter) for arg in expr[2]]
            if isinstance(destino, tuple) and destino[0] == 'FIELD':
                objeto = avaliar_expr(destino[1], interpreter)
                if isinstance(objeto, DogInstance):
                    return objeto.call_method(destino[2], args, interpreter)
                raise RuntimeError(f"{objeto} não é um objeto para chamar método {destino[2]}")
            if destino in interpreter.builtins:
                return interpreter.builtins[destino](*args)
            self_obj = interpreter.ambiente_atual.get('eu_mesmo') or interpreter.ambiente_atual.get('this')
            if isinstance(self_obj, DogInstance) and self_obj.dog_class.get_metodo(destino):
                return self_obj.call_method(destino, args, interpreter)
            return interpreter.call_function(destino, args)

        if expr[0] == 'INDEX':
            base = avaliar_expr(expr[1], interpreter)
            indice = avaliar_expr(expr[2], interpreter)
            if isinstance(base, list):
                try:
                    return base[indice]
                except Exception:
                    return 0
            if isinstance(base, dict):
                return base.get(indice, 0)
            if isinstance(base, str):
                try:
                    return base[indice]
                except Exception:
                    return ''
            return 0

        if expr[0] == 'NEW':
            nome_classe = expr[1]
            args = [avaliar_expr(arg, interpreter) for arg in expr[2]]
            return interpreter.instantiate(nome_classe, args)

        if expr[0] == 'BINOP':
            op = expr[1]
            esq = avaliar_expr(expr[2], interpreter)
            dir = avaliar_expr(expr[3], interpreter)
            if op == '+':
                return esq + dir
            if op == '-':
                return esq - dir
            if op == '*':
                return esq * dir
            if op == '/':
                return esq / dir if dir != 0 else 0
            if op == '%':
                return esq % dir if dir != 0 else 0
            if op == '==':
                return esq == dir
            if op == '!=':
                return esq != dir
            if op == '<':
                return esq < dir
            if op == '>':
                return esq > dir
            if op == '<=':
                return esq <= dir
            if op == '>=':
                return esq >= dir

        if expr[0] == 'NEG':
            return -avaliar_expr(expr[1], interpreter)

    return 0


def executar(codigo_dog, arquivo=None):
    # Função de entrada principal para interpretar código DogLanguage em texto.
    # Remove comentários em linha, tokeniza, parseia e executa o programa completo.
    try:
        linhas_limpas = []
        for linha in codigo_dog.split('\n'):
            if '//' in linha:
                linha = linha[:linha.index('//')]
            linhas_limpas.append(linha)
        codigo = '\n'.join(linhas_limpas)
        tokens = tokenizar(codigo)
        comandos = parse_programa(tokens)
        interpreter = DogInterpreter()
        if arquivo:
            interpreter.current_dir = os.path.dirname(os.path.abspath(arquivo))
        else:
            interpreter.current_dir = os.getcwd()
        for cmd in comandos:
            resultado = executar_comando(cmd, interpreter)
            if isinstance(resultado, tuple) and resultado[0] == 'RETURN':
                break
        if 'canil' in interpreter.functions:
            interpreter.call_function('canil', [])
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Uso: python dog_translator.py arquivo.dog")
        print("Executa código DogLanguage diretamente")
        sys.exit(1)

    arquivo = sys.argv[1]
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo_dog = f.read()
    except FileNotFoundError:
        print(f"❌ Erro: arquivo '{arquivo}' não encontrado", file=sys.stderr)
        sys.exit(1)
    executar(codigo_dog, arquivo)

if __name__ == "__main__":
    main()
