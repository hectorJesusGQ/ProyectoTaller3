import sys

def leer_archivo(File):
    with open(File, 'r') as archivo:
        txt = archivo.read()
    return txt

def contar_frecuencia(txt):
    frecuencia = {}
    for chtr in txt:
        if chtr in frecuencia:
            frecuencia[chtr] += 1
        else:
            frecuencia[chtr] = 1
    return frecuencia

def ListaFrecuencia(frecuencia):
    freqList = []
    for chtr, freq in frecuencia.items():
        freqList.append((freq, [chtr, [], []]))
    return freqList

def Huff(freqList):
    while len(freqList) > 1:
        freqList = sorted(freqList, key=lambda x: x[0])
        freq1, L = freqList.pop(0)
        freq2, R = freqList.pop(0)
        Newfreq = freq1 + freq2
        freqList.append([Newfreq, [[], L, R]])
    return freqList[0]

def CodeMap(T, currentCode="", codigos={}):
    if not T[1] and not T[2]:  
        codigos[T[0]] = currentCode
    else:
        CodeMap(T[1], currentCode + "0", codigos)
        CodeMap(T[2], currentCode + "1", codigos)
    return codigos

def codificador(txt, codigos):
    codedTXT = ""
    for chtr in txt:
        codedTXT += codigos[chtr]
    return codedTXT

def write(File, contenido):
    with open(File, 'w') as archivo:
        archivo.write(contenido)

def BinWrite(File, contenido):
    bArray = bytearray()
    for i in range(0, len(contenido), 8):
        byte = int(contenido[i:i+8], 2)
        bArray.append(byte)
    with open(File, 'wb') as archivo:
        archivo.write(bArray)

def TableCod(codigos):
    codigosSTR = ""
    for chtr, codigo in codigos.items():
        if chtr == ' ':
            codigosSTR += f"SPACE: {codigo}\n"
        else:
            codigosSTR += f"{chtr}: {codigo}\n"
    return codigosSTR

def Height(T):
    if not T[1] and not T[2]: 
        return 0
    return 1 + max(Height(T[1]), Height(T[2]))

def Wide(T):
    if not T[1] and not T[2]: 
        return 1
    return Wide(T[1]) + Wide(T[2])

def nodsbyLevel(T, Lvl=0, niveles={}):
    if Lvl not in niveles:
        niveles[Lvl] = 0
    niveles[Lvl] += 1
    if T[1] or T[2]: 
        nodsbyLevel(T[1], Lvl + 1, niveles)
        nodsbyLevel(T[2], Lvl + 1, niveles)
    return niveles

def Compresor(inputFile):
    txt = leer_archivo(inputFile)
    frecuencia = contar_frecuencia(txt)
    freqList = ListaFrecuencia(frecuencia)
    Thuff = Huff(freqList)
    codigos = CodeMap(Thuff[1])
    codedTXT = codificador(txt, codigos)
    codigos = TableCod(codigos)
    
    BinWrite('Compresion.huff', codedTXT)
    write('TablaCodigos.table', codigos)
    
    h = Height(Thuff[1])
    w = Wide(Thuff[1])
    lvl = nodsbyLevel(Thuff[1])
    freq = "\n".join(f"{chtr}: {freq}" for freq, [chtr, _, _] in freqList)
    
    estadisticas = (
        f"Altura: {h}\n"
        f"Anchura: {w}\n"
        f"Nodos por nivel: {lvl}\n"
        f"Frecuencia:\n{freq}")
    write('Stats.txt', estadisticas)

Compresor(sys.argv[1])
