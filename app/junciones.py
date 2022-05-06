import PySimpleGUI as sg#funciones
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

def getExtension(archivo):
    extension = os.path.splitext(archivo)[1]
    return extension
    
def leer(nombreArchivo):
    #extension = os.path.splitext(nombreArchivo)[1]
    if getExtension(nombreArchivo) == '.dbf':
        table = DBF(nombreArchivo, encoding='latin', load=True)
        return pd.DataFrame(iter(table))
    else:
        #para los que no son dbf
        return pd.read_excel(nombreArchivo)

def losInputs(nombreCampo,inputKey,fileKey, espacio):
    fila=[sg.Text(nombreCampo),
    sg.Input(key=inputKey, 
        change_submits=True, 
        pad=((espacio, 10), 5), 
        size=(80, 1)),
    sg.FileBrowse(key=fileKey)]
    return fila

def reducirColumnas (nombreArchivo,ddff):
        if getExtension (nombreArchivo) == '.dbf':
            bdReducida = ddff.loc[:, ('fecha_dia', 'nro_centro', 'cve_tipo_c', 'glosa_reng', 'cve_debe_h', 'monto_mo',
                                     'cod_moneda', 'cod_movimi', 'nom_movimi',
                                         'monto_mn', 'glosa_comp', 'nro_compro', 'cod_mayor')]
        else:

            bdReducida = ddff.loc[:, ('fecha_dia', 'nro_centro', 'cve_tipo_comprob', 'glosa_reng', 'cve_debe_haber', 'monto_mo',
                                     'cod_moneda', 'cod_movimiento', 'nom_movimiento',
                                         'monto_mn', 'glosa_comprob', 'nro_comprob', 'cod_mayor')]
        return bdReducida