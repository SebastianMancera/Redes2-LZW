import numpy as np

def leer_archivo_comprimido(archivo):
    archivo_comprimido = open(archivo, "r")
    lines = []
    for line in archivo_comprimido:
        lines.append(line)
    archivo_comprimido.close()
    return lines


def leer_codigo(lineas):
    mensaje = lineas[1].split(",")
    return mensaje

def leer_diccionario(lineas):
    dicc = lineas[0].split("|")
    diccionario_claves = []
    # se leen las claves del diccionario
    for lista in dicc:
        for caracter in lista:
            if caracter != ":":
                diccionario_claves.append(caracter)
            else:
                break
    # se leen los valores del diccionario
    diccionario_valores = []
    for lista in dicc:
        cadena = ""
        leer = False
        for caracter in lista:
            if caracter == ":":
                leer = True
                continue
            if leer:
                cadena += caracter
        diccionario_valores.append(cadena.rstrip("\n"))

    #diccionario_valores.remove("\n")
    diccionario = dict(zip(diccionario_claves, diccionario_valores))
    return diccionario



def contador_letras(codigo):
    return len(codigo) - 1


def traducir(codigo_viejo,diccionario):
    clave = list(diccionario.keys())[list(diccionario.values()).index(codigo_viejo)]
    return clave


def algoritmo_descompresion(codigo,diccionario, contar_letras,):
    # se crea la matriz donde se almacenará el código
    matriz = np.zeros(shape=(contar_letras + 1, 5), dtype="U100")
    posicion_fila = 0
    posicion_codigo = 0
    fin_archivo = False

    # se asignan los valores de la columna  de la matriz segun el nombre
    cod_viejo = 0
    cod_nuevo = 1
    cadena = 2
    caracter = 3
    salida = 4

    # incio algoritmo descompresion

    # leer codigo viejo
    matriz[posicion_fila, cod_viejo] = codigo[posicion_codigo]
    # caracter = Traducir(cód_viejo)
    matriz[posicion_fila, caracter] = traducir(matriz[posicion_fila, cod_viejo],diccionario)
    # imprimir caracter en salida
    matriz[posicion_fila, salida] = matriz[posicion_fila, caracter]
    # mientras no sea fin de archivo
    while not fin_archivo:
        # se itera al siguiente codigo
        posicion_codigo += 1
        # leer codigo nuevo
        matriz[posicion_fila, cod_nuevo] = codigo[posicion_codigo]
        # si codigo nuevo no esta en el diccionario
        if codigo[posicion_codigo] not in diccionario.values():
            # cadena=Traducir(cód_viejo)
            matriz[posicion_fila, cadena] = traducir(matriz[posicion_fila, cod_viejo],diccionario)
            # cadena= cadena + caracter
            matriz[posicion_fila, cadena + 1] = matriz[posicion_fila, cadena] + matriz[posicion_fila, caracter]
        else:  # cadena = traducir codigo nuevo
            matriz[posicion_fila, cadena] = traducir(matriz[posicion_fila, cod_nuevo],diccionario)
        posicion_fila = posicion_fila + 1
        # imprimir cadena en salida
        matriz[posicion_fila, salida] = matriz[posicion_fila - 1, cadena]
        # caracter = primer caracter de cadena
        matriz[posicion_fila, caracter] = str(matriz[posicion_fila - 1, cadena])[0]
        # Agregar Traducir(cód_viejo)+carácter al diccionario
        numero_final = diccionario.values()
        # se halla el ultimo valor asignado al diccionario
        numero_final = max([int(i) for i in numero_final])
        diccionario[traducir(matriz[posicion_fila - 1, cod_viejo],diccionario) + matriz[posicion_fila, caracter]] = str(
            numero_final + 1)
        # cód_viejo=cód_nuevo
        matriz[posicion_fila, cod_viejo] = matriz[posicion_fila - 1, cod_nuevo]
        # comprobar fin de archivo en cada iteración
        if posicion_codigo == contar_letras:
            matriz[posicion_fila, cod_nuevo] = "<EOF>"
            fin_archivo = True
    return matriz


def obtener_mensaje(matriz):
    salida = 4  # numero de la columna a obtener de la matriz
    columna = []
    for fila in matriz:
        columna.append(fila[salida])
    return "".join(columna)

def guardar_descompresion(mensaje):
    with open("mensaje_descomprimido.txt", "w") as mensaje_archivo:
        mensaje_archivo.write(mensaje)

def main():
    # leer archivo
    archivo = leer_archivo_comprimido("mensaje_comprimido.txt")
    # leer codigo
    codigo = leer_codigo(archivo)
    # leer diccionario
    diccionario = leer_diccionario(archivo)
    # se obtiene la cantidad de caracteres del mensaje comprimido para conocer el tamaño de la matriz
    cant_letras = contador_letras(codigo)
    # se crea la matriz del tamaño de codigos existentes en el mensaje y se descomprime
    matriz = algoritmo_descompresion(codigo,diccionario, cant_letras)
    print("Matriz de Descompresión LZW")
    # print("C_Viejo","C_Nuevo","Cadena","Caracter","Salida")
    print(matriz)
    print(" ")
    print("Diccionario para Descomprimir")
    print(diccionario)
    # se obtiene en mensaje de la columna 4 (salida) de la matriz
    mensaje = obtener_mensaje(matriz)
    print(" ")
    print(f"El mensaje obtenido es: {mensaje}")
    # se guarda mensaje en archivo
    guardar_descompresion(mensaje)


main()
