#Vinícius Dotto de Arruda Figueiredo
#Analisador Sintatico da Linguagem Lalg

from lexicoCompII import *
from operator import itemgetter

escopoAtual= "main"
tabela={"main":{}}
aux_var = []
contador = 0
contador_aux = 0
aux_tipo = None
aux_funcao = ""
aux_argumento=[]
ident_aux = None
categoria = ""
aux_read = []
aux_write = []

def buscaTS(cadeia):    
	return cadeia in tabela[escopoAtual]

def buscaGlobalTS(cadeia):    
	return cadeia in tabela["main"]

def buscaEscopoTS(cadeia, escopo):    
	return cadeia in tabela[escopo]

def VerificaParametros():
	global aux_argumento
	global escopoAtual
	global tabela
	global ident_aux
	tabelaAux = tabela[ident_aux]
	listaAux = []
	for linha in tabelaAux:
		if "parametro" in tabelaAux[linha]:
			listaAux.append(tabelaAux[linha])
	listaAux = sorted(listaAux, key=itemgetter(-1))
	if len(listaAux) != len(aux_argumento):
		exit("Parâmetros esperados: {}; Parâmetros recebidos: {}".format(len(listaAux),len(aux_argumento)))
	else:
		print (listaAux)
		print ("\n")
		print (aux_argumento)
		for a,b in zip(listaAux, aux_argumento):
			if not a[2] == b[2]:
				exit("Tipo de parâmetro recebido: {}; Parâmetro esperado: {}".format(b[2],a[2]))
	aux_argumento.clear()

def NovoEscopo(nomedoEscopo):
	tabela[nomedoEscopo] = {}

def inserirTS(cadeia, token, tipo,  escopo, cont):
	global escopoAtual
	global categoria
	if buscaTS(cadeia):
		print("Tabela de Símbolos:\n")
		for i in tabela.items():
			print("Escopo: {}".format(i[0]))
			print("Variáveis:{}\n".format(i[1]))
		exit("Variavél {}, já declarada no escopo: {}".format(cadeia,escopo))
	tabela[escopoAtual][cadeia] = ([token, categoria, tipo, escopoAtual, cont])

def insertVarTS(tipo):
	global aux_var
	global escopoAtual
	global contador_aux
	global contador
	for variavel in aux_var:
		if escopoAtual == "main":
			inserirTS(variavel.value, variavel.type, tipo, escopoAtual, cont=contador)
			contador += 1
		else:
			inserirTS(variavel.value, variavel.type, tipo , escopoAtual, cont=contador_aux)
			contador_aux += 1
	aux_var.clear()  

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
		print("Tabela de Símbolos:\n")
		for i in tabela.items():
			print("Escopo: {}".format(i[0]))
			print("Variáveis:{}\n".format(i[1]))

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
	global categoria
	if not tokens:
		return
	item = tokens[0]
	if item.value == 'var':
		categoria = "var"
		dc_v(tokens)
		mais_dc(tokens)
		return
	if item.value == 'procedure':
		categoria = "procedure"
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
	global escopoAtual
	global contador
	global contador_aux
	global aux_var
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
	global aux_var
	global escopoAtual
	check(tokens)
	item = tokens.pop(0)
	if item.value not in("integer","real"):
		erro (item, "integer ou real")
	print (item.value)
	insertVarTS(item.value)


def variaveis(tokens):
	global escopoAtual
	global contador
	global contador_aux
	global aux_var
	check(tokens)
	item = tokens.pop(0)
	if item.type != 'ident':
		erro(item, "tipo identificador")
	aux_var.append(item)
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
	global categoria
	global escopoAtual
	global contador
	check(tokens)
	item = tokens.pop(0)
	if item.value != 'procedure':
		erro(item, "procedure")
	categoria = "procedure"
	check(tokens)
	item = tokens.pop(0)
	if item.type != 'ident':
		erro(item, "tipo identificador")
	inserirTS(item.value, item.type, None, escopoAtual, cont=contador)
	escopoAtual = item.value
	NovoEscopo(escopoAtual)
	parametros(tokens)
	corpo_p(tokens)

def parametros(tokens):
	global categoria
	if not tokens:
		return
	item = tokens[0]
	if item.value != '(':
		return
	categoria = "parametro"
	tokens.pop(0)
	lista_par(tokens)
	check(tokens)
	item = tokens.pop(0)
	if item.value != ')':
		erro(item, ")")

def lista_par(tokens):
	global categoria
	categoria = "parametro"
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
	global categoria
	global escopoAtual
	global aux_var
	categoria = "var"
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
	aux_var.clear()
	escopoAtual = "main"

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
	VerificaParametros()
	check(tokens)
	item = tokens.pop(0)
	if item.value != ')':
		erro(item, ")")

def argumentos(tokens):
	global aux_argumento
	global tabela
	global escopoAtual
	global ident_aux
	check(tokens)
	item = tokens.pop(0)
	if item.type != 'ident':
		erro(item, "ident")
	if not buscaEscopoTS(item.value, ident_aux):
			if not buscaGlobalTS(item.value):
				exit("Variavel {} na linha {}, não declarada.".format(item.value,item.line+1))
	if escopoAtual == 'main':
		if buscaGlobalTS(item.value):
			aux_argumento.append(tabela["main"][item.value])
	else:
		if buscaEscopoTS(item.value,ident_aux):
			aux_argumento.append(tabela[ident_aux][item.value])
			print ("aqui")
			print (tabela[ident_aux][item.value])
	
	print ("inserido")
	print (aux_argumento)
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
	global aux_tipo
	global aux_var
	global ident_aux
	global aux_read
	global escopoAtual
	global aux_write
	check(tokens)
	item = tokens[0]
	if item.value == 'read':
		tokens.pop(0)
		check(tokens)
		item = tokens.pop(0)
		if item.value != '(':
			erro(item, "(")
		variaveis(tokens)
		for i in aux_var:
			if(buscaTS(i.value)):
				aux_read.append(tabela[escopoAtual][i.value])
			elif(buscaGlobalTS(i.value)):
				aux_read.append(tabela["main"][i.value])
			else:
				print("Variável: {} na linha: {}, não foi declarada.".format(i.value,item.line+1))
				exit()
		check(tokens)
		item = tokens.pop(0)
		if item.value != ')':
			erro(item, ")")
		return
	if item.value == 'write':
		tokens.pop(0)
		check(tokens)
		item = tokens.pop(0)
		if item.value != '(':
			erro(item, "(")
		variaveis(tokens)
		for i in aux_var:
			if(buscaTS(i.value)):
				aux_read.append(tabela[escopoAtual][i.value])
			elif(buscaGlobalTS(i.value)):
				aux_read.append(tabela["main"][i.value])
			else:
				print("Variável: {} na linha: {}, não foi declarada.".format(i.value,item.line+1))
				exit()
		check(tokens)
		item = tokens.pop(0)
		if item.value != ')':
			erro(item, ")")
		return
	if item.value == 'while':
		x = tokens[1]
		if x.value == '(':
			x = tokens[2]
		aux_tipo = tabela[escopoAtual][x.value]
		tokens.pop(0)
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
		x = tokens[1]
		if x.value == '(':
			x = tokens[2]
		aux_tipo = tabela[escopoAtual][x.value]
		tokens.pop(0)
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
		tokens.pop(0)
		if not(buscaTS(item.value)):
			if not(buscaGlobalTS(item.value)):
				print("Variável: {} na linha: {}, não foi declarada.".format(item.value,item.line+1))
				exit()
		aux_tipo = tabela[escopoAtual][item.value] if buscaTS(item.value) else tabela["main"][item.value]
		ident_aux = item.value
		restoldent(tokens)
		return
	erro(item, "read , write, while, if ou tipo idenficador")

def restoldent(tokens):
	global tabela
	global ident_aux
	check(tokens)
	item = tokens[0]
	if item.value == ':=':
		tokens.pop(0)
		expressao(tokens)
		return
	if tabela["main"][ident_aux][1] != "procedure":
		exit("Procedimento: {} na linha: {}, não declarado.".format(ident_aux, item.line + 1))
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
	global aux_var
	global aux_tipo
	global escopoAtual
	global tabela
	check(tokens)
	item = tokens.pop(0)
	if item.type == 'ident':
		if(buscaTS(item.value)):
			if(aux_tipo[2] != tabela[escopoAtual][item.value][2]):
				exit("Variável: {} de tipo {} incompatível. Linha: {}".format(item.value,aux_tipo[2],item.line+1))
		elif(buscaGlobalTS(item.value)):
			if(aux_tipo[2] != tabela["main"][item.value][2]):
				exit("Variável: {} de tipo {} incompatível. Linha: {}".format(item.value,aux_tipo[2],item.line+1))
		else:
			exit("Variável: {} na linha: {}, não foi declarada.".format(item.value,item.line+1))
		return
	if item.type == 'numero_int':
		if(aux_tipo[2] != "integer"):
			exit("Variável: {} de tipo {} incompatível. Linha: {}".format(item.value,aux_tipo[2],item.line+1))
		return
	if item.type == 'numero_real':
		if(aux_tipo[2] != "real"):
			exit("Variável: {} de tipo {} incompatível. Linha: {}".format(item.value,aux_tipo[2],item.line+1))
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



		