#Utilizamos matrices en PYTHON para crear el juego
#Instalamos NUMPY como libreria para la logica del juego

import numpy as np 

Numero_de_filas = 6
Numero_de_columnas = 7

#Crear tablero vacio
def Crear_tablero():
    #Función numpy matrices ceros
    tablero = np.zeros((Numero_de_filas, Numero_de_columnas))
    return(tablero)

#Comprobación de si el espacio (movimento del jugador) es valido
def espacio_valido(tablero, columna):
    return (tablero[Numero_de_filas - 1][columna] == 0)

#Saber cual es la siguiente fila vacia
def siguiente_fila_vacia(tablero, columna):
    for fila in range(Numero_de_filas):
        if tablero[fila][columna] == 0:
            return (fila)

#Soltar la pieza
def soltar_pieza(tablero, fila, columna, pieza):        
    tablero[fila][columna] = pieza

#Imprimir tablero piezas de abajo - arriba
def imprimir_tablero(tablero):
    print(np.flipud(tablero))

#Escoger ganador
def movida_ganadora(tablero, pieza):
    #Chekear posiciones en horizontal
    for c in range (Numero_de_columnas - 3):
        for f in range (Numero_de_filas):
            if tablero[f][c] == pieza and tablero[f][c + 1] == pieza and tablero[f][c + 2] == pieza and tablero[f][c + 3] == pieza:
                return (True)
    #Chekear posiciones en vertical
    for c in range (Numero_de_columnas):
        for f in range (Numero_de_filas - 3):
            if tablero[f][c] == pieza and tablero[f + 1][c] == pieza and tablero[f + 2][c] == pieza and tablero[f + 3][c] == pieza:
                return (True)
    #Chekear posiciones en diagonal con pendiente positiva
    for c in range (Numero_de_columnas - 3):
        for f in range (Numero_de_filas - 3):
            if tablero[f][c] == pieza and tablero[f + 1][c + 1] == pieza and tablero[f + 2][c + 2] == pieza and tablero[f + 3][c + 3] == pieza:
                return (True)
    #Chekear posiciones en diagonal con pendiente negativa
    for c in range (Numero_de_columnas - 3):
        for f in range (3, Numero_de_filas):
            if tablero[f][c] == pieza and tablero[f - 1][c + 1] == pieza and tablero[f - 2][c + 2] == pieza and tablero[f - 3][c + 3] == pieza:
                return (True)

tablero = Crear_tablero()
imprimir_tablero(tablero)    


#Funcion principal del juego
fin_del_juego = False
turno = 0

while not fin_del_juego:
   
    #Solicitar movida del jugador 1
    if turno == 0:
        columna = int(input("Jugador 1 haz tu movida (0-6):"))
        if espacio_valido(tablero, columna):
            fila = siguiente_fila_vacia(tablero, columna)
            soltar_pieza(tablero, fila, columna, 1)
            imprimir_tablero(tablero)

            if movida_ganadora(tablero, 1):
                print("Jugador uno ganó FELICIDADES!!!")
                imprimir_tablero(tablero)
                fin_del_juego = True
    else:
        columna = int(input("Jugador 2 haz tu movida (0-6):"))
        if espacio_valido(tablero, columna):
            fila = siguiente_fila_vacia(tablero, columna)
            soltar_pieza(tablero, fila, columna, 2)
            imprimir_tablero(tablero)

            if movida_ganadora(tablero, 2):
                print("Jugador dos ganó FELICIDADES!!!")
                imprimir_tablero(tablero)
                fin_del_juego = True

    turno += 1
    turno = turno % 2

