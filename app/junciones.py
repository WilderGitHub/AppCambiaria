#funciones
import os
from dbfread import DBF
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def getParametros(archivo,hoja=""):
    # Para las palabras clave
    if hoja=="palabras":
        palabrasClave = pd.read_excel(archivo, sheet_name=hoja)
        listaPalabrasClave = palabrasClave['PalabrasClave'].values.tolist()
        # aqui apachurramos todo
        junto = ''
        for palabrita in listaPalabrasClave:
            junto += '|' + palabrita
        junto = junto[1:]
        return junto
    #Para los cuentas
    if archivo == "cuentas":
        cuentas = [7, 10, 11, 12, 16, 17]
        return cuentas
    # Para movimientos y clasificador
    x = pd.read_excel(archivo, sheet_name=hoja)    
    return x

def leer(nombreArchivo):
    extension = os.path.splitext(nombreArchivo)[1]
    if extension == '.dbf':
        table = DBF(nombreArchivo, encoding='latin', load=True)
        return pd.DataFrame(iter(table))
    else:
        #para los que no son dbf
        return pd.read_excel(nombreArchivo)
# funciones