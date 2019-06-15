#Vinícius Dotto de Arruda Figueiredo
#Analisador Sintatico da Linguagem Lalg

from lexicoCompII import *

def check(tokens):
    if not tokens:
        print("Cadeia incompleta")
        exit()

def erro(item, esperado):
    print("Erro de sintaxe na linha " + str(item.line) + ", o valor esperado era: " + str(esperado) + " Mas a entrada encontrada foi: " + str(item.value))
    exit()

def programa(tokens):
    if tokens == 0:
    	exit()
    else:
    	check(tokens)
    	item = tokens.pop(0)
    	if item.value != 'program':
    		erro(item, "program")
    	check(tokens)
    	item = tokens.pop(0)
    	if item.type != 'ident':
    		erro(item, "tipo identificador")
    	corpo(tokens)
    	check(tokens)
    	item = tokens.pop(0)
    	if item.value != '.':
    		erro(item, ".")
    	print ("\n Analisador Sintatico não encontrou nenhum erro")

def corpo(tokens):
	dc(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != 'begin':
		erro(item, "begin")
	comandos(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != 'end':
		erro(item, "end")

def dc(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value == 'var':
		dc_v(tokens)
		mais_dc(tokens)
		return
	if item.value == 'procedure':
		dc_p(tokens)
		mais_dc(tokens)
		return
	return

def mais_dc(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != ';':
		return
	tokens.pop(0)
	dc(tokens)

def dc_v(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.value != 'var':
		erro(item, 'var')
	variaveis(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != ':':
		erro(item, ':')
	tipo_var(tokens)

def tipo_var(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.value not in("integer","real"):
		erro (item, "integer ou real")

def variaveis(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.type != 'ident':
		erro(item, "tipo identificador")
	mais_var(tokens)

def mais_var(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != ',':
		return
	tokens.pop(0)
	variaveis(tokens)

def dc_p(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.value != 'procedure':
		erro(item, "procedure")
	check(tokens)
	item = tokens.pop(0)
	if item.type != 'ident':
		erro(item, "tipo identificador")
	parametros(tokens)
	corpo_p(tokens)

def parametros(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != '(':
		return
	tokens.pop(0)
	lista_par(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != ')':
		erro(item, ")")

def lista_par(tokens):
	variaveis(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != ':':
		erro(item, ":")
	tipo_var(tokens)
	mais_par(tokens)

def mais_par(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != ';':
		return
	tokens.pop(0)
	lista_par(tokens)

def corpo_p(tokens):
	dc_loc(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != 'begin':
		erro(item, "begin")
	comandos(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != 'end':
		erro(item, "end")

def dc_loc(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != 'var':
		return
	dc_v(tokens)
	mais_dcloc(tokens)

def mais_dcloc(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != ';':
		return
	tokens.pop(0)
	dc_loc(tokens)

def lista_arg(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != '(':
		return
	tokens.pop(0)
	argumentos(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != ')':
		erro(item, ")")

def argumentos(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.type != 'ident':
		erro(item, "ident")
	mais_ident(tokens)

def mais_ident(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != ';':
		return
	tokens.pop(0)
	argumentos(tokens)

def p_falsa(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != 'else':
		return
	tokens.pop(0)
	comandos(tokens)

def comandos(tokens):
	comando(tokens)
	mais_comandos(tokens)

def mais_comandos(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != ';':
		return
	tokens.pop(0)
	comandos(tokens)

def comando(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.value == 'read' or item.value == 'write':
		check(tokens)
		item = tokens.pop(0)
		if item.value != '(':
			erro(item, "(")
		variaveis(tokens)
		check(tokens)
		item = tokens.pop(0)
		if item.value != ')':
			erro(item, ")")
		return
	if item.value == 'while':
		condicao(tokens)
		check(tokens)
		item = tokens.pop(0)
		if item.value != 'do':
			erro(item, "do")
		comandos(tokens)
		check(tokens)
		item = tokens.pop(0)
		if item.value != '$':
			erro(item, "$")
		return
	if item.value == 'if':
		condicao(tokens)
		check(tokens)
		item = tokens.pop(0)
		if item.value != 'then':
			erro(item, "then")
		comandos(tokens)
		p_falsa(tokens)
		check(tokens)
		item = tokens.pop(0)
		if item.value != '$':
			erro(item, "$")
		return
	if item.type == 'ident':
		restoldent(tokens)
		return
	erro(item, "read , write, while, if ou tipo idenficador")

def restoldent(tokens):
	check(tokens)
	item = tokens[0]
	if item.value == ':=':
		tokens.pop(0)
		expressao(tokens)
		return
	lista_arg(tokens)

def condicao(tokens):
	expressao(tokens)
	relacao(tokens)
	expressao(tokens)

def relacao(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.value in relacionais:
		return
	erro (item, "tipo relacional")

def expressao(tokens):
	termo(tokens)
	outros_termos(tokens)

def op_un(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value == '+' or item.value == '-':
		tokens.pop(0)
	return

def outros_termos(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value == '+' or item.value == '-':
		op_ad(tokens)
		termo(tokens)
		outros_termos(tokens)
	return

def op_ad(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.value != '+' and item.value != '-':
		erro(item, "+ ou -")

def termo(tokens):
	op_un(tokens)
	fator(tokens)
	mais_fatores(tokens)

def mais_fatores(tokens):
	if not tokens:
		return
	item = tokens[0]
	if item.value != '*' and item.value != '/':
		return
	op_mul(tokens)
	fator(tokens)
	mais_fatores(tokens)

def op_mul(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.value != '*' and item.value != '/':
		erro(item, "* ou /")

def fator(tokens):
	check(tokens)
	item = tokens.pop(0)
	if item.type == 'ident':
		return
	if item.type == 'numero_int':
		return
	if item.type == 'numero_real':
		return
	if item.value == '(':
		expressao(tokens)
		check(tokens)
		item = tokens.pop(0)
		if item.value != ')':
			erro(item, ")")
		return
	erro(item, "ident ou numero_real ou numero_int ou (")

if __name__ == '__main__':
    programa(lexico())



		