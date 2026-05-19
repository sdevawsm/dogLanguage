#!/usr/bin/env python3
"""
DogLanguage Interpreter
Executa código .dog diretamente em Python
"""

import sys
import re

class Ambiente:
    """Representa o ambiente de execução com variáveis"""
    def __init__(self, pai=None):
        self.pai = pai
        self.variaveis = {}
    
    def set(self, nome, valor):
        self.variaveis[nome] = valor
    
    def get(self, nome):
        if nome in self.variaveis:
            return self.variaveis[nome]
        if self.pai:
            return self.pai.get(nome)
        return None
    
    def existe(self, nome):
        if nome in self.variaveis:
            return True
        if self.pai:
            return self.pai.existe(nome)
        return False

class DogInterpreter:
    """Interpretador da linguagem Dog"""
    
    def __init__(self):
        self.ambiente_global = Ambiente()
        self.ambiente_atual = self.ambiente_global
    
    def latir(self, *args):
        """Equivalente a print/printf"""
        if not args:
            print()
            return
        
        formato = str(args[0])
        
        # Tenta substituir especificadores de formato C
        try:
            if len(args) > 1:
                # Remove \n para processamento
                resultado = formato.replace('\\n', '\n')
                # Tenta substituição simples com %
                if '%' in resultado:
                    resultado = resultado % args[1:]
            else:
                resultado = formato.replace('\\n', '\n')
            
            print(resultado, end='')
        except (TypeError, ValueError):
            print(formato.replace('\\n', '\n'), end='')
    
    def farejar(self, prompt=""):
        """Equivalente a input/scanf"""
        try:
            if prompt:
                prompt_str = str(prompt).replace('\\n', '\n')
                return input(prompt_str)
            return input()
        except EOFError:
            return ""

def tokenizar(codigo):
    """Tokeniza o código Dog"""
    tokens = []
    i = 0
    
    while i < len(codigo):
        # Pula espaços em branco
        if codigo[i].isspace():
            i += 1
            continue
        
        # String com aspas
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
        
        # Números
        if codigo[i].isdigit():
            j = i
            while j < len(codigo) and (codigo[j].isdigit() or codigo[j] == '.'):
                j += 1
            num_str = codigo[i:j]
            if '.' in num_str:
                tokens.append(('NUMERO', float(num_str)))
            else:
                tokens.append(('NUMERO', int(num_str)))
            i = j
            continue
        
        # Identificadores e palavras-chave
        if codigo[i].isalpha() or codigo[i] == '_':
            j = i
            while j < len(codigo) and (codigo[j].isalnum() or codigo[j] == '_'):
                j += 1
            palavra = codigo[i:j]
            
            palavras_chave_map = {
                'canil': 'CANIL',
                'latir': 'LATIR',
                'vira_lata': 'VAR',
                'pedigree': 'PEDIGREE',
                'AU': 'ABRE',
                'UAU': 'FECHA',
                'trazer_bolinha': 'RET',
                'dar_a_pata': 'SE',
                'ou_fingir_de_morto': 'SENAO',
                'focar_no_esquilo': 'ENQUANTO',
                'chamar_matilha': 'IMPORT',
            }
            
            if palavra in palavras_chave_map:
                tokens.append((palavras_chave_map[palavra], palavra))
            else:
                tokens.append(('ID', palavra))
            
            i = j
            continue
        
        # Operadores
        if i + 1 < len(codigo):
            dois = codigo[i:i+2]
            if dois in ('==', '!=', '<=', '>='):
                tokens.append(('OP', dois))
                i += 2
                continue
        
        if codigo[i] in '+-*/<>(){}[];,.=':
            tokens.append(('OP', codigo[i]))
            i += 1
            continue
        
        i += 1
    
    return tokens

def parse_programa(tokens):
    """Faz parse do programa"""
    pos = [0]  # Usando lista para passar por referência
    
    def atual():
        return tokens[pos[0]] if pos[0] < len(tokens) else None
    
    def proximo():
        pos[0] += 1
    
    def consume(tipo):
        token = atual()
        if token and token[0] == tipo:
            proximo()
            return token
        return None
    
    def parse_bloco():
        """Parse de um bloco de código"""
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
    
    def parse_comando():
        """Parse de um comando"""
        token = atual()
        
        if not token:
            return None
        
        if token[0] == 'VAR':
            proximo()
            var_name = consume('ID')
            if var_name:
                if atual() and atual()[1] == '=':
                    proximo()
                    valor = parse_expressao()
                    consume('OP')  # consome ; se existir
                    return ('VAR', var_name[1], valor)
        
        elif token[0] == 'LATIR':
            proximo()
            if atual() and atual()[1] == '(':
                proximo()
                args = []
                while atual() and atual()[1] != ')':
                    args.append(parse_expressao())
                    if atual() and atual()[1] == ',':
                        proximo()
                if atual() and atual()[1] == ')':
                    proximo()
                consume('OP')  # consome ; se existir
                return ('LATIR', args)
        
        elif token[0] == 'ID':
            nome = token[1]
            proximo()
            if atual() and atual()[1] == '=':
                proximo()
                valor = parse_expressao()
                consume('OP')  # consome ; se existir
                return ('ATRIB', nome, valor)
        
        elif token[0] == 'SE':
            proximo()
            if atual() and atual()[1] == '(':
                proximo()
                condicao = parse_expressao()
                if atual() and atual()[1] == ')':
                    proximo()
                bloco = parse_bloco()
                return ('SE', condicao, bloco)
        
        elif token[0] == 'ENQUANTO':
            proximo()
            if atual() and atual()[1] == '(':
                proximo()
                condicao = parse_expressao()
                if atual() and atual()[1] == ')':
                    proximo()
                bloco = parse_bloco()
                return ('ENQUANTO', condicao, bloco)
        
        elif token[0] == 'RET':
            proximo()
            valor = parse_expressao()
            return ('RET', valor)
        
        elif token[0] == 'IMPORT':
            proximo()
            consume('OP')
            while atual() and atual()[1] != '>':
                proximo()
            if atual():
                proximo()
            return None
        
        else:
            proximo()
            return None
    
    def parse_expressao():
        """Parse de expressão"""
        esq = parse_termo()
        
        while atual() and atual()[0] == 'OP' and atual()[1] in ('==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/'):
            op = atual()[1]
            proximo()
            dir = parse_termo()
            esq = ('BINOP', op, esq, dir)
        
        return esq
    
    def parse_termo():
        """Parse de um termo"""
        token = atual()
        
        if not token:
            return 0
        
        if token[0] == 'NUMERO':
            proximo()
            return token[1]
        
        if token[0] == 'STRING':
            proximo()
            return token[1]
        
        if token[0] == 'ID':
            proximo()
            return ('VAR', token[1])
        
        if token[1] == '(':
            proximo()
            valor = parse_expressao()
            if atual() and atual()[1] == ')':
                proximo()
            return valor
        
        proximo()
        return 0
    
    # Parse do programa
    comandos = []
    while pos[0] < len(tokens):
        cmd = parse_comando()
        if cmd:
            comandos.append(cmd)
    
    return comandos

def executar_comando(cmd, interpreter):
    """Executa um comando"""
    if not cmd:
        return None
    
    tipo_cmd = cmd[0]
    
    if tipo_cmd == 'VAR':
        nome, valor = cmd[1], avaliar_expr(cmd[2], interpreter)
        interpreter.ambiente_atual.set(nome, valor)
    
    elif tipo_cmd == 'LATIR':
        args = [avaliar_expr(arg, interpreter) for arg in cmd[1]]
        interpreter.latir(*args)
    
    elif tipo_cmd == 'ATRIB':
        nome, valor = cmd[1], avaliar_expr(cmd[2], interpreter)
        interpreter.ambiente_atual.set(nome, valor)
    
    elif tipo_cmd == 'SE':
        condicao, bloco = cmd[1], cmd[2]
        if avaliar_expr(condicao, interpreter):
            for c in bloco:
                resultado = executar_comando(c, interpreter)
                if resultado == 'RET':
                    return 'RET'
    
    elif tipo_cmd == 'ENQUANTO':
        condicao, bloco = cmd[1], cmd[2]
        while avaliar_expr(condicao, interpreter):
            for c in bloco:
                resultado = executar_comando(c, interpreter)
                if resultado == 'RET':
                    return 'RET'
    
    elif tipo_cmd == 'RET':
        return 'RET'
    
    return None

def avaliar_expr(expr, interpreter):
    """Avalia uma expressão"""
    if isinstance(expr, (int, float, str)):
        return expr
    
    if isinstance(expr, tuple):
        if expr[0] == 'VAR':
            valor = interpreter.ambiente_atual.get(expr[1])
            return valor if valor is not None else 0
        
        elif expr[0] == 'BINOP':
            op = expr[1]
            esq = avaliar_expr(expr[2], interpreter)
            dir = avaliar_expr(expr[3], interpreter)
            
            if op == '+':
                return esq + dir
            elif op == '-':
                return esq - dir
            elif op == '*':
                return esq * dir
            elif op == '/':
                return esq / dir if dir != 0 else 0
            elif op == '==':
                return esq == dir
            elif op == '!=':
                return esq != dir
            elif op == '<':
                return esq < dir
            elif op == '>':
                return esq > dir
            elif op == '<=':
                return esq <= dir
            elif op == '>=':
                return esq >= dir
    
    return 0

def executar(codigo_dog):
    """Executa código Dog"""
    try:
        # Remove comentários
        linhas_limpas = []
        for linha in codigo_dog.split('\n'):
            if '//' in linha:
                linha = linha[:linha.index('//')]
            linhas_limpas.append(linha)
        
        codigo = '\n'.join(linhas_limpas)
        
        # Tokeniza
        tokens = tokenizar(codigo)
        
        # Parse
        comandos = parse_programa(tokens)
        
        # Executa
        interpreter = DogInterpreter()
        for cmd in comandos:
            resultado = executar_comando(cmd, interpreter)
            if resultado == 'RET':
                break
    
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Função principal"""
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
    
    # Executa
    executar(codigo_dog)

if __name__ == "__main__":
    main()
