import PySimpleGUI as sg
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from junciones import *
#Archivo de parámetros, movimientos y palabras clave
parametros = "parametros.xlsx"
#Aqui empezaría la onda

# tema
sg.theme('LightGrey1')
# el diseño

layout = [[sg.T("")],
          losInputs("GEF: ","-GEF2-","GEF",30), losInputs("GOM: ","-GOM2-","GOM",26),
          losInputs("GOI: ","-GOI2-","GOI",34), losInputs("GTES: ","-GTESS-","GTES",22),
          [sg.Button("Procesar", pad=((350, 0), 30), font='Arial 12', button_color=('firebrick3'))]]
# Creamos la ventana
window = sg.Window('Balanza Cambiaria', layout, size=(750, 250))
# escuchamos los eventos
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Procesar":
        bdgef = leer(os.path.abspath(values["GEF"])) # lee una ruta
        bdgom = leer(os.path.abspath(values["GOM"]))
        bdgoi = leer(os.path.abspath(values["GOI"]))
        bdgtes = leer(os.path.abspath(values["GTES"]))
        #concatenamos todo
        bdBruto = pd.concat([bdgtes, bdgoi, bdgom, bdgef], ignore_index=True)
        # todo a minusculas
        bdBruto.columns = map(str.lower, bdBruto.columns)
        # reducimos columnas 
        print("bruta",bdBruto.shape)
        print ("reudcida ", reducirColumnas(os.path.abspath(values["GEF"]),bdBruto).shape)