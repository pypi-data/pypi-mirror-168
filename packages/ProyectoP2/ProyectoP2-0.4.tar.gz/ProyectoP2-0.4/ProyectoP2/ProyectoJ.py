#Utilizamos matrices en PYTHON para crear el juego
#Instalamos NUMPY como libreria para la logica del juego
#Instalomos PYGAME como libreria para las graficas del juego
import numpy as np 
import pygame
#Modulo sistema SYS
import sys
#Modulo math
import math

def play():
    Numero_de_filas = 6
    Numero_de_columnas = 7
    AZUL = (0,0,255)
    NEGRO = (0,0,0)
    AMARILLO = (255,255,0)
    VERDE = (0,255,0)

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

    def dibujar_tablero(tablero):
        for c in range (Numero_de_columnas):
            for f in range (Numero_de_filas):
                #Dibujar PYGAME rectangulo
                pygame.draw.rect(pantalla, AZUL, (c*tamaño_del_cuadrado, f*tamaño_del_cuadrado + tamaño_del_cuadrado, tamaño_del_cuadrado, tamaño_del_cuadrado))
                #Dibujar PYGAME circulo
                pygame.draw.circle(pantalla, NEGRO, (int(c*tamaño_del_cuadrado+(tamaño_del_cuadrado/2)), int(f*tamaño_del_cuadrado + tamaño_del_cuadrado + (tamaño_del_cuadrado/2))), RADIO)

        for c in range (Numero_de_columnas):
            for f in range (Numero_de_filas):
                if tablero[f][c] == 1:
                    pygame.draw.circle(pantalla, AMARILLO, (int(c*tamaño_del_cuadrado+(tamaño_del_cuadrado/2)), int(alto - (f*tamaño_del_cuadrado + (tamaño_del_cuadrado/2)))), RADIO)
                elif tablero[f][c] == 2:
                    pygame.draw.circle(pantalla, VERDE, (int(c*tamaño_del_cuadrado+(tamaño_del_cuadrado/2)), int(alto - (f*tamaño_del_cuadrado + (tamaño_del_cuadrado/2)))), RADIO)

        pygame.display.update()                


    tablero = Crear_tablero()
    imprimir_tablero(tablero)    


    #Funcion principal del juego
    fin_del_juego = False
    turno = 0



    #Inicializar PYGAME
    pygame.init()
    #TEXTO
    pygame.font.init()

    mi_fuente = pygame.font.SysFont("Courier", 60, bold=1)

    #Tamaño de nuestra ventana
    tamaño_del_cuadrado = 90
    RADIO = int((tamaño_del_cuadrado/2) - 5)
    ancho = Numero_de_columnas * tamaño_del_cuadrado
    alto = (Numero_de_filas + 1) * tamaño_del_cuadrado

    tamaño = (ancho, alto)
    pantalla = pygame.display.set_mode(tamaño)
    pygame.display.update()
    dibujar_tablero(tablero)


    while not fin_del_juego:
        #PYGAME maneja los eventos (teclado, mouse, etc.)
        for event in pygame.event.get():
            #Cerrar ventana
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(pantalla, NEGRO, (0,0,ancho, tamaño_del_cuadrado))
                posicion_x = event.pos[0]
                if turno == 0:
                    pygame.draw.circle(pantalla, AMARILLO,(posicion_x, int(tamaño_del_cuadrado/2)), RADIO)
                elif turno == 1:
                    pygame.draw.circle(pantalla, VERDE,(posicion_x, int(tamaño_del_cuadrado/2)), RADIO)

            pygame.display.update()
                
            #Utilizar mouse para colocar la pieza
            if event.type == pygame.MOUSEBUTTONDOWN:
                                          
                #Solicitar movida del jugador 1
                if turno == 0:            
                    #columna = int(input("Jugador 1 haz tu movida (0-6):"))
                    posicion_x = event.pos[0]
                    columna = math.floor(posicion_x/tamaño_del_cuadrado)
                    if espacio_valido(tablero, columna):
                        fila = siguiente_fila_vacia(tablero, columna)
                        soltar_pieza(tablero, fila, columna, 1)

                        if movida_ganadora(tablero, 1):
                            #print("Jugador 1 ganó FELICIDADES!!!")
                            texto = mi_fuente.render("Jugador 1 ganó", 0, AZUL)
                            pantalla.blit(texto,(40,20))
                            fin_del_juego = True

                else:
                    #columna = int(input("Jugador 2 haz tu movida (0-6):"))
                    posicion_x = event.pos[0]
                    columna = math.floor(posicion_x/tamaño_del_cuadrado)
                    if espacio_valido(tablero, columna):
                        fila = siguiente_fila_vacia(tablero, columna)
                        soltar_pieza(tablero, fila, columna, 2)

                        if movida_ganadora(tablero, 2):
                            #print("Jugador 2 ganó FELICIDADES!!!")
                            texto = mi_fuente.render("Jugador 2 ganó", 0, AZUL)
                            pantalla.blit(texto,(40,20))
                            fin_del_juego = True
                    
                imprimir_tablero(tablero)
                dibujar_tablero(tablero)
                     
                turno += 1
                turno = turno % 2


















            
