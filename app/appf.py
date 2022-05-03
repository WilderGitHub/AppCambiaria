import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from junciones import *

#Archivo de parámetros, movimientos y palabras clave
parametros = "parametros.xlsx"
archivo="gtes10ene.xls"
#Aqui empezaría la onda
print ("leyendo archivo ", leer(archivo).head(3))