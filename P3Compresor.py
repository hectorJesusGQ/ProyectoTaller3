import sys
import bitarray

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
        freqList.append((freq, chtr))
    return freqList

def Huff(freqList):
    while len(freqList) > 1:
        freqList = sorted(freqList, key=lambda x: x[0])
        freq1, L = freqList.pop(0)
        freq2, R = freqList.pop(0)
        Newfreq = freq1 + freq2
        freqList.append([Newfreq, [L, R]])
    return freqList[0]

def leaf(T):
    return isinstance(T, str)

def CodeMap(T, currentCode="", codigos={}):
    if leaf(T):
        codigos[T] = currentCode
    else:
        L, R = T
        CodeMap(L, currentCode+"0", codigos)
        CodeMap(R, currentCode+"1", codigos)
    return codigos

def codificar_texto(txt, codigos):
    codedTXT = ""
    for chtr in txt:
        codedTXT += codigos[chtr]
    return codedTXT

def escribir_archivo(File, contenido):
    with open(File, 'w') as archivo:
        archivo.write(contenido)

def escribir_archivo_binario(File, contenido):
    with open(File, 'wb') as archivo:
        archivo.write(bytearray(int(contenido[i:i+8], 2) for i in range(0, len(contenido), 8)))

def Height(T):
    if leaf(T):
        return 0
    L, R = T
    return 1 + max(Height(L), Height(R))

def Wide(T):
    if leaf(T):
        return 1
    L, R = T
    return Wide(L) + Wide(R)

def nodsbyLevel(T, Lvl=0, niveles=None):
    if not niveles:
        niveles = {}
    if Lvl not in niveles:
        niveles[Lvl] = 0
    niveles[Lvl] += 1
    if not leaf(T):
        L, R = T
        nodsbyLevel(L, Lvl + 1, niveles)
        nodsbyLevel(R, Lvl + 1, niveles)
    return niveles

def Compresor(inputFile):
    txt = leer_archivo(inputFile)
    frecuencia = contar_frecuencia(txt)
    freqList = ListaFrecuencia(frecuencia)
    Thuff = Huff(freqList)
    codigos = CodeMap(Thuff[1])
    codedTXT = codificar_texto(txt, codigos)
    
    escribir_archivo_binario('Compresion.huff', codedTXT)
    
    codigos = "\n".join(f"{chtr}: {codigo}" for chtr, codigo in codigos.items())
    escribir_archivo('TablaCodigos.table', codigos)
    
    h = Height(Thuff[1])
    w = Wide(Thuff[1])
    lvl = nodsbyLevel(Thuff[1])
    freq = "\n".join(f"{chtr}: {freq}" for freq, chtr in freqList)
    
    estadisticas = (
        f"Altura: {h}\n"
        f"Anchura: {w}\n"
        f"Nodos por L: {lvl}\n"
        f"Frecuencia:\n{freq}")
    escribir_archivo('Stats.txt', estadisticas)

Compresor(sys.argv[1])
