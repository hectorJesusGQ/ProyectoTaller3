import sys

def leer_archivo_binario(nombre_archivo):
    with open(nombre_archivo, 'rb') as archivo:
        contenido = archivo.read()
    return ''.join(format(byte, '08b') for byte in contenido)

def leer_tabla_codigos(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    codigos = {}
    for lnn in lineas:
        chtr, codigo = lnn.strip().split(': ')
        codigos[codigo] = chtr
    return codigos

def decodificador(codedTXT, codigos):
    currentCode = ""
    decodedTXT = ""
    for bit in codedTXT:
        currentCode += bit
        if currentCode in codigos:
            decodedTXT += codigos[currentCode]
            currentCode = ""
    return decodedTXT

def escribir_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(contenido)

def Descompresor(archivo_comprimido, archivo_tabla, archivo_salida):
    codedTXT = leer_archivo_binario(archivo_comprimido)
    codigos = leer_tabla_codigos(archivo_tabla)
    decodedTXT = decodificador(codedTXT, codigos)
    escribir_archivo(archivo_salida, decodedTXT)

Descompresor(sys.argv[1], sys.argv[2], sys.argv[3])
