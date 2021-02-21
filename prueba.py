def leer_archivo_comprimido():
    archivo_comprimido = open('mensaje_comprimido.txt', "r")
    lines = []
    for line in archivo_comprimido:
        lines.append(line)
    archivo_comprimido.close()
    return lines


def leer_codigo(lineas):
    mensaje = lineas[1].split(",")
    return mensaje

def leer_diccionario(lineas):
    dicc = lineas[0].split(",")
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
                print(cadena)
        diccionario_valores.append(cadena.rstrip("\n"))

    #diccionario_valores.remove("\n")
    diccionario = dict(zip(diccionario_claves, diccionario_valores))
    print("original",diccionario)
    print(diccionario_valores)
    return diccionario


def main():
    archivo = leer_archivo_comprimido()
    codigo = leer_codigo(archivo)
    dicc = leer_diccionario(archivo)
    print(dicc)

main()