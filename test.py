# # Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import nltk
import re


grammar = nltk.CFG.fromstring("""


S -> Axiom
Axiom -> VAR  '=' OPERACION
OPERACION ->  OPERACION  '+'  OPERACION  | OPERACION '-' OPERACION | OPERACION '*' OPERACION | OPERACION '/' OPERACION | OPERACION '%' OPERACION | '(' OPERACION ')' | VAR | NUMS | OPERACION '=' OPERACION  
VAR ->  CARACTERES | CARACTERES VAR | '' VAR | VAR '' | VAR NUMS | VAR NUMS VAR | VAR CARACTERES
CARACTERES -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h'
NUMS ->  '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | NUMS NUMS
WSP -> ' ' | ''
""")

operacion = "fea1=fea3=fea2"

caracteres = []

for letra in operacion:
    if letra != ' ':
        caracteres.append(letra)

print(caracteres)


sentence=' '.join(caracteres)
print(sentence)
parser = nltk.ChartParser(grammar)
tokens = sentence.split()


print('Expresion: ' + operacion)
for tree in parser.parse(tokens):
    tree.draw()
