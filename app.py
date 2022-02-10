import PySimpleGUI as sg
import os

sg.theme('LightGrey1')   # tema
# el diseño
''' layout = [[sg.Text('Some text on Row 1')],
          [sg.Text('Enter something on Row 2'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]
 '''
# images column

layout = [[sg.T("")],
          [sg.Text("GEF: "),
           sg.Input(key="-GEF2-", change_submits=True, size=(70, 1)),
           sg.FileBrowse(key="-GEF-")],
          [sg.Text("GOM: "),
           sg.Input(key="-GOM2-", change_submits=True, size=(70, 1)),
           sg.FileBrowse(key="-GOM-")],
          [sg.Text("GOI: "),
           sg.Input(key="-GOI2-", change_submits=True, size=(70, 1)),
           sg.FileBrowse(key="-GOI-")],
          [sg.Text("GTES: "),
           sg.Input(key="-GTES2-", change_submits=True, size=(70, 1)),
           sg.FileBrowse(key="-GTES-")],
          [sg.Button("Procesar", 'right', size=(30, 1))]]

# Creamos la ventana
# window = sg.Window('Balenza Cambiaria', layout)
window = sg.Window('Balenza Cambiaria', layout, size=(750, 350))
# escuchamos los eventos
while True:
    event, values = window.read()
    # print(values["-GOI2-"])
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Procesar":
        direccion = values["-GEF-"]
        nombreGEF = os.path.basename(direccion)
        print(nombreGEF)
        direccion = values["-GOM-"]
        nombreGOM = os.path.basename(direccion)
        print(nombreGOM)
        direccion = values["-GOI-"]
        nombreGOI = os.path.basename(direccion)
        print(nombreGOI)
        direccion = values["-GTES-"]
        nombreGTES = os.path.basename(direccion)
        print(nombreGTES)
