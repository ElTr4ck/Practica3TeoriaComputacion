#Autores:                                 4CM3
#Gutierrez Martínez Rodrigo Jozafat
#Villarreal Razo Carlos Gabriel

#----------------------Importacion de la libreria para el maneo de gramaticas----------------------
import nltk
from nltk import CFG
#----------------------Importacion de la libreria para la interfaz gráfica----------------------
import tkinter as tk
from tkinter import messagebox

#----------------------Definir la gramática----------------------
gramatica = CFG.fromstring("""
    S -> IDEN '=' ASIG ';'
    IDEN -> LET IDEN | IDEN NUM IDEN | IDEN NUM | LET
    ASIG -> IDEN '=' ASIG | OPEN | OPERACION
    OPERACION -> OPERACION OPER OPERACION | '(' OPERACION ')' | OPEN
    NUM -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0' NUM | '1' NUM | '2' NUM | '3' NUM | '4' NUM | '5' NUM | '6' NUM | '7' NUM | '8' NUM | '9' NUM
    LET -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | '_'
    OPER -> '+' | '-' | '*' | '/' | '%'
    OPEN -> IDEN | NUM
""")

#----------------------Definicion de la clase pila para su manejo en la practica----------------------
class Pila:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.items.pop()

    def cima(self):
        if self.esta_vacia():
            return None
        return self.items[-1]

    def tamano(self):
        return len(self.items)

#----------------------Funcion para identificar si una letra es un simbolo operador----------------------
def isOperador(letra):
    operadores = ['+', '-', '*', '/', '%']
    if letra in operadores: return True
    else: return False
 
#----------------------Funcion del automata completo----------------------
def AutoPila(cadena):
    #Pila para el automata
    pilaAceptacion = Pila()
    estadoActual = 0
    #El primer caracter debe de ser una letra para continuar
    if cadena[0].isalpha() or cadena[0] == '_':
        for caracter in cadena:
            if estadoActual == 0:
                if (caracter.isalpha() or caracter == '_') and pilaAceptacion.esta_vacia():
                    estadoActual = 1
                else: return False
            elif estadoActual == 1:
                if (caracter.isalpha() or caracter.isdigit() or caracter == '_') and ((pilaAceptacion.esta_vacia()) or (pilaAceptacion.cima() == 'I')):
                    estadoActual == 1
                elif caracter == ';' and (pilaAceptacion.cima() == 'I'):
                    estadoActual = 3
                elif caracter == '=' and (pilaAceptacion.esta_vacia() or pilaAceptacion.cima()=='I'):
                    estadoActual = 2
                    pilaAceptacion.apilar('I')
                elif isOperador(caracter) and (pilaAceptacion.cima() == 'I'):
                    estadoActual = 5
                else: return False
            elif estadoActual == 2:
                if (caracter.isalpha() or caracter == '_') and (pilaAceptacion.cima() == 'I'):
                    estadoActual = 1
                elif caracter.isdigit() and (pilaAceptacion.cima() == 'I'):
                    estadoActual = 4
                elif (caracter == '(') and (pilaAceptacion.cima() == 'I'):
                    estadoActual = 5
                    pilaAceptacion.apilar('P')
                else: return False
            elif estadoActual == 3:
                #Si le llega algo mas al automata cuando ya esta en el de aceptacion, devolver falso
                if caracter: return False
            elif estadoActual == 4:
                if caracter.isdigit() and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    estadoActual = 4
                    print("Entrando a q4 y permaneciendo con: " + caracter)
                elif caracter == ';' and pilaAceptacion.cima() == 'I':
                    pilaAceptacion.desapilar()
                    estadoActual = 3
                elif isOperador(caracter) and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    estadoActual = 5
                elif caracter == ')' and pilaAceptacion.cima() == 'P':
                    pilaAceptacion.desapilar()
                    estadoActual = 7
                else: return False
            elif estadoActual == 5:
                if caracter.isdigit() and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    estadoActual = 4
                elif (caracter.isalpha() or caracter == '_') and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    estadoActual = 6
                elif caracter == '(' and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    pilaAceptacion.apilar('P')
                    estadoActual = 5
                else: return False
            elif estadoActual == 6:
                if (caracter.isdigit() or caracter.isalpha() or caracter == '_') and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    estadoActual = 6
                elif isOperador(caracter) and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    estadoActual = 5
                elif caracter == ')' and pilaAceptacion.cima() == 'P':
                    pilaAceptacion.desapilar()
                    estadoActual = 7
                elif caracter == ';' and pilaAceptacion.cima() == 'I':
                    pilaAceptacion.desapilar()
                    estadoActual = 3
                else: return False
            elif estadoActual == 7:
                if caracter == ';' and pilaAceptacion.cima() == 'I':
                    pilaAceptacion.desapilar()
                    estadoActual = 3
                elif caracter == ')' and pilaAceptacion.cima() == 'P':
                    pilaAceptacion.desapilar()
                    estadoActual = 7
                elif isOperador(caracter) and (pilaAceptacion.cima() == 'I' or pilaAceptacion.cima() == 'P'):
                    estadoActual = 5
                else: return False

        if estadoActual == 3:
            return True
        else: return False

    else:
        return False

#----------------------Main----------------------
def ejecutarPrograma():
    #recuperar lo ingresado por el usuario
    exp = entrada.get()
    #eliminar los espacios en blanco si es que los hubiera
    exp = exp.replace(" ", "")
    #Pasar la expresion a minusculas para que la gramatica las pueda leer
    #exp = exp.lower()
    print(exp)
    
    #Comprobar si la expresion es aceptada por el automata
    if AutoPila(exp):
        messagebox.showinfo("Alerta", "La cadena SI es aceptada por la gramática")
        caracteres = []
        for letra in exp:
            if letra != ' ':
                caracteres.append(letra)
        sentence = ' '.join(caracteres)
        parser = nltk.ChartParser(gramatica)
        tokens = sentence.split()
        for tree in parser.parse(tokens):
            tree.draw()
            break
    else:
        messagebox.showinfo("Alerta", "La cadena NO es aceptada por la gramática")

#----------------------Crear la ventana principal----------------------
ventana = tk.Tk()
ventana.title("Practica 3")
#----------------------Configurar el estilo de la ventana----------------------
ventana.configure(bg="#F4F4F4")

#----------------------Crear el título----------------------
titulo = tk.Label(ventana, text="PRACTICA 3", font=("Arial", 18, "bold"), bg="#F4F4F4", fg="#333333")
titulo.pack(pady=20)

#----------------------Crear el campo de entrada----------------------
entrada = tk.Entry(ventana, font=("Arial", 12), bg="#FFFFFF", fg="#333333", relief="solid")
entrada.pack(pady=10)

#----------------------Crear el botón----------------------
boton = tk.Button(ventana, text="Comprobar cadena", font=("Arial", 12, "bold"), bg="#4CAF50", fg="#FFFFFF", relief="raised", command=ejecutarPrograma)
boton.pack(pady=10, padx=50)

#----------------------Ejecutar la ventana----------------------
ventana.mainloop()
