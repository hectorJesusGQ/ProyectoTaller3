import sys

def ReadBin(File):
    contenido = b''
    with open(File, 'rb') as archivo:
        while True:
            byte = archivo.read(1)
            if not byte:
                break
            contenido += byte
    resultado = ''
    for byte in contenido:
        resultado += format(byte, '08b')
    return resultado


def ReadCode(File):
    with open(File, 'r') as archivo:
        lineas = archivo.readlines()
    codigos = {}
    for lnn in lineas:
        chtr, codigo = lnn.strip().split(': ')
        if chtr == "SPACE":
            chtr = ' '
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

def write(File, contenido):
    with open(File, 'w') as archivo:
        archivo.write(contenido)

def Descompresor(archivo_comprimido, archivo_tabla, archivo_salida):
    codedTXT = ReadBin(archivo_comprimido)
    codigos = ReadCode(archivo_tabla)
    decodedTXT = decodificador(codedTXT, codigos)
    write(archivo_salida, decodedTXT)


Descompresor(sys.argv[1], sys.argv[2], sys.argv[3])
