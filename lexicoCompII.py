import nltk

palavraReservada = ('program','var','real','integer','if', 'then', 'while', 'do', 'write', 'read', 'else', 'begin', 'end', '$')
terminais = (' ', '\t', '\n', ',', '(', ')', ';', ':', ',', '*', '/', '+', '-', '<>', '>=', '>', '<', ':=')
delimitador = ('(', ')', ';', ':', ',')
operador = ('*', '/', '+', '-', '<>', '>=', '>', '<', ':=')

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
                if j == '/*':
                    if notComent2 == 1:
                        notComent1 = 0
                elif j == '{':
                    if notComent1 == 1:
                        notComent2 = 0
                elif j == '*/':
                    if notComent1 == 0:
                        notComent1 = 1
                elif j == '}':
                    if notComent2 == 0:
                        notComent2 = 1
                elif j in palavraReservada:
                    if notComent1 and notComent2:
                        tokens.append(Token(j, "reservada", i+1))
                elif j in delimitador:
                    if notComent1 and notComent2:
                        tokens.append(Token(j, "delimitador", i+1))
                elif j in operador:
                    if notComent1 and notComent2:
                        tokens.append(Token(j, "operador", i+1))
                elif j.isnumeric():
                    if notComent1 and notComent2:
                        if (len(termList) - 2) > indice:                         
                            if termList[indice+1] == '.':
                                numero = str(termList[indice]) + str(termList[indice+1]) + str(termList[indice+2])
                                tokens.append(Token(numero, "numero_real", i+1))
                                print (termList)
                                del termList [indice+1]
                                print (termList)
                                del termList [indice+1]
                                print (termList)
                            else: 
                                tokens.append(Token(j, "numero_int", i+1))
                        else:
                            tokens.append(Token(j, "numero_int", i+1))        
                elif j.isalnum():
                    if notComent1 and notComent2:
                        if j[0].isalpha():
                            tokens.append(Token(j, "ident", i+1))
                        elif j[0].isdigit():
                            print ("Erro lexico")
                            exit()
                elif j:
                    if notComent1 and notComent2:
                        print ("Erro lexico")
                        exit()    
        for i in tokens:
            print ('[', i, ']')
        print('\n Cadeia aceita')
        return tokens      


if __name__ == '__main__':
	lexico()
	