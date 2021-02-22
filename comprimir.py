import numpy as np
import math
import os
from PIL import Image as im
salida = []
from PIL import Image


def leerMensaje():
    archivo = open("mensaje.txt", "r")
    mensaje = archivo.read()
    archivo.close()
    return mensaje


def leerCaracteres(mensaje):
    for i in mensaje:
        print(i)


def cantidadCaracteres(mensaje):
    contador_letras = 0
    for i in mensaje:
        contador_letras += 1
    return contador_letras


def crearDiccionario(mensaje):
    diccionario = {}
    numeroletra = -1
    for i in mensaje:
        if i not in diccionario:
            numeroletra += 1
            diccionario[i] = numeroletra
    return diccionario


def agregarAlDiccionario(diccionario, clave, valor):
    diccionario[clave] = valor
    return diccionario


def imprimir(diccionario,codigo):
    impresion = diccionario[codigo]
    return impresion



def algoritmolzw(contador_letras,diccionario,mensaje):
    """
    Se crea una matriz de tres columnas y n filas para almacenar las columnas w,k,wk
    Primera columna w
    Segunda columna k
    Tercera columna wk
    """

    matriz = np.zeros(shape=(contador_letras + 1, 3), dtype="U100")
    fin_archivo = False
    posicion_codigo = 0
    posicion_fila = 0

    # se asignan los valores de la columna  de la matriz segun el nombre
    w = 0
    k = 1
    wk = 2

    # incio algoritmo lzw
    # w = null
    matriz[posicion_fila, w] = "vacio"

    # mientras no sea fin de archivo
    while not fin_archivo:
        # leer K
        matriz[posicion_fila,k] = mensaje[posicion_codigo]
        # wk = w + k
        if matriz[posicion_fila, w] == "vacio":
            matriz[posicion_fila, wk] = matriz[posicion_fila,k]
        else:
            matriz[posicion_fila, wk] = matriz[posicion_fila, w ] + matriz[posicion_fila,k]
        posicion_codigo += 1
        posicion_fila += 1
        # si wk esta en el diccionario
        if matriz[posicion_fila - 1,wk] in diccionario.keys():
            # w = wk
            matriz[posicion_fila, w] = matriz[posicion_fila -1, wk]
        else:
            # imprimir el código  w
            impresion = imprimir(diccionario, matriz[posicion_fila -1, w])
            salida.append(impresion)
            # agregar wk al diccionario
            numero_final = diccionario.values()
            # se halla el ultimo valor asignado al diccionario
            numero_final = max([int(i) for i in numero_final])
            agregarAlDiccionario(diccionario,matriz[posicion_fila -1 ,wk],numero_final + 1 )
            # w=K
            matriz[posicion_fila,w] = matriz[posicion_fila-1,k]
        # fin de archivo
        if posicion_codigo == contador_letras:
            matriz[posicion_fila, k] = "<EOF>"
            fin_archivo = True
    # imprimir el codigo de w
    impresion = imprimir(diccionario, matriz[posicion_fila, w])
    salida.append(impresion)
    return matriz



def cantidadBitsMensaje(contador_letras):
    bits_mensaje = contador_letras * 8
    return bits_mensaje


def cantidadBitsCodigos(diccionario, salida):
    bits_codigo = list(diccionario.values())
    bits_codigo = max(bits_codigo) + 1
    bits_codigo = math.ceil(math.log(bits_codigo, 2))
    total_bits_codigo = bits_codigo * len(salida)
    return total_bits_codigo


def relacionCompresion(bits_mensaje, bits_salida):
    rc = round(bits_mensaje / bits_salida, 3)
    print(f"En LZW un bit en el codigo resultante representa {rc} bits de la version sin comprimir")


def evaluacionCompresion(cantidad_letras, diccionario, salida):
    bits_mensaje = cantidadBitsMensaje(cantidad_letras)
    bits_salida = cantidadBitsCodigos(diccionario, salida)
    relacionCompresion(bits_mensaje, bits_salida)


def guardarcompresion(diccionario, salida):
    pos_mensaje = 0
    pos_diccionario = 0
    with open("mensaje_comprimido.txt", "w") as mensaje_archivo:
        for simbolo, valor in diccionario.items():
            pos_diccionario += 1
            mensaje_archivo.write(f"{simbolo}:{valor}")
            if pos_diccionario != len(diccionario.keys()):
                mensaje_archivo.write("|")
        mensaje_archivo.write("\n")
        for mensaje in salida:
            pos_mensaje +=1
            if pos_mensaje == len(salida):
                mensaje_archivo.write(f"{mensaje}")
            else:
                mensaje_archivo.write(f"{mensaje},")
    mensaje_archivo.close()


def main():
    mensaje = leerMensaje()
    print("Texto a comprimir:", mensaje, sep="\n")
    print("")
    cantidad_letras = cantidadCaracteres(mensaje)
    diccionario = crearDiccionario(mensaje)
    print("Diccionario original:")
    print(diccionario)
    print("")
    diccionario_original = diccionario.copy()
    matriz = algoritmolzw(cantidad_letras,diccionario,mensaje)
    print("Matriz LZW")
    print("[  W,  K,  WK]")
    print(matriz)
    print("")
    print("Diccionario construido:")
    print(diccionario)
    print("")
    print("Salida:")
    print(salida)
    print("")
    print("Información de Compresión")
    evaluacionCompresion(cantidad_letras, diccionario, salida)
    guardarcompresion(diccionario_original, salida)

main()
