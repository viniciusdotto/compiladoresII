#Vinícius Dotto de Arruda Figueiredo
#Analisador Léxico da Linguagem Lalg
#usar find() pra resolver o erro


import nltk

palavraReservada = ('program','procedure', 'var','real','integer','if', 'then', 'while', 'do', 'write', 'read', 'else', 'begin', 'end', '$')
terminais = (' ', '\t', '\n', ',', '(', ')', ';', ':', ',', '*', '/', '+', '-', '<>', '>=', '>', '<', ':=', '=')
delimitador = ('(', ')', ';', ':', ',','.')
operador = ('*', '/', '+', '-', ':=')
relacionais = ('=', '<>', '>=', '<=', '>', '<')

class Token:
    def __init__(self, _value, _type, _line):
        self.type = _type
        self.value = _value
        self.line = _line

    def __str__(self):
        return "'{}' {} linha {}".format(self.value, self.type, self.line)

    __repr__ = __str__

def lexico():
    with open('arquivo.txt','r') as arq:
        tokens = []
        erro = 0
        notComent1 = 1
        notComent2 = 1
        for i, l in enumerate(arq):
            tokenizer = nltk.WordPunctTokenizer()
            termList = tokenizer.tokenize(l)
            for indice, j in enumerate(termList):
                if j == ');':
                    if notComent1 and notComent2:
                        tokens.append(Token(')', "delimitador", i+1))
                        tokens.append(Token(';', "delimitador", i+1))
                elif j.find('/*') != -1:
                    aux = j.find('/*')
                    if notComent2 == 1:
                        if aux != 0:
                            termList.insert(indice+1, j[:aux])
                            termList.insert(indice+2, j[aux:])
                        else:
                            notComent1 = 0
                elif j.find('{') != -1:
                    aux = j.find('{')
                    if notComent1 == 1:
                        if aux != 0:
                            termList.insert(indice+1, j[:aux])
                            termList.insert(indice+2, j[aux:])
                        else:
                            notComent2 = 0
                elif j.find('*/') != -1:
                    aux = j.find('*/')
                    if notComent1 == 0:
                        notComent1 = 1
                        termList.insert(indice+1, j[aux+2:])
                    elif notComent1 and notComent2:
                        print ("Erro lexico, fim de comentário não esperado.\nValor encontrado: " + str('*/') + ".\nLinha: " + str(i+1))
                        exit()        
                elif j.find('}') != -1:
                    aux = j.find('}')
                    if notComent2 == 0:
                        notComent2 = 1
                        termList.insert(indice+1, j[aux+1:])
                    elif notComent1 and notComent2:
                        print ("Erro lexico, fim de comentário não esperado.\nValor encontrado: " + str('}') + ".\nLinha: " + str(i+1))
                        exit()       
                elif j in palavraReservada:
                    if notComent1 and notComent2:
                        tokens.append(Token(j, "reservada", i+1))
                elif j in delimitador:
                    if notComent1 and notComent2:
                        tokens.append(Token(j, "delimitador", i+1))
                elif j in operador:
                    if notComent1 and notComent2:
                        tokens.append(Token(j, "operador", i+1))
                elif j in relacionais:
                    if notComent1 and notComent2:
                        tokens.append(Token(j, "relacional", i+1))
                elif j.isnumeric():
                    if notComent1 and notComent2:
                        if (len(termList) - 2) > indice:                         
                            if termList[indice+1] == '.':
                                numero = str(termList[indice]) + str(termList[indice+1]) + str(termList[indice+2])
                                tokens.append(Token(numero, "numero_real", i+1))
                                del termList [indice+1]
                                del termList [indice+1]
                            else: 
                                tokens.append(Token(j, "numero_int", i+1))
                        else:
                            tokens.append(Token(j, "numero_int", i+1))        
                elif j.isalnum():
                    if notComent1 and notComent2:
                        if j[0].isalpha():
                            tokens.append(Token(j, "ident", i+1))
                        elif j[0].isdigit():
                            print ("Erro lexico, identificador nao pode começar com numero.\nValor encontrado: " + str(j) + ".\nLinha: " + str(i+1))
                            exit()
                elif j:
                    if notComent1 and notComent2:
                        print ("Erro lexico, simbolo invalido\nValor encontrado: " + str(j) + ".\nLinha: " + str(i+1))
                        exit()    
        print('\n Cadeia de Tokens aceita')
        for i in tokens:
            print ('[', i, ']')
        return tokens      


